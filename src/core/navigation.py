# src/core/navigation.py

import aioredis

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from src.callbacks.page_callbacks import PageCallback

class NavigationManager:
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self._redis = None

    async def connect(self):
        self._redis = await aioredis.from_url(self.redis_url)

    async def push(self, user_id: int, page_name: str):
        await self._redis.lpush(f"nav:{user_id}", page_name)

    async def pop(self, user_id: int) -> str:
        await self._redis.lpop(f"nav:{user_id}")

    async def last(self, user_id: int) -> str:
        page = await self._redis.lindex(f"nav:{user_id}", 0)
        if page:
            return page.decode()
        return "StartPage"

    async def get_back_button(self, user_id: int) -> InlineKeyboardMarkup:
        last_page = await self.last(user_id)
        cb_data = PageCallback(name=last_page).pack()
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="↩️ Ortga", callback_data=cb_data)]
        ])
        return markup

    def get_home_button(self) -> InlineKeyboardMarkup:
        cb_data = PageCallback(name="StartPage").pack()
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data=cb_data)]
        ])
        return markup
