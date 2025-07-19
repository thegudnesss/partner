# src/core/helpers.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Union

async def render_buttons(
    user_id: int,
    buttons: List[Union[str, dict]],
    extra: dict = None
) -> InlineKeyboardMarkup:
    keyboard = []
    for btn in buttons:
        if isinstance(btn, dict):
            keyboard.append([
                InlineKeyboardButton(
                    text=btn["text"],
                    callback_data=btn["callback_data"]
                )
            ])
        elif isinstance(btn, str):
            from src.callbacks.page_callbacks import PageCallback
            cb_data = PageCallback(name=btn, **(extra or {})).pack()
            keyboard.append([
                InlineKeyboardButton(
                    text=btn,
                    callback_data=cb_data
                )
            ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
