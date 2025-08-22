#!/usr/bin/env python3
"""
Скрипт для настройки webhook Telegram Bot
"""

import os
import requests
import json
from dotenv import load_dotenv

def setup_webhook(bot_token: str, webhook_url: str):
    """Настроить webhook для Telegram Bot"""
    
    # URL для установки webhook
    url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
    
    # Данные для webhook
    data = {
        "url": webhook_url,
        "allowed_updates": ["message", "callback_query"]
    }
    
    try:
        # Отправляем запрос
        response = requests.post(url, json=data)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get("ok"):
            print(f"✅ Webhook успешно установлен: {webhook_url}")
            print(f"📊 Информация: {result.get('description', 'N/A')}")
        else:
            print(f"❌ Ошибка установки webhook: {result.get('description', 'Unknown error')}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка сети: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ Ошибка парсинга JSON: {e}")

def get_webhook_info(bot_token: str):
    """Получить информацию о текущем webhook"""
    
    url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get("ok"):
            webhook_info = result.get("result", {})
            print("📋 Информация о webhook:")
            print(f"   URL: {webhook_info.get('url', 'Не установлен')}")
            print(f"   Ошибки: {webhook_info.get('last_error_message', 'Нет')}")
            print(f"   Обновления: {webhook_info.get('pending_update_count', 0)}")
        else:
            print(f"❌ Ошибка получения информации: {result.get('description', 'Unknown error')}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка сети: {e}")

def delete_webhook(bot_token: str):
    """Удалить webhook"""
    
    url = f"https://api.telegram.org/bot{bot_token}/deleteWebhook"
    
    try:
        response = requests.post(url)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get("ok"):
            print("✅ Webhook успешно удален")
        else:
            print(f"❌ Ошибка удаления webhook: {result.get('description', 'Unknown error')}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка сети: {e}")

def main():
    """Главная функция"""
    
    # Загружаем переменные окружения
    load_dotenv()
    
    # Получаем токен бота
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        print("❌ Не установлена переменная BOT_TOKEN")
        return
    
    print("🤖 Telegram Bot Webhook Manager")
    print("=" * 40)
    
    while True:
        print("\nВыберите действие:")
        print("1. Установить webhook")
        print("2. Получить информацию о webhook")
        print("3. Удалить webhook")
        print("4. Выход")
        
        choice = input("\nВведите номер (1-4): ").strip()
        
        if choice == "1":
            webhook_url = input("Введите URL webhook (например: https://your-app.vercel.app/webhook): ").strip()
            if webhook_url:
                setup_webhook(bot_token, webhook_url)
            else:
                print("❌ URL не может быть пустым")
                
        elif choice == "2":
            get_webhook_info(bot_token)
            
        elif choice == "3":
            confirm = input("Вы уверены, что хотите удалить webhook? (y/N): ").strip().lower()
            if confirm == 'y':
                delete_webhook(bot_token)
                
        elif choice == "4":
            print("👋 До свидания!")
            break
            
        else:
            print("❌ Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
