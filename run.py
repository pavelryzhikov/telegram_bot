#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, json , time,random
from flask import Flask, request

#from flask import Flask, session, redirect, url_for, escape, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config.from_object('config')

TOKEN = app.config['TOKEN'] 
WEBHOOKURL = app.config['WEBHOOKURL'] 
BOT_URL = 'https://api.telegram.org/bot'+TOKEN+'/'


db = SQLAlchemy(app)

#users = []

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    sex = db.Column(db.String(1))



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
    #send_hook( WEBHOOKURL+TOKEN)
    try:
        send_reply(request.data) 
    except:
        pass
    #send_hook()
    #update_params = {"offset": json.loads(request.data)['update_id']+1}
    #requests.get(BOT_URL+'getUpdates',data = update_params)
    #send_hook(WEBHOOKURL+TOKEN)
    return 'OK', 200
    


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
    
    users = []
    l_users = {}
    resp = ['I don''t understand', 'What?', 'WTF you want?', 'check /help']
    v_help =    '/help - this message\n' \
                '/calc - calculator\n' \
                '/currency - het USD and EUR currency\n' \
                '/myid - get my id\n' \
                '/json - show request json\n' \
                '/weather - weather at moscow'
            
    text_mess = json.loads(p_json)

    data = {"chat_id": 41108330, 
                "text": p_json}
    requests.get(BOT_URL+'sendMessage',data = data)

    mess = Response(p_json)
    requests.get(BOT_URL+mess.message_type_dict[mess.message_type],data = mess.data)
     

    if text_mess['message']['text'] == '/help':
        data = {"chat_id": text_mess['message']['chat']['id'], 
                "text": v_help}
        requests.get(BOT_URL+'sendMessage',data = data)
    elif text_mess['message']['text'] == '/start':
        try:
            user = User(id = text_mess['message']['chat']['id'])
            db.session.add(user)
            db.session.commit()
        except:
            pass
        data = {"chat_id": text_mess['message']['chat']['id'], 
                "text": 'hello, ' + str(text_mess['message']['from']['first_name'])}
        requests.get(BOT_URL+'sendMessage',data = data)
    elif text_mess['message']['text'] == '/calc':
        data = {"chat_id": text_mess['message']['chat']['id'], 
                "text": '2X2=5'}
        requests.get(BOT_URL+'sendMessage',data = data)
    elif text_mess['message']['text'] == '/currency':
        data = {"chat_id": text_mess['message']['chat']['id'], 
                "text": 'USD = 100\nEUR = 100'}
        requests.get(BOT_URL+'sendMessage',data = data)
    elif text_mess['message']['text'] == '/myid':
        data = {"chat_id": text_mess['message']['chat']['id'], 
                "text": text_mess['message']['chat']['id']}
        requests.get(BOT_URL+'sendMessage',data = data)
    elif text_mess['message']['text'] == '/weather':
        data = {"chat_id": text_mess['message']['chat']['id'], 
                "text": '-10 sunny'}
        requests.get(BOT_URL+'sendMessage',data = data)
    elif text_mess['message']['text'] == '/json':
        data = {"chat_id": text_mess['message']['chat']['id'], 
                "text": p_json}
        requests.get(BOT_URL+'sendMessage',data = data)
    elif text_mess['message']['text'] == '/go':

        reply_markup= {'keyboard': [[{"text":"1","request_contact": True}], [{"text":"2", 'request_location': True}]], 'resize_keyboard': True, 'one_time_keyboard': True}
        data = {"chat_id": text_mess['message']['chat']['id'], 
                #"reply_to_message_id": text_mess['message']['message_id'],
                "text": 'send me info',
                "reply_markup": json.dumps(reply_markup) }
        requests.get(BOT_URL+'sendMessage',data = data)
    elif text_mess['message']['text'] == '/users':
        users = User.query.all()
        for u1 in users:
            l_users[u1.id] = u1.sex
        data = {"chat_id": text_mess['message']['chat']['id'], 
                "text": json.dumps(l_users)}
        requests.get(BOT_URL+'sendMessage',data = data)
    elif text_mess['message']['text'] == '/add':
        pass

    elif text_mess['message']['text'] == 'test':
        data = {"chat_id": text_mess['message']['chat']['id'], 
                "text": str(text_mess['message']['chat']['id']) + 'qq'}
        requests.get(BOT_URL+'sendMessage',data = data)
    else:
        try:
            resp.append('сам '.decode('utf-8')+ text_mess['message']['text'])
        except: 
            pass
        data = {"chat_id": text_mess['message']['chat']['id'], 
                "text": random.choice(resp)}
        requests.get(BOT_URL+'sendMessage',data = data)



#        return render_template("main_page.html", comments=Comment.query.all())

        #return render_template("main_page.html", comments=comments)
#    comment = Comment(content=request.form["contents"])
#    db.session.add(comment)
#    db.session.commit()
    #comments.append(request.form["contents"])
#    return redirect(url_for('index')

class Response(object):

    message_type_dict = {
                'text': 'sendMessage',
                'voice': 'sendVoice',
                'contact': 'sendContact',
                'location': 'sendLocation',
                'sticker': 'sendSticker',
                'audio': 'sendAudio',
                'video': 'sendVideo',
                'document': 'sendDocument',
                'photo': 'sendPhoto'
    }
    
    def __init__(self, p_json):
        self.massive = json.loads(p_json)
        self.chat_id = self.massive['message']['chat']['id']
        self.get_message_item()

    def get_message_item(self):
            
        for mess_type in self.message_type_dict.keys():
            if mess_type in self.massive['message'].keys():
                self.message_type = mess_type
                if self.message_type in ['text'] :
                    self.item = self.massive['message'][self.message_type]
                elif self.message_type == 'photo':
                    self.item = self.massive['message'][self.message_type][2]['file_id']
                elif self.message_type == 'location':
                    self.data = {   'chat_id': self.chat_id, 
                                'latitude': self.massive['message'][self.message_type]['latitude'],
                                'longitude': self.massive['message'][self.message_type]['longitude']
                            }
                    return
                elif self.message_type == 'contact':
                
                    self.data = {   'chat_id': self.chat_id, 
                            'phone_number': self.massive['message'][self.message_type]['phone_number'],
                            'first_name': self.massive['message'][self.message_type]['first_name']
                        }
                    return
                else:
                    self.item = self.massive['message'][self.message_type]['file_id']
    
        self.data = {   'chat_id': self.chat_id, 
                            self.message_type: self.item
                     }
    
    
    
    
    def wtf(self):
        if self.message_type == 'location':
            self.data = {   'chat_id': self.chat_id, 
                            'latitude': self.massive['message'][self.message_type]['latitude'],
                            'longitude': self.massive['message'][self.message_type]['longitude']
                        }
        elif self.message_type == 'contact':
            self.data = {   'chat_id': self.chat_id, 
                            'phone_number': self.massive['message'][self.message_type]['phone_number'],
                            'first_name': self.massive['message'][self.message_type]['first_name']
                        }
        else:
            self.data = {   'chat_id': self.chat_id, 
                            self.message_type: self.item
                        }

