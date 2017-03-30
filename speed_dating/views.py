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
BOT_NAME = app.config['BOT_NAME']

# custom const

#db = SQLAlchemy(app)
from speed_dating.database import db, db_users, db_groups, db_pairs, db_admin

CONST_MIN_NATURALS = app.config['CONST_MIN_NATURALS']
CONST_MIN_BROS = app.config['CONST_MIN_BROS']
ADMIN_ID = app.config['ADMIN_ID']
HELP_MSG = app.config['HELP_MSG']



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

def send_reply(p_json):
    
    import datetime

    parcel = Parcel(p_json)
    user = User_info(parcel.user_id,parcel.user_name)
    sender = Sender(user.id)



    if parcel.text is not None:
        if parcel.text == '/start':

            if db_users.query.get(user.id) is None:
                sender.reply_text( 'try to subscribe')
                new_user = db_users(id = user.id, nick = user.nick)
                db.session.add(new_user)
                db.session.commit()
                sender.reply_text( 'successfully subscribed')
            else:
                pass
            sender.reply_text( 'hello, %s'%(user.nick))
            sender.reply_text(HELP_MSG)
            fill_form(user, parcel)
            return

        else:

            if db_users.query.get(user.id) is None:
                sender.reply_text( 'try /start')
                return
    else:

        if db_users.query.get(user.id) is None:
            sender.reply_text( 'try /start')
            return


    if user.id == ADMIN_ID:
        admin = admin_params() 

        # admin commands
        if parcel.text == '/admin_info':
            sender.reply_text(admin)
            return 
        elif parcel.text == '/spam on':
            row_admin = db_admin.query.get('SPAM')
            row_admin.status = 'Y'
            db.session.commit()
            return 
        elif parcel.text == '/spam off':
            row_admin = db_admin.query.get('SPAM')
            row_admin.status = 'N'
            db.session.commit()
            return 
        elif parcel.text == '/get_my_id':
            sender.reply_text('id=%s'%(user.id))
            return  
        elif parcel.text == '/friend on':
            row_admin = db_admin.query.get('FRIEND')
            row_admin.status = 'Y'
            row_admin.f_number = None
            db.session.commit()
            return  
        elif parcel.text == '/friend off':
            row_admin = db_admin.query.get('FRIEND')
            row_admin.status = 'N'
            row_admin.f_number = None
            db.session.commit()
            return  
        elif parcel.text == '/group on':
            row_admin = db_admin.query.get('GROUP')
            row_admin.status = 'Y'
            row_admin.f_string = None
            db.session.commit()
            return  
        elif parcel.text == '/group off':
            row_admin = db_admin.query.get('GROUP')
            row_admin.status = 'N'
            row_admin.f_string = None
            db.session.commit()
            return  
        else: 
            pass
       
        # check admin flags       
        if admin.spam == 'Y':
            cursor_users = db_users.query.all()
            for c_user in cursor_users:
                resender = Sender(c_user.id)
                resender.resender(parcel)
            return
        elif admin.friend == 'Y':
            if admin.friend_id is None:
                row_admin = db_admin.query.get('FRIEND')
                #row_admin.status = 'Y'
                row_admin.f_number = parcel.text
                db.session.commit()
            else:
                resender = Sender(admin.friend_id)
                resender.resender(parcel)
            
            return
        elif admin.group == 'Y':
            if admin.group_id is None:
                row_admin = db_admin.query.get('FRIEND')
                #row_admin.status = 'Y'
                row_admin.f_string = parcel.text
                db.session.commit()
            else:
                cursor_groups = db_groups.query.filter_by(group = admin.group_id)
                for c_row_group in cursor_groups:
                    resender = Sender(c_row_group.user_id)
                    resender.resender(parcel)
            
            return
        else:
            pass
            #sender.reply_text( 'not admin')
            

    wait_count = -1
    
    if user.interactive == 'Y':
        row_user = db_users.query.get(user.id)
        row_user.interactive = None
        db.session.commit()
        debug_resender = Sender(ADMIN_ID)
        parcel.data['text'] = '#wish id:%d '%(user.id) + parcel.data['text']
        debug_resender.resender(parcel)
        sender.reply_text( 'Your message:\n'+parcel.data['text']+'\ndelivered to ADMIN successfully')
        return

    if fill_form(user, parcel)==False:
        pass
    else:
        #sender.reply_text( 'try /form')
        return #fill form in process

    if parcel.text is not None:
        if parcel.text == '/help':
            sender.reply_text(HELP_MSG)
#        elif parcel.text == '/start':
#
#            if db_users.query.get(user.id) is None:
#                sender.reply_text( 'try to subscribe')
#                new_user = db_users(id = user.id, nick = user.nick)
#                db.session.add(new_user)
#                db.session.commit()
#                sender.reply_text( 'successfully subscribed')
#            else:
#                pass
#            sender.reply_text( 'hello, %s'%(user.nick))
#            sender.reply_text(HELP_MSG)
#            fill_form(user, parcel)
#            return

        elif parcel.text == '/stop':
            user_row = db_users.query.get(user.id)
            if user_row is not None:
                group_row = db_groups.query.get(user.id)
                if group_row is not None:
                    if group_row.group is None:
                        db.session.delete(group_row)
                        db.session.delete(user_row)
                    else:
                        sender.reply_text( 'first /leave game')
                        return #cant del. in_game = 'Y'

                else:
                    db.session.delete(user_row)
            else:
                sender.reply_text( 'You are already deleted. first /start')
                return

            db.session.commit()
            sender.reply_text( 'Bye ' + str(user.nick))

        elif parcel.text == '/form':
            if not db_users.query.get(user.id) is None:
                row_user = db_users.query.get(user.id)
                row_user.is_bro = None
                row_user.gender = None
                db.session.commit()
            fill_form(user, parcel)
            return
        elif parcel.text == '/join':
            #sender.reply_text('ok, i got it')
            try:
                if db_groups.query.get(user.id) is None:
                    #sender.reply_text('try 1')
                    row_user = db_users.query.get(user.id)
                    row_group = db_groups(user_id = user.id, gender = row_user.gender, is_bro = row_user.is_bro,date_start = datetime.datetime.now() )
                    db.session.add(row_group)
                    db.session.commit()
                    sender.reply_text('you successfully added to waiting list')
                else:
                    sender.reply_text( 'try /count')
                    return

            except:
                sender.reply_text('error')
                db.session.rollback()

            try:
                wait_count = groups_count(user)
            except:
                pass

            if wait_count == 0:
                create_group(user)
                next_round(user)
                #sender.reply_text('you successfully added to group')
            else:
                sender.reply_text('try /count')

        elif parcel.text == '/leave':
            try:
                row_group = db_groups.query.get(user.id)
                if not row_group is None:
                    if row_group.group is None:
                        db.session.delete(row_group)
                        db.session.commit()
                        sender.reply_text('you successfully leaved from waiting list')
                    else:
                        sender.reply_text('you are in game. try /next')
                        #bad_request(sender)
                else:
                    sender.reply_text('you are not in group. try /join')
            except:
                db.session.rollback()
            groups_count(user)
        elif parcel.text == '/count':
            groups_count(user)
        elif parcel.text == '/next':
            next_round(user)
        elif '/wish' in parcel.text:
            row_user = db_users.query.get(user.id)
            row_user.interactive = 'Y'
            db.session.commit()
            sender.reply_text('please, type your message:')
        else:
            if user.in_game =='Y':
                resender = Sender(user.friend_id)
                resender.resender(parcel)
            else:
                sender.reply_text('you will not hear. try /join')
            debug_resender = Sender(ADMIN_ID)
            debug_resender.reply_text('id:%d'%(user.id))
            debug_resender.resender(parcel)

    if parcel.text is None:
        if user.in_game =='Y':
            resender = Sender(user.friend_id)
            resender.resender(parcel)
        else:
            sender.reply_text('you will not hear. try /join')
        debug_resender = Sender(ADMIN_ID)
        debug_resender.reply_text('id:%d'%(user.id))
        debug_resender.resender(parcel)



def admin_console(command):
    pass

class admin_params(object):
    def __init__(self):
        cursor_admin = db_admin.query.all()
        self.spam = None 
        self.friend = None
        self.friend_id = None
        self.group = None
        self.group_id = None
        for key in cursor_admin:
            if key.item == 'SPAM':
                self.spam = key.status
            elif key.item == 'FRIEND':
                self.friend = key.status
                self.friend_id = key.f_number
            elif key.item == 'GROUP':
                self.group = key.status
                self.group_id = key.f_string
            else:
                pass
       
    def __str__(self):
        return 'spam=%r \n friend=%r \n friend_id=%r \n group=%r \n group_id=%r' % (self.spam, 
                                                                            self.friend, 
                                                                            self.friend_id,
                                                                            self.group,
                                                                            self.group_id)

def bad_request(sender):
    sender.reply_text('bad request')

def fill_form(user,  parcel):
    sender = Sender(user.id)
    #sender.reply_text('check info')
    if not db_users.query.get(user.id) is None:
        #sender.reply_text('1')
        row_user = db_users.query.get(user.id)
        #sender.reply_text('2')
    else:
        sender.reply_text('try /start. you are not subscribed')
        #sender.reply_text('3')
        return
    last_question = None
    curr_question = None
    if row_user.gender is None:
        if parcel.is_callback == 'Y':
            if parcel.text in ['M','W']:
                row_user.gender = parcel.text
                db.session.commit()
                parcel.is_callback = 'N' #unset
                # send next Q
            else:
                curr_question = 'Y'
        else:
            curr_question = 'Y'

        if curr_question == 'Y':

            reply_markup= {'inline_keyboard': [[{'text':'I''m a BOY','callback_data':'M'}], [{'text':'I''m a GIRL','callback_data':'W'}]]}
            #reply_markup= {'inline_keyboard': [[['text':'gogo','callback_data':'hello']], [['text':'hello','callback_data':'hello']]]}
            sender.set_reply_markup(reply_markup)
            sender.reply_text('Please choose your gender')
            return
    else:
        pass #send next Q

    curr_question = None
    if row_user.is_bro is None:
        if parcel.is_callback == 'Y':
            if parcel.text in ['M','W']:
                if parcel.text == row_user.gender:
                    row_user.is_bro = 'Y'
                else:
                    row_user.is_bro = 'N'
                db.session.commit()
                parcel.is_callback = 'N' #unset
                # send next Q
                last_question = 'Y' # send last question
            else:
                curr_question = 'Y'
        else:
            curr_question = 'Y'

        if curr_question == 'Y':

            reply_markup= {'inline_keyboard': [[{'text':'BOYS','callback_data':'M'}], [{'text':'GIRLS','callback_data':'W'}]]}
            #reply_markup= {'inline_keyboard': [[['text':'gogo','callback_data':'hello']], [['text':'hello','callback_data':'hello']]]}
            sender.set_reply_markup(reply_markup)
            sender.reply_text('Who are you looking for?')
            return


    if parcel.is_callback == 'Y':
        if parcel.text == 'Y':
            row_user.nick = None
            db.session.commit()
            sender.reply_text('Ok, send your nick to me')
            return
        else:
            sender.reply_text('Ok, %s. Done. try /join'%(row_user.nick))
            return
    else:
        if row_user.nick is None:
            row_user.nick = parcel.text
            db.session.commit()
            sender.reply_text('Ok, %s. Done. try /join'%(row_user.nick))
            return
        else:
            if last_question =='Y':
                reply_markup= {'inline_keyboard': [[{'text':'YES','callback_data':'Y'}], [{'text':'NO','callback_data':'N'}]]}
                #reply_markup= {'inline_keyboard': [[['text':'gogo','callback_data':'hello']], [['text':'hello','callback_data':'hello']]]}
                sender.set_reply_markup(reply_markup)
                sender.reply_text('Do you want change your nick? \n Current %s'%(user.nick))
                return
    return False


def groups_count(user):

    sender = Sender(user.id)
    men_count, women_count, bro_count = None, None, None

    row_user = db_users.query.get(user.id)
    if db_groups.query.get(user.id) is None:
        sender.reply_text('first /join')
        return -1
    if row_user.is_bro == 'Y':
        bro_count = db_groups.query.filter_by(gender = row_user.gender, is_bro = 'Y', status = 'W').count()
        bro_count = 0 if bro_count >= CONST_MIN_BROS else CONST_MIN_BROS - bro_count
        sender.reply_text( 'we need %r bros' % (bro_count))
    else:
        men_count = db_groups.query.filter_by(gender = 'M', is_bro = 'N', status = 'W').count()
        women_count = db_groups.query.filter_by(gender = 'W', is_bro = 'N', status = 'W').count()
        men_count = 0 if men_count >= CONST_MIN_NATURALS else CONST_MIN_NATURALS - men_count
        women_count = 0 if women_count >= CONST_MIN_NATURALS else CONST_MIN_NATURALS - women_count
        sender.reply_text('we need %r girls and %r boys' % (women_count, men_count))

    if (men_count == 0 and women_count == 0) or (bro_count  == 0):
        return 0
    else:
        return -1

def create_group_auto():
    import uuid, datetime
    while True:
        cur_group = db.session.query(db_groups).filter(db_groups.status == 'W',db_groups.date_start < datetime.datetime.now()-datetime.timedelta(minutes=5)).limit(CONST_MIN_BROS) 
        if cur_group.count() < CONST_MIN_BROS:
            break

        bros = []
        #row_group = db_groups.query.get(user.id)
        group_id = str(uuid.uuid1())
        for c_row_group in cur_group:
            bros.append(c_row_group.user_id)
            c_row_group.status = 'A'
            c_row_group.group = group_id
            #c_row_group.date_start = datetime.datetime.now()
        db.session.commit()

        users = bro_pairs(bros)


        while True:
            try:
                pairs = users.next()
                for pair in pairs:
                    row_pair = db_pairs(group_id = group_id, iterator = pair[0], user1=pair[1],user2=pair[2])
                    db.session.add(row_pair)
                    db.session.commit()
            except:
                break





def create_group(user):
    import uuid, datetime
    sender = Sender(user.id)
    # set group id
    bros = []
    girls = []
    boys = []
    row_group = db_groups.query.get(user.id)
    group_id = str(uuid.uuid1())
    if row_group.is_bro == 'Y':
        cursor_groups = db_groups.query.filter_by(status = 'W',is_bro = 'Y', gender = row_group.gender).limit(CONST_MIN_BROS)
        for c_row_group in cursor_groups:
            bros.append(c_row_group.user_id)
            c_row_group.status = 'A'
            c_row_group.group = group_id
            #c_row_group.date_start = datetime.datetime.now()
        db.session.commit()
    else:
        cursor_groups = db_groups.query.filter_by(status = 'W',is_bro = 'N', gender = 'M').limit(CONST_MIN_NATURALS)
        for c_row_group in cursor_groups:
            boys.append(c_row_group.user_id)
            c_row_group.status = 'A'
            c_row_group.group = group_id
            #c_row_group.date_start = datetime.datetime.now()
        db.session.commit()
        cursor_groups = db_groups.query.filter_by(status = 'W',is_bro = 'N', gender = 'W').limit(CONST_MIN_NATURALS)
        for c_row_group in cursor_groups:
            girls.append(c_row_group.user_id)
            c_row_group.status = 'A'
            c_row_group.group = group_id
            #c_row_group.date_start = datetime.datetime.now()
        db.session.commit()


    # create stack for communication
    if row_group.is_bro == 'Y':
        users = bro_pairs(bros)
#        while True:
#            try:
#                pairs = users.next()
#                for pair in pairs:
#                    row_pair = db_pairs(group_id = group_id, iterator = pair[0], user1=pair[1],user2=pair[2])
#                    db.session.add(row_pair)
#                    db.session.commit()
#            except:
#                break
    else:
        users = love_pairs(boys,girls)

    while True:
        try:
            pairs = users.next()
            for pair in pairs:
                row_pair = db_pairs(group_id = group_id, iterator = pair[0], user1=pair[1],user2=pair[2])
                db.session.add(row_pair)
                db.session.commit()
        except:
            break

    # set status in_game to started and set friend_id for user
    # or.... its new function


def next_round(user):
    from sqlalchemy import func
    import datetime
    sender = Sender(user.id)

    row_group = db_groups.query.get(user.id)
    if row_group is not None:
        if row_group.status == 'A':
            # check rouund is active

            active_rounds = db_pairs.query.filter(db_pairs.status == 'A',db_pairs.group_id == row_group.group, db_pairs.date_start > datetime.datetime.now()-datetime.timedelta(minutes=5))
            if active_rounds.count() != 0:
                a = ((active_rounds[0].date_start+datetime.timedelta(minutes=5))-datetime.datetime.now()).seconds
                m, s = divmod(a, 60)
                sender.reply_text("Wait for %02d:%02d" % (m, s))
                return

            current_round = db.session.query(func.min(db_pairs.iterator)).filter_by(status='W',group_id = row_group.group).scalar()
            if current_round is None:
                # clear info about in_game status
                cursor_pairs = db_pairs.query.filter_by(group_id = row_group.group)
                for c_row_pair in cursor_pairs:
                    c_row_pair.status = 'C'

                cursor_group = db_groups.query.filter_by(group = row_group.group)
                for c_row_group in cursor_group:
                    #c_row_group.status = 'C'
                    row_user = db_users.query.get(c_row_group.user_id)
                    row_user.in_game = None
                    row_user.friend_id = None
                    spam = Sender(row_user.id)
                    spam.reply_text('GAME OVER!!! \nGood Luck!!!\n...and send /join to try again')
                    db.session.delete(c_row_group)
                db.session.commit()
                return

        else:
            sender.reply_text('not now')
            return

            #cursor_groups = db_groups.query.filter_by(status = 'W',is_bro = 'N', gender = 'W').limit(CONST_MIN_NATURALS)

    else:
        sender.reply_text('first try /join')
        return

    #sender.reply_text('update users...')
    cursor_pairs = db_pairs.query.filter_by(status = 'W',iterator = current_round, group_id = row_group.group)

    for c_row_pair in cursor_pairs:
        c_row_pair.status = 'A'
        c_row_pair.date_start = datetime.datetime.now()
        # update users
        user1 = db_users.query.get(c_row_pair.user1)
        user2 = db_users.query.get(c_row_pair.user2)
        user1.friend_id = user2.id
        user2.friend_id = user1.id
        user1.in_game = 'Y'
        user2.in_game = 'Y'
        db.session.commit()

        # send info abot start to everybody in group
        user_info1 = User_info(user1.id)
        user_info2 = User_info(user2.id)
        sender1 = Sender(user_info1.id)
        sender2 = Sender(user_info2.id)

        sender1.reply_text('Your new opponent %s.\n Good luck!\n try start from joke or funny sticker'%(user_info2.nick))
        sender2.reply_text('Your new opponent %s.\n Good luck!\n try start from joke or funny sticker'%(user_info1.nick))
        #sender2.reply_text('Your new opponent. ' + str(user_info1.nick) + '\n Good luck!\n try start from joke or funny sticker')


def next_round_auto():
    from sqlalchemy import func
    import datetime
    #rpe_func(1)
    # just active group
    #cur_groups_id = db.session.query(db_pairs.group_id).filter(db_pairs.status == 'A', db_pairs.date_start < datetime.datetime.now()-datetime.timedelta(minutes=4)).distinct() 
    cur_groups_id = db.session.query(db_groups.group).filter(db_groups.status == 'A').distinct()
    for i in cur_groups_id:
        v_group_id = i[0]

        active_rounds = db_pairs.query.filter(db_pairs.status == 'A',db_pairs.group_id == v_group_id, db_pairs.date_start > datetime.datetime.now()-datetime.timedelta(minutes=4))
        if active_rounds.count() != 0:
            continue

        current_round = db.session.query(func.min(db_pairs.iterator)).filter_by(status='W',group_id = v_group_id).scalar()
        if current_round is None:
            # clear info about in_game status
            cursor_pairs = db_pairs.query.filter_by(group_id = v_group_id)
            for c_row_pair in cursor_pairs:
                c_row_pair.status = 'C'

            cursor_group = db_groups.query.filter_by(group = v_group_id)
            for c_row_group in cursor_group:
                #c_row_group.status = 'C'
                row_user = db_users.query.get(c_row_group.user_id)
                row_user.in_game = None
                row_user.friend_id = None
                spam = Sender(row_user.id)
                spam.reply_text('GAME OVER!!! \nGood Luck!!!\n...and send /join to try again')
                db.session.delete(c_row_group)
            db.session.commit()
            continue
    
    
        #rpe_func(2)
        #sender.reply_text('update users...')
        cursor_pairs = db_pairs.query.filter_by(status = 'W',iterator = current_round, group_id = v_group_id)

        for c_row_pair in cursor_pairs:
            c_row_pair.status = 'A'
            c_row_pair.date_start = datetime.datetime.now()
            # update users
            user1 = db_users.query.get(c_row_pair.user1)
            user2 = db_users.query.get(c_row_pair.user2)
            user1.friend_id = user2.id
            user2.friend_id = user1.id
            user1.in_game = 'Y'
            user2.in_game = 'Y'
            db.session.commit()

            # send info abot start to everybody in group
            user_info1 = User_info(user1.id)
            user_info2 = User_info(user2.id)
            sender1 = Sender(user_info1.id)
            sender2 = Sender(user_info2.id)

            sender1.reply_text('Your new opponent %s.\n Good luck!\n try start from joke or funny sticker'%(user_info2.nick))
            sender2.reply_text('Your new opponent %s.\n Good luck!\n try start from joke or funny sticker'%(user_info1.nick))
            #sender2.reply_text('Your new opponent. ' + str(user_info1.nick) + '\n Good luck!\n try start from joke or funny sticker')


def bro_pairs(bros):
    for rounds in range(1,len(bros)):
        users = []
        for i in range(0,len(bros)/2):
            print bros[i], bros[len(bros)-1-i]
            users.append([rounds, bros[i],bros[len(bros)-1-i]])
        to_end = bros[1]
        del bros[1]
        bros.append(to_end)
        yield users

def love_pairs(boys, girls):
    for rounds in range(1,len(boys)+1):
        users = []
        for i in range(0,len(boys)):
            print boys[i], girls[i]
            users.append([rounds, boys[i], girls[i]])
        to_end = girls[0]
        del girls[0]
        girls.append(to_end)
        yield users



def rpe_func(id = None):
    data = {"chat_id": ADMIN_ID,
            "text": 'func()'+str(id)}
    requests.get(BOT_URL+'sendMessage',data = data)


def ping():
    data = {"chat_id": ADMIN_ID,
            "text": 'alive'}
    requests.get(BOT_URL+'sendMessage',data = data)


class User_info(object):
    def __init__(self,id,nick = None):
        self._u = db_users.query.get(id)
        if self._u is None:
            self.id = id
            self.gender = None
            self.is_bro = None
            self.nick = nick
            self.friend_id = None
            self.in_game = None
            self.interactive = None
        else:
            self.id = self._u.id
            self.gender = self._u.gender
            self.is_bro = self._u.is_bro
            self.nick = self._u.nick
            self.friend_id = self._u.friend_id
            self.in_game = self._u.in_game
            self.interactive = self._u.interactive

        if self.nick is None:
            self.nick = 'Stranger'


class Parcel(object):


    def __init__(self, p_json):
        self.data = {}
        self.text = None
        self.json = p_json
        self.massive = json.loads(p_json)
        self.is_callback = 'N'

        if 'callback_query' in self.massive:
            self.chat_id = self.massive['callback_query']['message']['chat']['id']

            self.is_callback = 'Y'
            self.user_id = self.chat_id
            self.item = self.massive['callback_query']['data']
            self.data = {   'chat_id': self.chat_id,
                            'text': self.item
                        }
            self.message_type = 'text'
            self.user_name = self.massive['callback_query']['message']['from']['first_name']
            self.text = self.item
            return

        try:
            self.chat_id = self.massive['message']['chat']['id']
            #self.message_id = self.massive['message']['message_id']
            self.user_name = self.massive['message']['from']['first_name']
            self.user_id = self.chat_id
        except:
            pass
        try:
            self.get_message_item()
        except:
            pass
        #try:
        #    self.reply_to_message = self.massive['message']['reply_to_message']['text']
        #except:
        #    self.reply_to_message = None



    def get_message_item(self):

        for mess_type in Sender.message_type_dict.keys():
            if mess_type in self.massive['message'].keys():
                self.message_type = mess_type
                if self.message_type in ['text'] :
                    self.item = self.massive['message'][self.message_type]
                    self.item = (self.item).replace(BOT_NAME,'')
                    self.text = self.item
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


class Sender(object):


    resp = ['I don''t understand', 'What?', 'WTF you want?', 'check /help']
    #v_help =    '/help - this message\n' \
    #            '/start - magic thing\n' \
    #            '/join - join to waiting group\n' \
    #            '/leave - leave from waiting group\n' \
    #            '/next - i want another lover \n' \
    #            ''

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
    #data = {}
    #header = None

    def __init__(self,user_id):
        self.data = {}
        self.chat_id = user_id
        self.data['chat_id'] = user_id
        self.header = self.message_type_dict['text']

    def send(self):
        requests.get(BOT_URL+self.header, data = self.data)

    def set_header(self, message_type):
        self.header = self.message_type_dict[message_type]


    def reply_text(self,text):
        self.data['text'] = text
        self.send()

    def set_reply_markup(self,reply_markup):
        self.data['reply_markup'] = json.dumps(reply_markup)

    def resender(self,parcel):
        self.data = parcel.data
        self.data['chat_id'] = self.chat_id
        self.header = self.message_type_dict[parcel.message_type]
        self.send()

