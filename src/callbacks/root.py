# src/callbacks/root.py

from aiogram.filters.callback_data import CallbackData


class RootCallback(CallbackData, prefix="root"):
    section: str
