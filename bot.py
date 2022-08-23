# main body of bot
from flask import Flask
from flask import request
from flask import Response
import requests

import os, yaml # loading configs


def parse_config_path(filename: str):
    return os.path.abspath(os.path.dirname(__file__)) + "/config/" + filename


config = yaml.safe_load(open(parse_config_path('bot_settings.yml')))
TOKEN = config['TOKEN']

app = Flask(__name__)

def tel_parse_message(message):
    print("message-->",message)
    try:
        chat_id = message['message']['chat']['id']
        txt = message['message']['text']
        print("chat_id-->", chat_id)
        print("txt-->", txt)
 
        return chat_id,txt
    except:
        print("NO text found-->>")
 
def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': text
                }
   
    r = requests.post(url,json=payload)
 
    return r
 
def tel_send_image(chat_id, caption: str):
    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
    payload = {
        'chat_id': chat_id,
        'photo': "https://github.com/DoubleSpicy/anya-like-this-bot/blob/main/resources/anya-likes-typhoon8.jpg?raw=true",
        'caption': caption
    }
 
    r = requests.post(url, json=payload)
    return r
 
@ app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        try:
            chat_id, txt = tel_parse_message(msg)
            if txt == "like this":
                # tel_send_message(chat_id,"Hello, world!")
                tel_send_image(chat_id, 'WAKU WAKU!')
        #     elif txt == "image":
        #         tel_send_image(chat_id)
 
        #     else:
        #         tel_send_message(chat_id, 'from webhook')
        except:
            print("fail to parse and send response!")
 
        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"


if __name__ == '__main__':
    print(TOKEN)
    app.run(debug=True ,host="0.0.0.0", threaded=True, port=5000)