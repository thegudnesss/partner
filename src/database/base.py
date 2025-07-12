# partner/src/database/base.py

from typing import TypeVar, Type, Any, List, Optional, Self
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from bson import ObjectId

from src.config import config
from src.utils.logging import log

T = TypeVar("T", bound="MongoBaseModel")


class PyObjectId(ObjectId):
    """
    BSON ObjectId uchun custom field converter.
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        elif isinstance(v, str):
            return str(ObjectId(v))
        raise ValueError(f"Invalid ObjectId: {v}")

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class MongoBaseModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")

    class Config:
        json_encoders = {
            ObjectId: str
        }
        allow_population_by_field_name = True

    @classmethod
    def _collection_name(cls) -> str:
        name = cls.__name__
        if name.endswith("Model"):
            name = name[:-5]
        name = name.lower()
        if name.endswith("s"):
            return name
        return name + "s"


    @classmethod
    def _db(cls):
        client = AsyncIOMotorClient(config.mongo_uri)
        return client[config.mongo_db_name]

    @classmethod
    async def find_one(cls: Type[T], **query) -> Optional[T]:
        col = cls._db()[cls._collection_name()]
        document = await col.find_one(query)
        if document:
            document["id"] = str(document.pop("_id"))
            return cls(**document)
        return None

    @classmethod
    async def find_many(cls: Type[T], **query) -> List[T]:
        col = cls._db()[cls._collection_name()]
        cursor = col.find(query)
        result = []
        async for doc in cursor:
            doc["id"] = str(doc.pop("_id"))
            result.append(cls(**doc))
        return result

    @classmethod
    async def insert(cls: Type[T], **data) -> str:
        col = cls._db()[cls._collection_name()]
        result = await col.insert_one(data)
        log.info(f"Inserted document into {cls._collection_name()}", inserted_id=str(result.inserted_id))
        return str(result.inserted_id)

    @classmethod
    async def update(cls: Type[T], filter: dict[str, Any], update: dict[str, Any]) -> Optional[T]:
        col = cls._db()[cls._collection_name()]
        await col.update_one(filter, {"$set": update})
        return await cls.find_one(**filter)

    @classmethod
    async def delete(cls: Type[T], **query) -> bool:
        col = cls._db()[cls._collection_name()]
        result = await col.delete_one(query)
        log.info(f"Deleted {result.deleted_count} document(s) from {cls._collection_name()}")
        return result.deleted_count > 0

    async def save(self: Self) -> str:
        data = self.dict(by_alias=True, exclude={"id"})
        col = self._db()[self._collection_name()]
        if self.id:
            await col.update_one({"_id": ObjectId(self.id)}, {"$set": data})
            log.info(f"Updated document {self.id} in {self._collection_name()}")
            return self.id
        else:
            result = await col.insert_one(data)
            self.id = str(result.inserted_id)
            log.info(f"Inserted new document {self.id} into {self._collection_name()}")
            return self.id
