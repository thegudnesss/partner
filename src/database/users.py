from cashews import cache

from src.database import MongoBaseModel
from src.utils.logging import log

from src import i18n


class Users(MongoBaseModel):
    id: str
    language_code: str

    @classmethod
    async def get_user(cls, user_id: int) -> "Users | None":
        """
        Avval Redis'dan, bo‘lmasa MongoDB'dan userni topadi
        """
        cache_key = f"user:{user_id}:data"
        cached_data = await cache.get(cache_key)
        if cached_data:
            log.debug(f"User {user_id} loaded from Redis.")
            return cls(**cached_data)

        user = await cls.find_one(id=str(user_id))
        if user:
            await cache.set(cache_key, user.dict(), expire=3600)
            log.debug(f"User {user_id} loaded from MongoDB and cached.")
            return user

        log.debug(f"User {user_id} not found.")
        return None

    @classmethod
    async def set_language(cls, user_id: int, language_code: str) -> "Users":
        """
        User language_code ni yangilaydi yoki yangi user yaratadi
        """
        user = await cls.find_one(id=str(user_id))
        if user:
            user.language_code = language_code
            await user.save()
            log.info(f"User {user_id} language updated to {language_code}.")
        else:
            user = cls(id=str(user_id), language_code=language_code)
            await user.save()
            log.info(f"User {user_id} created with language {language_code}.")

        
        cache_key = f"user:{user_id}:data"
        await cache.set(cache_key, user.dict(), expire=3600)

        
        await cache.set(f"user:{user_id}:lang", language_code, expire=3600)

        return user

    @classmethod
    async def get_language(cls, user_id: int) -> str:
        """
        Userning tilini oladi (Redis → Mongo tartibida)
        """
        cache_key = f"user:{user_id}:lang"
        lang = await cache.get(cache_key)
        if lang:
            log.debug(f"User {user_id} language loaded from Redis.")
            return lang

        user = await cls.get_user(user_id)
        if user:
            await cache.set(cache_key, user.language_code, expire=3600)
            return user.language_code

        log.debug(f"User {user_id} language not found. Defaulting to 'en'.")
        return i18n.default_locale

    @classmethod
    async def delete_user(cls, user_id: int) -> bool:
        """
        Userni Mongo va Redisdan o‘chirish
        """
        deleted = await cls.delete(id=str(user_id))
        if deleted:
            await cache.delete(f"user:{user_id}:data")
            await cache.delete(f"user:{user_id}:lang")
            log.info(f"User {user_id} deleted from Mongo and Redis.")
        return deleted

    async def save(self) -> str:
        """
        Modelni MongoDB'ga saqlash, Redisni yangilash
        """
        result_id = await super().save()

        
        cache_key = f"user:{self.id}:data"
        await cache.set(cache_key, self.dict(), expire=3600)

        await cache.set(f"user:{self.id}:lang", self.language_code, expire=3600)
        log.debug(f"User {self.id} saved and cached in Redis.")
        return result_id
