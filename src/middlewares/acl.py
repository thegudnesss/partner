from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.enums import ChatType
from aiogram.types import Chat, TelegramObject, User
from collections.abc import Awaitable, Callable
from typing import Any

from src import i18n
from src.database import Users, Chats
from babel import Locale, UnknownLocaleError

class ACLMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user: User | None = data.get("event_from_user")
        chat: Chat | None = data.get("event_chat")

        if user and not user.is_bot:
            userdb = await Users.get_user(user=user)
            if not userdb:
                locale = i18n.default_locale
                if user.language_code:
                    try:
                        locale_obj = Locale.parse(user.language_code, sep="-")
                        if str(locale_obj) in i18n.available_locales:
                            locale = str(locale_obj)
                    except UnknownLocaleError:
                        pass

                if chat and chat.type == ChatType.PRIVATE:
                    userdb = await Users.set_language(
                        user=user,
                        language_code=locale,
                    )
            data["user"] = userdb

        if chat:
            chatdb = await Chats.get_chat(chat=chat)
            if not chatdb and chat.type in {ChatType.GROUP, ChatType.SUPERGROUP}:
                chatdb = await Chats.set_language(
                    chat=chat,
                    language_code=i18n.default_locale,
                )
            data["chat"] = chatdb

        return await handler(event, data)
