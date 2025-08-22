"""
Webhook endpoint для Telegram Bot на Vercel
"""

import os
import json
import logging
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import Application
from bot.handlers import setup_handlers
from bot.config import Config

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Создаем Flask приложение
app = Flask(__name__)

# Глобальная переменная для хранения экземпляра бота
bot_application = None

def get_bot_application():
    """Получить или создать экземпляр бота"""
    global bot_application
    if bot_application is None:
        config = Config()
        bot_application = Application.builder().token(config.bot_token).build()
        setup_handlers(bot_application)
    return bot_application

@app.route('/webhook', methods=['POST'])
def webhook():
    """Обработчик webhook от Telegram"""
    try:
        # Получаем данные запроса
        update_data = request.get_json()
        update = Update.de_json(update_data, get_bot_application().bot)
        
        # Обрабатываем обновление
        get_bot_application().process_update(update)
        
        return jsonify({'status': 'ok'})
        
    except Exception as e:
        logger.error(f"Ошибка при обработке webhook: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def health_check():
    """Проверка работоспособности бота"""
    return 'Bot is running!'

@app.route('/webhook', methods=['GET'])
def webhook_info():
    """Информация о webhook"""
    return jsonify({
        'status': 'active',
        'bot': 'Telegram Survey Bot',
        'webhook_url': '/webhook'
    })

# Экспортируем приложение для Vercel
app.debug = False
