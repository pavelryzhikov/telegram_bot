#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from flask import Flask, request
from speed_dating import app
from controller import send_reply, ping, debug

TOKEN = app.config['TOKEN']
WEBHOOKURL = app.config['WEBHOOKURL']
BOT_URL = 'https://api.telegram.org/bot'+TOKEN+'/'
#BOT_NAME = app.config['BOT_NAME']


@app.route('/')
def hello_world():
    return 'ok', 200

@app.route('/token')
def token():
    return TOKEN


@app.route('/updates')
def updates():
    return getUpdates()


@app.route('/'+TOKEN, methods=['POST'])
def get_message():
    try:
        #debug(request.data)
        send_reply(request.data)
    except:
        pass
    return 'OK', 200


@app.route('/hook', methods=['GET', 'POST'])
def init_hook():
    req = send_hook(WEBHOOKURL+TOKEN)
    return req


def send_hook(p_url = ''):
    url = BOT_URL+'setWebhook'
    data = {'url': p_url}
    r = requests.post(url, data=data)
    if r.status_code != 200:
        return 'bad'
    else:
        return 'ok'


#def __print__(p_json):
#    print json.dumps(p_json,indent=4,separators=(',',': '))



