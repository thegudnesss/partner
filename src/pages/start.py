# src/pages/start.py

from src.pages.base_page import BasePage
from src.callbacks.page_callbacks import PageCallback

class StartPage(BasePage):
    name = "StartPage"
    text_key = "page.start"
    buttons = [
        PageCallback(name="CatalogPage").pack(),
        PageCallback(name="SearchPage").pack(),
        PageCallback(name="ProfilePage").pack(),
    ]
