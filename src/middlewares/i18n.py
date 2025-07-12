
from typing import Any, cast

from aiogram.enums import ChatType
from aiogram.types import Chat, TelegramObject, User
from aiogram.utils.i18n import I18nMiddleware

from src.database import Users, Chats
    
class MyI18nMiddleware(I18nMiddleware):
    async def get_locale(self, event: TelegramObject, data: dict[str, Any]) -> str:
        user: User | None = data.get("event_from_user")
        chat: Chat | None = data.get("event_chat")

        if not user or not chat:
            return self.i18n.default_locale

        if chat.type == ChatType.PRIVATE:
            user_db = await Users.get_user(user=user)
            language_code = await Users.get_language(user=user)
            if not user_db:
                return self.i18n.default_locale
        else:
            chat_db = await Chats.get_chat(chat=chat)
            language_code = await Chats.get_language(chat=chat)
            if not chat_db:
                return self.i18n.default_locale

        if language_code not in self.i18n.available_locales:
            return self.i18n.default_locale

        return cast(str, language_code)
