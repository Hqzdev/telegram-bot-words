# 🤖 Настройка Telegram Survey Bot

## Описание

Telegram бот для проведения опросов собственников земельных участков с автоматическим сохранением данных в Google Sheets. Между анкетами автоматически добавляются 2 пустые строки для удобства чтения.

## Особенности

- 📝 Интерактивные опросы с различными типами вопросов
- 📊 Автоматическое сохранение ответов в Google Sheets
- 🔄 Интервал в 2 строки между анкетами для удобства чтения
- 🎯 Поддержка комментариев к ответам
- 🚀 Готовность к деплою на Vercel

## Структура проекта

```
telegram-bot-words/
├── bot/                    # Основные модули бота
│   ├── __init__.py
│   ├── bot_instance.py     # Инициализация бота
│   ├── config.py          # Конфигурация
│   ├── data_processor.py  # Обработка данных
│   ├── google_sheets.py   # Работа с Google Sheets
│   ├── handlers.py        # Обработчики команд
│   ├── keyboard_builder.py # Построение клавиатур
│   └── survey_manager.py  # Управление опросами
├── api/
│   └── webhook.py         # Webhook для Vercel
├── main.py                # Локальный запуск
├── vercel.json           # Конфигурация Vercel
├── requirements.txt      # Зависимости Python
├── survey_config.json    # Конфигурация опроса
└── README.md            # Документация
```

## 1. Создание Telegram Bot

### 1.1 Получение токена бота

1. Найдите [@BotFather](https://t.me/botfather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям:
   - Введите имя бота (например: "Опрос землевладельцев")
   - Введите username бота (например: "land_survey_bot")
4. Сохраните полученный токен

### 1.2 Настройка описания бота

```bash
# Установка описания
/setdescription - "Опрос собственников земельных участков для планирования развития сельскохозяйственных территорий"

# Установка информации о боте
/setabouttext - "Бот для сбора информации о земельных участках и планах их развития"
```

## 2. Настройка Google Sheets API

### 2.1 Создание проекта в Google Cloud Console

1. Перейдите в [Google Cloud Console](https://console.cloud.google.com/)
2. Создайте новый проект или выберите существующий
3. Запомните ID проекта

### 2.2 Включение Google Sheets API

1. В меню слева выберите "APIs & Services" → "Library"
2. Найдите "Google Sheets API"
3. Нажмите на него и нажмите "Enable"

### 2.3 Создание Service Account

1. В меню слева выберите "APIs & Services" → "Credentials"
2. Нажмите "Create Credentials" → "Service Account"
3. Заполните форму:
   - **Service account name**: `telegram-bot-sheets`
   - **Service account ID**: автоматически заполнится
   - **Description**: `Service account for Telegram bot Google Sheets integration`
4. Нажмите "Create and Continue"
5. На следующем экране нажмите "Continue"
6. Нажмите "Done"

### 2.4 Создание ключа для Service Account

1. В списке Service Accounts найдите созданный аккаунт
2. Нажмите на него
3. Перейдите на вкладку "Keys"
4. Нажмите "Add Key" → "Create new key"
5. Выберите "JSON"
6. Нажмите "Create"
7. Файл автоматически скачается

### 2.5 Настройка Google Sheets

1. Создайте новую таблицу в [Google Sheets](https://sheets.google.com/)
2. Скопируйте ID таблицы из URL:
   ```
   https://docs.google.com/spreadsheets/d/YOUR_SHEETS_ID_HERE/edit
   ```
3. Предоставьте доступ Service Account:
   - Нажмите "Share" в правом верхнем углу
   - В поле "Add people and groups" введите email из Service Account
   - Email выглядит так: `telegram-bot-sheets@your-project.iam.gserviceaccount.com`
   - Установите права "Editor"
   - Нажмите "Send" (можно убрать галочку "Notify people")

## 3. Локальная установка

### 3.1 Клонирование репозитория

```bash
git clone <your-repo-url>
cd telegram-bot-words
```

### 3.2 Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3.3 Настройка переменных окружения

Создайте файл `.env` на основе `env_example.txt`:

```bash
cp env_example.txt .env
```

Заполните переменные в `.env`:

```env
BOT_TOKEN=your_telegram_bot_token
GOOGLE_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEETS_ID=your_google_sheets_id
```

### 3.4 Размещение учетных данных

1. Переименуйте скачанный JSON файл в `credentials.json`
2. Поместите его в корневую папку проекта

### 3.5 Запуск бота

```bash
python main.py
```

## 4. Конфигурация опроса

Настройка вопросов производится в файле `survey_config.json`:

```json
{
  "questions": {
    "q1_1": {
      "text": "Ваш вопрос здесь",
      "type": "single_choice",
      "options": [
        {
          "id": "option1",
          "text": "Вариант 1",
          "comment_required": false
        }
      ],
      "next": "q1_2"
    }
  }
}
```

### Типы вопросов:

- `text` - текстовый ответ
- `single_choice` - выбор одного варианта
- `multi_choice` - выбор нескольких вариантов

## 5. Структура данных в Google Sheets

Данные сохраняются в следующем формате:

| A (Вопросы) | B (Ответы) |
|-------------|------------|
| Вопрос 1 | Ответ 1 |
| Вопрос 2 | Ответ 2 |
| ... | ... |
| | |
| | |
| Вопрос 1 (следующая анкета) | Ответ 1 |
| Вопрос 2 (следующая анкета) | Ответ 2 |

**Важно:** Между анкетами автоматически добавляются 2 пустые строки для удобства чтения.

## 6. Проверка настройки

### 6.1 Локальная проверка

```bash
python -c "
from bot.config import Config
from bot.google_sheets import GoogleSheetsManager
config = Config()
sheets = GoogleSheetsManager(config)
print('✅ Подключение к Google Sheets успешно!')
"
```

### 6.2 Тестирование бота

1. Найдите вашего бота в Telegram
2. Отправьте `/start`
3. Пройдите опрос
4. Проверьте, что данные появились в Google Sheets

## 7. Устранение неполадок

### 7.1 Бот не отвечает
- Проверьте правильность BOT_TOKEN
- Убедитесь, что бот запущен
- Проверьте логи в консоли

### 7.2 Ошибки с Google Sheets
- Убедитесь, что Service Account имеет права "Editor" на таблицу
- Проверьте правильность `GOOGLE_SHEETS_ID`
- Проверьте формат файла `credentials.json`

### 7.3 Ошибка "Access denied"
- Убедитесь, что Service Account имеет права "Editor" на таблицу
- Проверьте правильность email в настройках доступа

### 7.4 Ошибка "Invalid credentials"
- Проверьте правильность JSON файла
- Убедитесь, что Google Sheets API включен в проекте

### 7.5 Ошибка "Spreadsheet not found"
- Проверьте правильность `GOOGLE_SHEETS_ID`
- Убедитесь, что таблица существует и доступна

## 8. Безопасность

⚠️ **Важно:**
- Никогда не коммитьте `credentials.json` в Git
- Добавьте `credentials.json` в `.gitignore`
- Регулярно ротируйте ключи Service Account
- Используйте HTTPS для всех соединений

## 9. Мониторинг

### 9.1 Логи
- Для локальной разработки логи выводятся в консоль
- Уровень логирования: INFO

### 9.2 Google Cloud Console
1. Перейдите в "APIs & Services" → "Dashboard"
2. Выберите "Google Sheets API"
3. Просматривайте статистику запросов и ошибок

## 10. Поддержка

При возникновении проблем:
1. Проверьте логи в консоли
2. Убедитесь в правильности всех настроек
3. Проверьте документацию Telegram Bot API и Google Sheets API
