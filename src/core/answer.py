# src/core/answer.py

from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from typing import Union

async def answer(
    union: Union[Message, CallbackQuery],
    text: str,
    reply_markup: InlineKeyboardMarkup = None,
    parse_mode: str = "HTML",
):
    is_callback = isinstance(union, CallbackQuery)
    target = union.message if is_callback else union
    await target.answer(
        text=text,
        reply_markup=reply_markup,
        parse_mode=parse_mode,
    )
