from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is running! ✅'

@app.route('/webhook', methods=['POST'])
def webhook():
    return jsonify({'status': 'ok'})

@app.route('/webhook', methods=['GET'])
def webhook_info():
    return jsonify({
        'status': 'active',
        'message': 'Webhook endpoint is working'
    })

@app.route('/test')
def test():
    return jsonify({
        'message': 'API is working!',
        'status': 'ok'
    })

if __name__ == '__main__':
    app.run(debug=True)
