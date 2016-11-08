#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from speed_dating import app

db = SQLAlchemy(app)

class db_users(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(1))
    is_bro = db.Column(db.String(1))
    nick = db.Column(db.String(255))
    in_game = db.Column(db.String(1))
    friend_id = db.Column(db.Integer)
    interactive = db.Column(db.String(1))

    def __init__(self, id, gender = None,is_bro = None,nick = None,in_game=None,friend_id = None,interactive = None):
        self.id = id
        self.gender = gender
        self.is_bro = is_bro
        self.nick = nick
        self.in_game = in_game
        self.friend_id = friend_id
        self.interactive = interactive

    def __repr__(self):
        return '<user id=%r,gender=%r,is_bro=%r,nick=%r,in_game=%r,friend_id=%r>' % (self.id, self.gender, self.is_bro,self.nick,self.in_game, self.friend_id)

class db_groups(db.Model):

    __tablename__ = "groups"

    user_id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(36))
    gender = db.Column(db.String(1))
    is_bro = db.Column(db.String(1)) # Bros gotta stick together ;)
    status = db.Column(db.String(1))
    date_start = db.Column(db.DateTime)

    def __init__(self, user_id, gender = None, is_bro=None):
        self.user_id = user_id
        self.group = None
        self.gender = gender
        self.is_bro= is_bro
        self.status = 'W'
        self.date_start = None

    def __repr__(self):
        return '<Groups id=%r,group=%r,gender=%r,is_bro=%r,status=%r,date_start=%r>' % (self.user_id, self.group, self.gender, self.is_bro, self.status, self.date_start)


class db_pairs(db.Model):
    
    __tablename__ = "pairs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True) #groip_id+'#'+iterator
    group_id = db.Column(db.String(36))
    iterator = db.Column(db.Integer)
    user1 = db.Column(db.Integer)
    user2 = db.Column(db.Integer)
    status = db.Column(db.String(1))
    date_start = db.Column(db.DateTime)

    def __init__(self, group_id, iterator,user1,user2,status=None):
        #self.id = group_id+'#'+str(iterator)
        self.group_id = group_id
        self.iterator = iterator
        self.user1=user1
        self.user2=user2
        self.status = 'W'
        self.date_start = None

    def __repr__(self):
        return '<Groups id=%r ,group_id=%r,iterator=%r,user1=%r,user2=%r,status=%r,date_start=%r>' % (self.id, self.group_id, self.iterator,self.user1,self.user2,self.status, self.date_start)



class db_admin(db.Model):
    
    __tablename__ = "admin"

    item = db.Column(db.String(255), primary_key=True) 
    status = db.Column(db.String(1))
    f_number = db.Column(db.Integer)
    f_string = db.Column(db.String(255))
    f_date = db.Column(db.DateTime)

    def __init__(self, item, status=None, f_number=None,f_string=None,f_date=None):
        self.item = item
        self.status = status
        self.f_number=f_number
        self.f_string=f_string
        self.f_date = f_date

#    def __repr__(self):
#        return '<Groups id=%r ,group_id=%r,iterator=%r,user1=%r,user2=%r,status=%r,date_start=%r>' % (self.id, self.group_id, self.iterator,self.user1,self.user2,self.status, self.date_start)











