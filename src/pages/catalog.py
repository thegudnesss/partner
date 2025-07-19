# src/pages/catalog.py

from src.pages.base_page import BasePage
from src.callbacks.page_callbacks import PageCallback

class CatalogPage(BasePage):
    name = "CatalogPage"
    text_key = "page.catalog"
    buttons = [
        PageCallback(name="CategoryPage", extra="anime").pack(),
        PageCallback(name="CategoryPage", extra="kino").pack(),
    ]
