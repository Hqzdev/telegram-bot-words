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
        try:
            config = Config()
            bot_application = Application.builder().token(config.bot_token).build()
            setup_handlers(bot_application)
            logger.info("Bot application initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing bot: {e}")
            return None
    return bot_application

@app.route('/webhook', methods=['POST'])
def webhook():
    """Обработчик webhook от Telegram"""
    try:
        # Получаем данные запроса
        update_data = request.get_json()
        if not update_data:
            logger.error("No JSON data received")
            return jsonify({'error': 'No JSON data'}), 400
        
        # Инициализируем бота
        bot_app = get_bot_application()
        if not bot_app:
            return jsonify({'error': 'Bot not initialized'}), 500
        
        # Создаем Update объект
        update = Update.de_json(update_data, bot_app.bot)
        
        # Обрабатываем обновление
        bot_app.process_update(update)
        
        logger.info("Webhook processed successfully")
        return jsonify({'status': 'ok'})
        
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def health_check():
    """Проверка работоспособности бота"""
    try:
        bot_app = get_bot_application()
        if bot_app:
            return 'Bot is running! ✅'
        else:
            return 'Bot initialization failed! ❌'
    except Exception as e:
        return f'Bot error: {str(e)} ❌'

@app.route('/webhook', methods=['GET'])
def webhook_info():
    """Информация о webhook"""
    return jsonify({
        'status': 'active',
        'bot': 'Telegram Survey Bot',
        'webhook_url': '/webhook',
        'health': 'ok'
    })

@app.route('/test', methods=['GET'])
def test():
    """Тестовая страница"""
    return jsonify({
        'message': 'API is working!',
        'status': 'ok'
    })

# Экспортируем приложение для Vercel
if __name__ == '__main__':
    app.run(debug=True)
