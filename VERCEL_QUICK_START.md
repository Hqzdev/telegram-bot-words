# Быстрый старт: Деплой на Vercel

## 🚀 Быстрый деплой (5 минут)

### 1. Установите Vercel CLI
```bash
npm install -g vercel
```

### 2. Войдите в аккаунт
```bash
vercel login
```

### 3. Деплойте проект
```bash
vercel --prod
```

### 4. Настройте переменные окружения
```bash
vercel env add TELEGRAM_TOKEN
vercel env add GOOGLE_SHEETS_ID
vercel env add GOOGLE_CREDENTIALS_JSON
```

### 5. Настройте webhook
```bash
python setup_webhook.py https://your-project.vercel.app
```

## 📋 Что было подготовлено

✅ **vercel.json** - конфигурация Vercel  
✅ **api/index.py** - serverless function для обработки webhook  
✅ **setup_webhook.py** - скрипт настройки webhook  
✅ **requirements.txt** - обновлен с requests  
✅ **DEPLOY_TO_VERCEL.md** - подробная инструкция  

## 🔧 Переменные окружения

Вам нужно будет добавить в Vercel:
- `TELEGRAM_TOKEN` - токен вашего бота
- `GOOGLE_SHEETS_ID` - ID Google таблицы
- `GOOGLE_CREDENTIALS_JSON` - содержимое JSON файла с credentials

## 🌐 После деплоя

1. Получите URL вида: `https://your-project.vercel.app`
2. Проверьте работу: `https://your-project.vercel.app/api`
3. Настройте webhook: `python setup_webhook.py https://your-project.vercel.app`

## 📖 Подробная инструкция

См. файл `DEPLOY_TO_VERCEL.md` для детальной информации.
