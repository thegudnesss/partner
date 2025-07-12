import asyncio
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.i18n import I18n
from cashews import cache

from src.config import config


# Yo'llarni sozlash
app_dir: Path = Path(__file__).parent.parent
locales_dir: Path = app_dir / "locales"

# Redis cache
cache.setup(f"redis://{config.redis_host}", client_side=True)

# Bot
bot = Bot(
    token=config.bot_token.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

# Dispatcher
dp = Dispatcher()

# I18N
i18n = I18n(
    path=locales_dir,
    default_locale=config.default_language,
    domain="bot"
)

# API Clients (trace moe)
# Hozircha TraceMoeClient yo‘q, importni commentda qoldirdim
# from src.utils.api_clients.trace_moe import TraceMoeClient
# TraceMoe = TraceMoeClient()

# Logger (logging.py yo‘q hozircha)
# from src.utils.logging import log
# log.info("MyMediaBot loaded init config successfully!")

