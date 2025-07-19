import asyncio
from pathlib import Path

from aiogram.types.chat import Chat

a = Chat.has_protected_content

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.i18n import I18n
from cashews import cache

from src.config import config

app_dir: Path = Path(__file__).parent.parent
locales_dir: Path = app_dir / "locales"

cache.setup(f"redis://{config.redis_host}", client_side=True)

bot = Bot(
    token=config.bot_token.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)


dp = Dispatcher()


i18n = I18n(
    path=locales_dir,
    default_locale=config.default_language,
    domain="bot"
)

