#!/usr/bin/env python
#-*- coding:utf-8 -*-

from datetime import datetime
from libs import Base, db_session
from utils import encrypt
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


class User(Base):
    __tablename__ = 'wmh_user'
    user_id = Column(Integer, primary_key=True)
    realname = Column(String(16))
    username = Column(String(16))
    email = Column(String(32))
    password = Column(String(32))
    reg_ip = Column(String(16))
    last_login_time = Column(DateTime)
    last_login_ip = Column(String(16))
    login_times = Column(Integer)
    update_time = Column(DateTime)
    #user_info = relationship('UserInfo', backref='wmh_user')

    def __init__(self, user_id, username, email, realname):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.realname = realname

    def __repr__(self):
        return "<User('%s')>" % (self.username)

    @classmethod
    def new(cls, username, email, password, reg_ip):
        """
        add new user
        """
        user = User(None, username, email)
        user.password = encrypt(password) if password else ''
        user.reg_ip = reg_ip
        db_session.add(user)
        #只有提交事务了，才可以获取(user.user_id)数据的ID值
        try:
            db_session.commit()
        except:
            db_session.rollback()
        db_session.close()

        if user.user_id:
            return cls.get(user.user_id)
        return None

    def update_password(self, password):
        password = encrypt(password)
        current_time = datetime.now()
        update_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        update = {
            User.password: password,
            User.update_time: update_time
        }
        db_session.query(User).filter(User.user_id == self.user_id).update(update)
        try:
            return db_session.commit()
        except:
            db_session.rollback()

    def get_password(self):
        return db_session.query(User).filter(User.user_id == self.user_id).first().password

    def update_login_info(self, last_login_ip):
        current_time = datetime.now()
        last_login_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        update = {
            User.last_login_time: last_login_time,
            User.last_login_ip: last_login_ip,
            User.login_times: User.login_times + 1
        }
        db_session.query(User).filter(User.user_id == self.user_id).update(update)
        try:
            return db_session.commit()
        except:
            db_session.rollback()

    def update_email(self, email):
        current_time = datetime.now()
        update_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        update = {
            User.email: email,
            User.update_time: update_time
        }
        db_session.query(User).filter(User.user_id == self.user_id).update(update)
        try:
            return db_session.commit()
        except:
            db_session.rollback()

    @classmethod
    def initialize(cls, item):
        if not item:
            return None
        user_id = item.user_id
        username = item.username
        email = item.email
        realname = item.realname
        if not user_id:
            return None
        return cls(user_id, username, email, realname)

    @classmethod
    def get(cls, user_id):
        item = db_session.query(User).filter(User.user_id == user_id).first()
        return item and cls.initialize(item)

    @classmethod
    def get_by_uid(cls, user_id):
        item = db_session.query(User).filter(User.user_id == user_id).first()
        return item and cls.initialize(item)

    @classmethod
    def get_by_email(cls, email):
        item = db_session.query(User).filter(User.email == email).first()
        return item and cls.initialize(item)

    @classmethod
    def get_by_username(cls, username):
        item = db_session.query(User).filter(User.username == username).first()
        return item and cls.initialize(item)

    def update(self, username='', email='', realname='', about_me='', avatar_src=''):
        update = {}
        update_info = {}
        if username:
            update['username'] = username
        if email:
            update['email'] = email
        if realname:
            update['realname'] = realname

        current_time = datetime.now()
        update_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        update['update_time'] = update_time

        if about_me:
            update_info['about_me'] = about_me
        if avatar_src:
            update_info['avatar_src'] = avatar_src

        try:
            db_session.query(User).filter(User.user_id == self.user_id).update(update)
            #if update_info['about_me'] or update_info['avatar_src']:
            #    db_session.query(UserInfo).filter(UserInfo.user_id == self.user_id).update(update_info)

            db_session.commit()
        except:
            db_session.rollback()
            raise


class UserInfo(Base):

    __tablename__ = 'wmh_user_extinfo'

    id = Column(Integer, primary_key=True)
    #user_id = Column(Integer, ForeignKey('wmh_user.user_id'))
    user_id = Column(Integer)
    gender = Column(Integer)
    birthday = Column(DateTime)
    about_me = Column(String(500))
    #avatar_src = Column(String(255))

    def __init__(self, user_id, gender, birthday, about_me):
        self.user_id = user_id
        self.gender = gender
        self.birthday = birthday
        self.about_me = about_me
        #self.avatar_src = avatar_src

    def __repr__(self):
        return "<UserInfo(gender=%s, birthday=%s)>" % (self.gender, self.birthday)

    @classmethod
    def initialize(cls, item):
        if not item:
            return None
        user_id = item.user_id
        gender = item.gender
        birthday = item.birthday
        about_me = item.about_me
        #avatar_src = item.avatar_src
        if not user_id:
            return None
        return cls(user_id, gender, birthday, about_me )

    @classmethod
    def get_info_by_uid(cls, user_id):
        item = db_session.query(UserInfo).filter(UserInfo.user_id==user_id).first()
        return item and cls.initialize(item)
