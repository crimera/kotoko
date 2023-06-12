import requests, os
from flask import Flask, request
app = Flask(__name__)

pageToken = os.environ['PAGE_TOKEN']
callbackToken = os.environ['CALLBACK_TOKEN']

@app.route('/')
def index():
    return 'Hello from Flask!'

@app.route('/webhook', methods=['GET'])
def webhook():
    verify_token = request.args.get("hub.verify_token")
    # Check if sent token is correct
    if verify_token == callbackToken:
        # Responds with the challenge token from the request
        return request.args.get("hub.challenge")
    return 'Unable to authorise.'

# Adds support for POST requests
@app.route("/webhook", methods=['POST'])
def webhook_handle():
    data = request.get_json()
    message = data['entry'][0]['messaging'][0]['message']['text']
    sender_id = data['entry'][0]['messaging'][0]['sender']['id']
    text = "hi!"
    print(message+"\n"+text)
    request_body = {
            'recipient': {
            'id': sender_id
        },
        'message': {"text":text}
    }
    response = requests.post('https://graph.facebook.com/v5.0/me/messages?access_token='+pageToken,json=request_body).json()
    return response
    return 'ok'

# app.run(port=5000, threaded=True)
