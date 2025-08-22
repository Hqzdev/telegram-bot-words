# 🚀 Руководство по хостингу на Vercel

## Подготовка к деплою

### Требования

- Аккаунт на [Vercel](https://vercel.com)
- Установленный [Vercel CLI](https://vercel.com/docs/cli)
- Настроенный Telegram Bot Token
- Настроенный Google Sheets API
- GitHub репозиторий с кодом

### Подготовка репозитория

Убедитесь, что в репозитории есть все необходимые файлы:

```
telegram-bot-words/
├── bot/
├── api/
├── main.py
├── vercel.json
├── requirements.txt
├── survey_config.json
└── README.md
```

## Деплой на Vercel

### Способ 1: Через Vercel CLI

#### 1. Установка Vercel CLI

```bash
npm install -g vercel
```

#### 2. Логин в Vercel

```bash
vercel login
```

#### 3. Деплой проекта

```bash
# Перейдите в папку проекта
cd telegram-bot-words

# Первоначальный деплой
vercel

# Для продакшена
vercel --prod
```

#### 4. Настройка переменных окружения

```bash
# Добавление переменных через CLI
vercel env add BOT_TOKEN
vercel env add GOOGLE_SHEETS_ID
vercel env add GOOGLE_CREDENTIALS_JSON
```

### Способ 2: Через Vercel Dashboard

#### 1. Подключение репозитория

1. Перейдите на [vercel.com](https://vercel.com)
2. Нажмите "New Project"
3. Выберите ваш GitHub репозиторий
4. Нажмите "Import"

#### 2. Настройка проекта

- **Framework Preset**: Other
- **Root Directory**: `./` (оставьте пустым)
- **Build Command**: оставьте пустым
- **Output Directory**: оставьте пустым
- **Install Command**: `pip install -r requirements.txt`

#### 3. Настройка переменных окружения

В разделе "Environment Variables" добавьте:

| Name | Value | Environment |
|------|-------|-------------|
| `BOT_TOKEN` | `your_telegram_bot_token` | Production, Preview |
| `GOOGLE_SHEETS_ID` | `your_sheets_id` | Production, Preview |
| `GOOGLE_CREDENTIALS_JSON` | `{"type":"service_account",...}` | Production, Preview |

**Важно:** Для `GOOGLE_CREDENTIALS_JSON` скопируйте все содержимое JSON файла с учетными данными.

#### 4. Деплой

Нажмите "Deploy"

## Настройка Webhook

### 1. Получение URL приложения

После деплоя вы получите URL вида:
```
https://your-app-name.vercel.app
```

### 2. Установка webhook

#### Через скрипт:

```bash
python setup_webhook.py
```

#### Через curl:

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://your-app-name.vercel.app/webhook"}'
```

#### Через браузер:

```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://your-app-name.vercel.app/webhook
```

### 3. Проверка webhook

```bash
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
```

## Проверка работоспособности

### 1. Проверка приложения

Откройте в браузере: `https://your-app-name.vercel.app/`
Должно появиться: "Bot is running!"

### 2. Проверка webhook

Откройте: `https://your-app-name.vercel.app/webhook`
Должно появиться JSON с информацией о webhook

### 3. Тестирование бота

1. Найдите вашего бота в Telegram
2. Отправьте `/start`
3. Пройдите опрос
4. Проверьте, что данные появились в Google Sheets

## Мониторинг

### 1. Логи Vercel

- Перейдите в Vercel Dashboard → ваш проект → Functions
- Просматривайте логи в реальном времени

### 2. Логи Telegram

```bash
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
```

### 3. Логи Google Sheets

- Проверяйте таблицу на наличие новых данных
- Используйте Google Cloud Console для мониторинга API

## Обновление бота

### 1. Автоматическое обновление

При push в GitHub репозиторий Vercel автоматически пересоберет и развернет приложение.

### 2. Ручное обновление

```bash
vercel --prod
```

### 3. Откат к предыдущей версии

В Vercel Dashboard → Deployments → выберите предыдущую версию → "Promote to Production"

## Устранение неполадок

### Ошибка "Function not found"

- Проверьте, что файл `api/webhook.py` существует
- Убедитесь, что Flask приложение правильно настроено

### Ошибка "Environment variable not found"

- Проверьте переменные окружения в Vercel Dashboard
- Убедитесь, что переменные добавлены для правильной среды (Production/Preview)

### Ошибка "Import error"

- Проверьте `requirements.txt`
- Убедитесь, что все зависимости указаны

### Бот не отвечает

1. Проверьте webhook: `curl "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"`
2. Проверьте логи в Vercel Dashboard
3. Убедитесь, что переменные окружения настроены правильно

### Ошибки с Google Sheets

1. Проверьте `GOOGLE_CREDENTIALS_JSON` в Vercel
2. Убедитесь, что Service Account имеет доступ к таблице
3. Проверьте `GOOGLE_SHEETS_ID`

### Ошибка "Quota exceeded"

- Google Sheets API имеет лимиты на количество запросов
- Для продакшена рассмотрите возможность увеличения квоты

## Оптимизация

### 1. Уменьшение размера бандла

- Удалите неиспользуемые зависимости из `requirements.txt`
- Используйте только необходимые модули

### 2. Улучшение производительности

- Используйте кэширование для Google Sheets API
- Оптимизируйте обработку данных

### 3. Безопасность

- Регулярно обновляйте зависимости
- Ротируйте ключи Service Account
- Используйте HTTPS для всех соединений

## Дополнительные настройки

### Увеличение квоты API

1. В Google Cloud Console перейдите в "APIs & Services" → "Quotas"
2. Найдите "Google Sheets API"
3. Нажмите "Edit Quotas"
4. Запросите увеличение лимитов

### Мониторинг использования

1. В Google Cloud Console перейдите в "APIs & Services" → "Dashboard"
2. Выберите "Google Sheets API"
3. Просматривайте статистику запросов и ошибок

## Поддержка

При возникновении проблем:

1. Проверьте логи в Vercel Dashboard
2. Убедитесь в правильности всех настроек
3. Проверьте документацию:
   - [Vercel Documentation](https://vercel.com/docs)
   - [Telegram Bot API](https://core.telegram.org/bots/api)
   - [Google Sheets API](https://developers.google.com/sheets/api)

## Быстрый старт

### Минимальные шаги для деплоя:

1. **Подготовка:**
   ```bash
   git clone <your-repo>
   cd telegram-bot-words
   ```

2. **Деплой:**
   ```bash
   vercel login
   vercel
   ```

3. **Настройка переменных в Vercel Dashboard:**
   - `BOT_TOKEN`
   - `GOOGLE_SHEETS_ID`
   - `GOOGLE_CREDENTIALS_JSON`

4. **Настройка webhook:**
   ```bash
   python setup_webhook.py
   ```

5. **Проверка:**
   - Откройте URL приложения
   - Протестируйте бота в Telegram
