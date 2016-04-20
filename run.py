#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, json, time
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('CONFIG')
TOKEN = config.get('DEFAULT', 'TOKEN') 

BOT_URL = 'https://api.telegram.org/bot'+TOKEN+'/'

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

while True:
    getUpdates()            
    time.sleep(5)

