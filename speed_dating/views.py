#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, json , time,random
from flask import Flask, request

#from flask import Flask, session, redirect, url_for, escape, request, render_template
#from flask.ext.sqlalchemy import SQLAlchemy

from speed_dating import app
#app = Flask(__name__)
#app.config.from_object('config')

#from model import db, db_users, db_groups, db_pairs

TOKEN = app.config['TOKEN']
WEBHOOKURL = app.config['WEBHOOKURL']
BOT_URL = 'https://api.telegram.org/bot'+TOKEN+'/'
#BOT_NAME = app.config['BOT_NAME']

# custom const

#db = SQLAlchemy(app)
from database import db, db_users, db_groups, db_pairs, db_admin
from controller import send_reply

#CONST_MIN_NATURALS = app.config['CONST_MIN_NATURALS']
#CONST_MIN_BROS = app.config['CONST_MIN_BROS']
#ADMIN_ID = app.config['ADMIN_ID']
#HELP_MSG = app.config['HELP_MSG']



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



