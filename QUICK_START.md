# Быстрый запуск Telegram-бота

## Предварительные требования

1. ✅ Python 3.7+ установлен
2. ✅ Получен токен от @BotFather
3. ✅ Создана Google Sheets таблица
4. ✅ Настроен Google Cloud Service Account
5. ✅ Файл `credentials.json` помещен в корневую папку

## Шаги запуска

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Настройка переменных окружения
Создайте файл `.env` в корневой папке:
```env
TELEGRAM_TOKEN=ваш_токен_бота
GOOGLE_SHEETS_ID=id_вашей_таблицы
GOOGLE_CREDENTIALS_FILE=credentials.json
```

### 3. Тестирование конфигурации
```bash
python3 test_config.py
```

### 4. Запуск бота
```bash
python3 main.py
```

## Проверка работы

1. Найдите вашего бота в Telegram
2. Отправьте `/start`
3. Пройдите тестовый опрос
4. Проверьте данные в Google Sheets

## Остановка бота

Нажмите `Ctrl+C` в терминале

## Логи

Логи выводятся в консоль. При ошибках проверьте:
- Правильность токена
- Доступ к Google Sheets
- Корректность файла credentials.json
