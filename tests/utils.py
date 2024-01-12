import pytest
import telebot
from bot.telegram_interface import start_bot

@pytest.fixture
def start() -> None:
    start_bot()


