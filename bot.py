# main body of bot
from email import message
from flask import Flask
from flask import request
from flask import Response
import requests

import os, yaml # loading configs

import telegram
import logging

from cv_script import produce_output

def parse_config_path(filename: str):
    return os.path.abspath(os.path.dirname(__file__)) + "/config/" + filename


config = yaml.safe_load(open(parse_config_path('bot_settings.yml')))
TOKEN = config['TOKEN']

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)





def tel_parse_message(message):
    print("message-->",message)
    print(type(message))
    try:
        chat_id = message['message']['chat']['id']
        txt = message['message']['text']
        print("chat_id-->", chat_id)
        print("txt-->", txt)
 
        return chat_id,txt
    except:
        print("NO text found-->>")
 
def msgHandler(message):
    # msg['message']['reply_to_message']['photo'][-1]
    chat_id=message['message']['chat']['id']
    if message['message'].get('reply_to_message'):
        if message['message']['reply_to_message'].get('document'):
            if message['message']['reply_to_message']['document']['mime_type'] == 'image/jpeg' or message['message']['reply_to_message']['document']['mime_type'] == 'image/png':
                file_id = message['message']['reply_to_message']['document']['thumb']['file_id']
                url = f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}"
                download_and_process(url, chat_id=chat_id)
        elif message['message']['reply_to_message'].get('photo'):
            file_id = message['message']['reply_to_message']['photo'][-1]['file_id']
            print("file_id-->", file_id)
            # file_id = file_info['file_id']
            url = f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}"
            download_and_process(url, chat_id=chat_id)

def download_and_process(url, chat_id):
    r = requests.get(url)
    if r.status_code == 200:
        # return ok, use file_id and chat id to download the image.
        file_id = r.json()['result']['file_id']
        file_path = r.json()['result']['file_path']
        print(r.json())
        print(file_id, file_path)
        # Download photo
        file_name = os.path.basename(file_path)
        response = requests.get('https://api.telegram.org/file/bot%s/%s' % (TOKEN, file_path))
        dst_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)) + '/temp', 'target.jpg')
        print(dst_file_path)
        with open(dst_file_path, 'wb') as f:
            f.write(response.content)
        print(u"Downloaded file to {}".format(dst_file_path))

        # call openCV to make new output
        produce_output(dst_file_path)
        
        # upload this photo
        send_photo(chat_id=chat_id, image_path='./temp/output.jpg')
        os.remove(dst_file_path)
        os.remove('./temp/output.jpg')

def send_photo(chat_id, image_path, image_caption="WAKU WAKU!"):
    data = {"chat_id": chat_id, "caption": image_caption}
    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={chat_id}'
    with open(image_path, "rb") as image_file:
        ret = requests.post(url, data=data, files={"photo": image_file})
    return ret.json()

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


def get_json(method_name, *args, **kwargs):
    return make_request('get', method_name, *args, **kwargs)

def post_json(method_name, *args, **kwargs):
    return make_request('post', method_name, *args, **kwargs)

def make_request(method, method_name, *args, **kwargs):
    response = getattr(requests, method)(
        'https://api.telegram.org/bot%s/%s' % (TOKEN, method_name),
        *args, **kwargs
    )
    if response.status_code > 200:
        raise DownloadError(response)
    return response.json()

class DownloadError(Exception):
    pass





@ app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        # try:
        chat_id, txt = tel_parse_message(msg)
        # print(msg)
        print('=================')
        print(msg['message']['reply_to_message']['photo'][-1])
        print(txt)
        print('=================')
        if txt == "like this":
            print('triggered!!')
            msgHandler(msg)
        # except Exception as e:
        #     print("fail to parse and send response!")
        #     print(e)
 
        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"


if __name__ == '__main__':
    print(TOKEN)
    app.run(debug=True ,host="0.0.0.0", threaded=True, port=5000)