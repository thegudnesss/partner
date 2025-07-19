# src/pages/base_page.py

from aiogram.types import Message, CallbackQuery
from typing import Union

from src.core.answer import answer
from src.core.helpers import gettext, render_buttons


class BasePage:
    name: str
    text_key: str
    buttons_key: str

    def __init__(self, user_id: int, lang: str = "uz", page: int = 1):
        self.user_id = user_id
        self.lang = lang
        self.page = page

    def get_text(self) -> str:
        return gettext(self.lang, self.text_key)

    def get_keyboard(self):
        return render_buttons(self.lang, self.buttons_key)

    async def render(self, union: Union[Message, CallbackQuery]):
        text = self.get_text()
        keyboard = self.get_keyboard()
        await answer(union, text, keyboard)
