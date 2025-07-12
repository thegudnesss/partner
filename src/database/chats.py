# partner/src/database/chats.py

from cashews import cache

from src.database import MongoBaseModel
from src.utils.logging import log

from src import i18n


class Chats(MongoBaseModel):
    id: str
    language_code: str

    @classmethod
    async def get_chat(cls, chat_id: int) -> "Chats | None":
        """
        Avval Redis'dan, bo‘lmasa MongoDB'dan chatni topadi
        """
        cache_key = f"chat:{chat_id}:data"
        cached_data = await cache.get(cache_key)
        if cached_data:
            log.debug(f"Chat {chat_id} loaded from Redis.")
            return cls(**cached_data)

        chat = await cls.find_one(id=str(chat_id))
        if chat:
            await cache.set(cache_key, chat.dict(), expire=3600)
            log.debug(f"Chat {chat_id} loaded from MongoDB and cached.")
            return chat

        log.debug(f"Chat {chat_id} not found.")
        return None

    @classmethod
    async def set_language(cls, chat_id: int, language_code: str) -> "Chats":
        """
        Chat language_code ni yangilaydi yoki yangi chat yaratadi
        """
        chat = await cls.find_one(id=str(chat_id))
        if chat:
            chat.language_code = language_code
            await chat.save()
            log.info(f"Chat {chat_id} language updated to {language_code}.")
        else:
            chat = cls(id=str(chat_id), language_code=language_code)
            await chat.save()
            log.info(f"Chat {chat_id} created with language {language_code}.")

        # Redisni yangilash
        cache_key = f"chat:{chat_id}:data"
        await cache.set(cache_key, chat.dict(), expire=3600)

        # Langni alohida cache qilamiz
        await cache.set(f"chat:{chat_id}:lang", language_code, expire=3600)

        return chat

    @classmethod
    async def get_language(cls, chat_id: int) -> str:
        """
        Chatning tilini oladi (Redis → Mongo tartibida)
        """
        cache_key = f"chat:{chat_id}:lang"
        lang = await cache.get(cache_key)
        if lang:
            log.debug(f"Chat {chat_id} language loaded from Redis.")
            return lang

        chat = await cls.get_chat(chat_id)
        if chat:
            await cache.set(cache_key, chat.language_code, expire=3600)
            return chat.language_code

        log.debug(f"Chat {chat_id} language not found. Defaulting to '{i18n.default_locale}'.")
        return i18n.default_locale

    @classmethod
    async def delete_chat(cls, chat_id: int) -> bool:
        """
        Chatni Mongo va Redisdan o‘chirish
        """
        deleted = await cls.delete(id=str(chat_id))
        if deleted:
            await cache.delete(f"chat:{chat_id}:data")
            await cache.delete(f"chat:{chat_id}:lang")
            log.info(f"Chat {chat_id} deleted from Mongo and Redis.")
        return deleted

    async def save(self) -> str:
        """
        Modelni MongoDB'ga saqlash, Redisni yangilash
        """
        result_id = await super().save()

        # Redisni avtomatik yangilash
        cache_key = f"chat:{self.id}:data"
        await cache.set(cache_key, self.dict(), expire=3600)

        await cache.set(f"chat:{self.id}:lang", self.language_code, expire=3600)
        log.debug(f"Chat {self.id} saved and cached in Redis.")
        return result_id
