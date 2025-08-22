"""
Экземпляр Telegram бота
"""

import os
from telegram.ext import Application

# Бот будет инициализирован после загрузки конфигурации
bot = None

def initialize_bot():
    """Инициализировать бота после загрузки конфигурации"""
    global bot
    from bot.config import Config
    config = Config()
    bot = Application.builder().token(config.telegram_token).build()
    return bot
