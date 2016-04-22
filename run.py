#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, json , time,random
from flask import Flask, request

app = Flask(__name__)
app.config.from_object('config')

TOKEN = app.config['TOKEN'] 
WEBHOOKURL = app.config['WEBHOOKURL'] 
BOT_URL = 'https://api.telegram.org/bot'+TOKEN+'/'

@app.route('/')
def hello_world():
    return 'hello' 

@app.route('/token')
def token():
    return TOKEN 

@app.route('/updates')
def updates():
    return getUpdates()
    

@app.route('/'+TOKEN, methods=['POST'])
def get_message():
    send_hook( WEBHOOKURL+TOKEN)
    send_reply(request.data) 
    send_hook()
    update_params = {"offset": json.loads(request.data)['update_id']+1}
    requests.get(BOT_URL+'getUpdates',data = update_params)
    send_hook(WEBHOOKURL+TOKEN)

    


@app.route('/hook', methods=['GET', 'POST'])
def init_hook():
    req = send_hook(WEBHOOKURL+TOKEN)
    return req


def send_hook(p_url = ''):
    url = BOT_URL+'setWebhook'
    #data = {'url': WEBHOOKURL+TOKEN, 'certificate': open('YOURPUBLIC.pem', 'rb')}
    data = {'url': p_url}
    r = requests.post(url, data=data)
    if r.status_code != 200:
        return 'bad'
    else: 
        return 'ok'


def __print__(p_json):
    print json.dumps(p_json,indent=4,separators=(',',': '))

def send_reply(p_json):
    
    resp = ['I don''t understand', 'What?', 'WTF you want?', 'check /help']
    v_help =    '/help - this message\n' \
                '/calc - calculator\n' \
                '/currency - het USD and EUR currency\n' \
                '/weather - weather at moscow'
            
    text_mess = json.loads(p_json)
    
    if text_mess['message']['text'] == '/help':
        data = {"chat_id": text_mess['message']['chat']['id'], 
                "text": v_help}
        requests.get(BOT_URL+'sendMessage',data = data)
    elif text_mess['message']['text'] == '/calc':
        data = {"chat_id": text_mess['message']['chat']['id'], 
                "text": '2X2=5'}
        requests.get(BOT_URL+'sendMessage',data = data)
    elif text_mess['message']['text'] == '/currency':
        data = {"chat_id": text_mess['message']['chat']['id'], 
                "text": 'USD = 100\nEUR = 100'}
        requests.get(BOT_URL+'sendMessage',data = data)
    elif text_mess['message']['text'] == '/weather':
        data = {"chat_id": text_mess['message']['chat']['id'], 
                "text": '-10 sunny'}
        requests.get(BOT_URL+'sendMessage',data = data)
    else:
        try:
            resp.append('сам '.decode('utf-8')+ text_mess['message']['text'])
        except: 
            pass
        data = {"chat_id": text_mess['message']['chat']['id'], 
                "text": random.choice(resp)}
        requests.get(BOT_URL+'sendMessage',data = data)


