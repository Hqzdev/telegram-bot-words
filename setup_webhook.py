#!/usr/bin/env python3
"""
Скрипт для настройки webhook в Telegram Bot API
"""

import os
import requests
from dotenv import load_dotenv

def setup_webhook(vercel_url):
    """
    Настраивает webhook для Telegram бота
    
    Args:
        vercel_url (str): URL вашего Vercel приложения
    """
    # Загружаем переменные окружения
    load_dotenv()
    
    # Получаем токен бота
    bot_token = os.getenv('TELEGRAM_TOKEN')
    if not bot_token:
        print("Ошибка: TELEGRAM_TOKEN не найден в переменных окружения")
        return
    
    # Формируем URL для webhook
    webhook_url = f"{vercel_url}/api"
    
    # URL для установки webhook
    set_webhook_url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
    
    # Данные для запроса
    data = {
        'url': webhook_url,
        'allowed_updates': ['message', 'callback_query']
    }
    
    try:
        # Отправляем запрос
        response = requests.post(set_webhook_url, json=data)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get('ok'):
            print(f"✅ Webhook успешно установлен!")
            print(f"URL: {webhook_url}")
            
            # Проверяем информацию о webhook
            info_url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
            info_response = requests.get(info_url)
            info_result = info_response.json()
            
            if info_result.get('ok'):
                webhook_info = info_result.get('result', {})
                print(f"Статус: {webhook_info.get('url', 'Не установлен')}")
                print(f"Последняя ошибка: {webhook_info.get('last_error_message', 'Нет ошибок')}")
        else:
            print(f"❌ Ошибка при установке webhook: {result.get('description')}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка сети: {e}")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")

def delete_webhook():
    """Удаляет webhook для Telegram бота"""
    # Загружаем переменные окружения
    load_dotenv()
    
    # Получаем токен бота
    bot_token = os.getenv('TELEGRAM_TOKEN')
    if not bot_token:
        print("Ошибка: TELEGRAM_TOKEN не найден в переменных окружения")
        return
    
    # URL для удаления webhook
    delete_webhook_url = f"https://api.telegram.org/bot{bot_token}/deleteWebhook"
    
    try:
        # Отправляем запрос
        response = requests.post(delete_webhook_url)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get('ok'):
            print("✅ Webhook успешно удален!")
        else:
            print(f"❌ Ошибка при удалении webhook: {result.get('description')}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка сети: {e}")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Использование:")
        print("  python setup_webhook.py <vercel_url>  # Установить webhook")
        print("  python setup_webhook.py --delete      # Удалить webhook")
        print("\nПример:")
        print("  python setup_webhook.py https://your-bot.vercel.app")
        sys.exit(1)
    
    if sys.argv[1] == '--delete':
        delete_webhook()
    else:
        vercel_url = sys.argv[1]
        setup_webhook(vercel_url)
