# src/callbacks/page_callbacks.py

from aiogram.filters.callback_data import CallbackData

class PageCallback(CallbackData, prefix="page"):
    name: str
    page: int = 1
    extra: str = None
