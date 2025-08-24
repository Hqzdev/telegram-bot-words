def handler(request, context):
    """Простой тестовый handler"""
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': '{"status": "Test endpoint working"}'
    }
