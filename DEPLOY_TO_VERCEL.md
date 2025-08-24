# Деплой Telegram бота на Vercel

## Подготовка к деплою

### 1. Установка Vercel CLI

```bash
npm install -g vercel
```

### 2. Логин в Vercel

```bash
vercel login
```

### 3. Подготовка переменных окружения

Создайте файл `.env` в корне проекта со следующими переменными:

```env
TELEGRAM_TOKEN=your_telegram_bot_token
GOOGLE_SHEETS_ID=your_google_sheets_id
GOOGLE_CREDENTIALS_FILE=your_google_credentials.json
```

**Важно:** Для Google Sheets вам нужно будет загрузить файл credentials в Vercel как переменную окружения.

## Деплой на Vercel

### 1. Инициализация проекта

```bash
vercel
```

Следуйте инструкциям:
- Выберите "Link to existing project" или создайте новый
- Выберите ваш аккаунт
- Выберите или создайте проект
- Подтвердите настройки

### 2. Настройка переменных окружения в Vercel

```bash
vercel env add TELEGRAM_TOKEN
vercel env add GOOGLE_SHEETS_ID
vercel env add GOOGLE_CREDENTIALS_FILE
```

Для каждой переменной введите соответствующее значение.

### 3. Деплой

```bash
vercel --prod
```

После успешного деплоя вы получите URL вида: `https://your-project.vercel.app`

## Настройка Webhook

### 1. Установка webhook

После деплоя выполните команду для настройки webhook:

```bash
python setup_webhook.py https://your-project.vercel.app
```

Замените `https://your-project.vercel.app` на ваш реальный URL.

### 2. Проверка webhook

Вы можете проверить статус webhook, перейдя по URL:
`https://your-project.vercel.app/api`

Должен вернуться JSON ответ: `{"status": "Bot is running"}`

## Управление деплоем

### Обновление бота

```bash
vercel --prod
```

### Просмотр логов

```bash
vercel logs
```

### Удаление webhook (если нужно)

```bash
python setup_webhook.py --delete
```

## Структура файлов для Vercel

```
telegram-bott/
├── api/
│   └── index.py          # Vercel serverless function
├── bot/                  # Модули бота
├── vercel.json          # Конфигурация Vercel
├── requirements.txt     # Python зависимости
├── setup_webhook.py    # Скрипт настройки webhook
└── .env                # Локальные переменные окружения
```

## Возможные проблемы

### 1. Ошибка с Google Credentials

Если у вас проблемы с Google Sheets, убедитесь что:
- Файл credentials загружен в переменные окружения Vercel
- Учетная запись Google имеет доступ к Sheets API

### 2. Webhook не работает

Проверьте:
- URL webhook правильный
- Бот токен корректный
- Vercel приложение работает

### 3. Таймауты

Если бот не отвечает, проверьте логи Vercel:
```bash
vercel logs
```

## Альтернативный способ деплоя через GitHub

1. Загрузите код в GitHub репозиторий
2. Подключите репозиторий к Vercel через веб-интерфейс
3. Настройте переменные окружения в Vercel Dashboard
4. Деплой будет происходить автоматически при push в main ветку

## Мониторинг

- Логи: `vercel logs`
- Статус: Vercel Dashboard
- Webhook статус: `https://api.telegram.org/bot<TOKEN>/getWebhookInfo`
