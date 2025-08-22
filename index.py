def handler(request, context):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/plain'},
        'body': 'Bot is running! ✅'
    }
