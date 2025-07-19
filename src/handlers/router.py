# src/handlers/router.py

from aiogram import Router
from aiogram.types import CallbackQuery
from src.callbacks.page_callbacks import PageCallback

router = Router()

@router.callback_query(PageCallback.filter())
async def page_router(cb: CallbackQuery, callback_data: PageCallback):
    from src.pages import base_page
    from src.pages.start import StartPage
    from src.pages.catalog import CatalogPage
    from src.pages.category import CategoryPage
    from src.pages.media_detail import MediaDetailPage
    from src.pages.profile import ProfilePage
    from src.pages.search import SearchPage
    from src.pages.settings import SettingsPage

    pages = {
        "StartPage": StartPage,
        "CatalogPage": CatalogPage,
        "CategoryPage": CategoryPage,
        "MediaDetailPage": MediaDetailPage,
        "ProfilePage": ProfilePage,
        "SearchPage": SearchPage,
        "SettingsPage": SettingsPage,
    }

    page_cls = pages.get(callback_data.name)
    if not page_cls:
        await cb.answer("Sahifa topilmadi.")
        return

    page = page_cls(cb.from_user.id, page=callback_data.page, extra=callback_data.extra)
    await page.render(cb)
