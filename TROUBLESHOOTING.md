# Устранение ошибок при деплое на Vercel

## Ошибка 500: INTERNAL_SERVER_ERROR

### Возможные причины:

1. **Отсутствуют переменные окружения**
2. **Неправильный формат Google credentials**
3. **Ошибки в коде инициализации**

### Пошаговое решение:

#### 1. Проверьте переменные окружения

Убедитесь, что в Vercel настроены все переменные:

```bash
vercel env ls
```

Должны быть:
- `TELEGRAM_TOKEN`
- `GOOGLE_SHEETS_ID` 
- `GOOGLE_CREDENTIALS_JSON`

#### 2. Правильный формат Google credentials

Для переменной `GOOGLE_CREDENTIALS_JSON` нужно скопировать **содержимое** JSON файла, а не путь к файлу.

Пример правильного формата:
```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "service-account@project.iam.gserviceaccount.com",
  "client_id": "client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/service-account%40project.iam.gserviceaccount.com"
}
```

#### 3. Проверьте логи

```bash
vercel logs
```

#### 4. Тестовый endpoint

Попробуйте сначала простой endpoint:

```bash
# Переименуйте api/index.py в api/index_backup.py
# Переименуйте api/test.py в api/index.py
# Деплойте заново
vercel --prod
```

#### 5. Постепенная отладка

Если тестовый endpoint работает, постепенно добавляйте функциональность:

1. Сначала только инициализация конфигурации
2. Потом инициализация бота
3. Затем обработчики

### Альтернативное решение

Если проблемы продолжаются, используйте polling вместо webhook:

1. Создайте отдельный файл `polling_bot.py`
2. Запустите его на отдельном сервере (например, Railway, Heroku)
3. Используйте `bot.run_polling()` вместо webhook

### Проверка работоспособности

После исправления проверьте:

1. **GET запрос**: `https://your-project.vercel.app/api`
   - Должен вернуть: `{"status": "Bot is running"}`

2. **Webhook статус**: 
   ```bash
   curl "https://api.telegram.org/bot<YOUR_TOKEN>/getWebhookInfo"
   ```

3. **Отправьте сообщение боту** в Telegram

### Частые ошибки

#### "Module not found"
- Проверьте `requirements.txt`
- Убедитесь, что все импорты корректны

#### "Invalid credentials"
- Проверьте формат `GOOGLE_CREDENTIALS_JSON`
- Убедитесь, что service account имеет доступ к Sheets API

#### "Token invalid"
- Проверьте `TELEGRAM_TOKEN`
- Убедитесь, что бот не заблокирован

### Контакты для поддержки

Если ничего не помогает:
1. Проверьте логи Vercel
2. Создайте issue в GitHub
3. Обратитесь в поддержку Vercel
