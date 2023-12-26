import pytest
import telebot
from bot.telegram_interface import start_bot

@pytest.fixture
def start():
    start_bot()


