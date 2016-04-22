#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, json , time
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
def get_webhook1():
    pass
    send_hook( WEBHOOKURL+TOKEN)
    session = requests.Session()
    respons(chat_id = json.loads(request.data)['message']['chat']['id'], text = 'сам '.decode('utf-8')+json.loads(request.data)['message']['text'], session=session)
    send_hook()
    update_params = {"offset": json.loads(request.data)['update_id']+1}
    r = session.get(BOT_URL+'getUpdates',data = update_params)
    send_hook(WEBHOOKURL+TOKEN)

    


@app.route('/hook', methods=['GET', 'POST'])
def hook():
    url = BOT_URL+'setWebhook'
    #data = {'url': WEBHOOKURL+TOKEN, 'certificate': open('YOURPUBLIC.pem', 'rb')}
    data = {'url': WEBHOOKURL+TOKEN}
    r = requests.post(url, data=data)
    if r.status_code != 200:
        return 'bad'
    else: 
        return 'ok'


def send_hook(p_url = ''):
    url = BOT_URL+'setWebhook'
    #data = {'url': WEBHOOKURL+TOKEN, 'certificate': open('YOURPUBLIC.pem', 'rb')}
    data = {'url': p_url}
    r = requests.post(url, data=data)
    if r.status_code != 200:
        return 'bad'
    else: 
        return 'ok'


class User(object):
    def __init__(self,id,username):
        self.id = id
        self.username = username

class Result(object):
    #messages=[]
    #update_id = 0
    def __init__(self,ok):
        self.ok = ok
        self.messages = []
        self.update_id = 0
    #def __call__(self):
    #    self.messages = []
    #    self.update_id = 0
    #    self.ok = None
    def message_add(self,message): 
        self.messages.append(message)
        self.update_id = max(message.update_id, self.update_id)

class Message(object):
    def __init__(self,update_id,message_id,date,text, p_from = None, chat=None):
        self.update_id = update_id
        self.message_id = message_id
        self.date = date
        self.text = text
        self.p_from = p_from
        self.chat = chat


def getUpdates():
    offset = 0

    session = requests.Session()
    request = session.get(BOT_URL+'getUpdates')
    p_json = json.loads(request.content)
    result = Result(p_json['ok'])
    #print self.json    
    for i in p_json['result']:
        result.message_add(Message( update_id = i['update_id'],
                                        message_id = i['message']['message_id'],
                                        date = i['message']['date'],
                                        text = i['message']['text'] if 'text' in i['message'].keys() else '',
                                        p_from = i['message']['from']['id'],
                                        chat = i['message']['chat']['id']
                                    ))
    __print__(p_json)
    reply(result,session)
    if result.update_id != 0:
        offset = result.update_id+1
        update_params = {"offset": offset}
        request = session.get(BOT_URL+'getUpdates',data = update_params)
    return json.dumps(p_json,indent=4,separators=(',',': '))

    #session.close()
    #result.__call__()


def __print__(p_json):
    print json.dumps(p_json,indent=4,separators=(',',': '))
    
def respons(chat_id,text,session):
    body = {"chat_id": chat_id, "text": text}
    response = session.get(BOT_URL+'sendMessage',data = body)

def reply(result,session):
    for message in result.messages:
        if message.text == 'ping':
            respons(chat_id = message.chat, text = 'pong',session=session)
        if message.text == '/help':
            respons(chat_id = message.chat, text = 'sos',session=session)

#while True:
#    getUpdates()            
#    time.sleep(5)


