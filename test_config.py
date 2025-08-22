#!/usr/bin/env python3
"""
Скрипт для тестирования конфигурации бота
"""

import json
import os
from dotenv import load_dotenv
from bot.survey_manager import SurveyManager
from bot.config import Config

def test_survey_config():
    """Тестирование конфигурации опроса"""
    print("🔍 Тестирование конфигурации опроса...")
    
    try:
        survey_manager = SurveyManager()
        print("✅ Конфигурация опроса загружена успешно")
        
        # Проверяем количество вопросов
        questions = survey_manager.config.get("questions", {})
        print(f"📝 Найдено вопросов: {len(questions)}")
        
        # Проверяем первый вопрос
        first_question = survey_manager.get_question("q1_1")
        if first_question:
            print(f"✅ Первый вопрос: {first_question.get('text', '')[:50]}...")
        else:
            print("❌ Первый вопрос не найден")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка загрузки конфигурации: {e}")
        return False

def test_env_variables():
    """Тестирование переменных окружения"""
    print("\n🔍 Тестирование переменных окружения...")
    
    load_dotenv()
    
    required_vars = [
        'TELEGRAM_TOKEN',
        'GOOGLE_SHEETS_ID',
        'GOOGLE_CREDENTIALS_FILE'
    ]
    
    all_present = True
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            if var == 'TELEGRAM_TOKEN':
                print(f"✅ {var}: {'*' * 10}...{value[-4:]}")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: не установлена")
            all_present = False
    
    return all_present

def test_credentials_file():
    """Тестирование файла учетных данных"""
    print("\n🔍 Тестирование файла учетных данных...")
    
    credentials_file = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
    
    if os.path.exists(credentials_file):
        try:
            with open(credentials_file, 'r') as f:
                data = json.load(f)
            
            if 'client_email' in data and 'private_key' in data:
                print(f"✅ Файл {credentials_file} содержит корректные данные")
                print(f"📧 Service Account email: {data['client_email']}")
                return True
            else:
                print(f"❌ Файл {credentials_file} не содержит необходимые поля")
                return False
                
        except json.JSONDecodeError:
            print(f"❌ Файл {credentials_file} не является корректным JSON")
            return False
        except Exception as e:
            print(f"❌ Ошибка чтения файла {credentials_file}: {e}")
            return False
    else:
        print(f"❌ Файл {credentials_file} не найден")
        return False

def test_config_class():
    """Тестирование класса конфигурации"""
    print("\n🔍 Тестирование класса конфигурации...")
    
    try:
        # Проверяем, что переменные окружения установлены
        if not test_env_variables():
            print("⚠️  Пропускаем тест конфигурации (переменные не установлены)")
            return False
        
        config = Config()
        print("✅ Класс конфигурации создан успешно")
        
        # Проверяем, что все поля заполнены
        if config.telegram_token and config.google_sheets_id and config.google_credentials_file:
            print("✅ Все поля конфигурации заполнены")
            return True
        else:
            print("❌ Не все поля конфигурации заполнены")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка создания конфигурации: {e}")
        return False

def main():
    """Главная функция тестирования"""
    print("🚀 Тестирование конфигурации Telegram-бота")
    print("=" * 50)
    
    tests = [
        ("Конфигурация опроса", test_survey_config),
        ("Переменные окружения", test_env_variables),
        ("Файл учетных данных", test_credentials_file),
        ("Класс конфигурации", test_config_class)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Ошибка в тесте '{test_name}': {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Результаты тестирования:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ ПРОЙДЕН" if result else "❌ ПРОВАЛЕН"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\n📈 Итого: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 Все тесты пройдены! Бот готов к запуску.")
        return True
    else:
        print("⚠️  Некоторые тесты не пройдены. Проверьте конфигурацию.")
        return False

if __name__ == "__main__":
    main()
