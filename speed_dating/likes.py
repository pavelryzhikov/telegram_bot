#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, json
from flask import Flask, request
from speed_dating import app
#from database import db, db_users, db_groups, db_pairs, db_admin
from copy import deepcopy

TOKEN = app.config['TOKEN']
ADMIN_ID = app.config['ADMIN_ID']
BOT_URL = 'https://api.telegram.org/bot'+TOKEN+'/'
reply_markup_mass = {'0': {
                            'reply_markup': {'inline_keyboard': [[
                {'text':u'\ud83d\udc4d 0','callback_data':'1'},
                {'text':u'\ud83d\udc4e 0','callback_data':'-1'}
                                            ]]
                                            },
                            'count': {} # [+1, -1]
                          }
                    }

def update_reply_markup(message_id, user_id, choice_val):
    message_id = str(message_id)
    user_id = str(user_id)
    try:
        if reply_markup_mass[message_id]:
            pass
    except:
        reply_markup_mass[message_id]=deepcopy(reply_markup_mass['0'])

    #debug('update_reply_markup'+message_id+';'+str(reply_markup_mass[message_id]['count'] ))
    #debug(json.dumps(reply_markup_mass))
#    debug('test')
    #debug(json.dumps(reply_markup_mass))
    reply_markup_mass[message_id]['count'][user_id]=choice_val

#    debug(json.dumps(reply_markup_mass))
    reply_markup_mass[message_id]['reply_markup']['inline_keyboard'][0][0]['text']=u'\ud83d\udc4d' + str(reply_markup_mass[message_id]['count'].values().count('1'))
    reply_markup_mass[message_id]['reply_markup']['inline_keyboard'][0][1]['text']=u'\ud83d\udc4e' + str(reply_markup_mass[message_id]['count'].values().count('-1'))
#    if str(choice_val) == '1':
#        reply_markup_mass[message_id]['reply_markup']['inline_keyboard'][0][0]['text']=u'\ud83d\udc4d' + str(reply_markup_mass[message_id]['count']['+1']+1)
#        reply_markup_mass[message_id]['count']['+1']= reply_markup_mass[message_id]['count']['+1']+1
#    else:
#        reply_markup_mass[message_id]['reply_markup']['inline_keyboard'][0][1]['text']=u'\ud83d\udc4e' + str(reply_markup_mass[message_id]['count']['-1']+1)
#        reply_markup_mass[message_id]['count']['-1'] = reply_markup_mass[message_id]['count']['-1']+1

#    debug(json.dumps(reply_markup_mass))
    return reply_markup_mass[message_id]['reply_markup']

def debug(text, chat_id=ADMIN_ID):
    data = {"chat_id": chat_id,
        "text": text}
    requests.get(BOT_URL+'sendMessage',data = data)

def answerCallbackQuery(callback_query_id, text,show_alert=False):
    data = {"callback_query_id": callback_query_id,
        "text": text,
        "show_alert": show_alert}
    requests.get(BOT_URL+'answerCallbackQuery',data = data)

def editMessageReplyMarkup(chat_id, message_id,user_id, choice_val):
    #debug('editMessageReplyMarkup')
    data = {"chat_id": chat_id,
        "message_id": message_id,
        "reply_markup": json.dumps(update_reply_markup(message_id, user_id, choice_val))}

    #debug(json.dumps(data))
    requests.get(BOT_URL+'editMessageReplyMarkup',data = data)


