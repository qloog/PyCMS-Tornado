#!/usr/bin/env python
#-*- coding:utf-8 -*-

from datetime import datetime
from libs import Base, db_session
from utils import encrypt, obj2dict
from sqlalchemy import Column, Integer, String, DateTime, Boolean, desc, asc
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


class Admin(Base):

    __tablename__ = 'wmh_admin'

    user_id = Column(Integer, primary_key=True)
    realname = Column(String(16))
    username = Column(String(16))
    email = Column(String(32))
    password = Column(String(32))
    last_login_time = Column(DateTime)
    last_login_ip = Column(String(16))
    login_times = Column(Integer)
    update_time = Column(DateTime)
    status = Column(Integer)
    role_id = Column(Integer)
    #user_info = relationship('UserInfo', backref='wmh_user')

    def __init__(self, user_id, username, email, realname, role_id=0):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.realname = realname
        self.role_id = role_id

    def __repr__(self):
        return "<Admin('%s')>" % (self.username)

    @classmethod
    def new(cls, username, email, password, realname, role_id):
        """
        add new user
        """
        user = Admin(None, username, email, realname, role_id)
        user.password = encrypt(password) if password else ''
        user.status = 1
        #TODO optimize
        user.last_login_time = '0000-00-00 00:00:00'
        user.last_login_ip = ''
        user.login_times = 0
        user.update_time = '0000-00-00 00:00:00'

        db_session.add(user)
        #只有提交事务了，才可以获取(user.user_id)数据的ID值
        try:
            db_session.commit()
        except:
            db_session.rollback()

        if user.user_id:
            return cls.get(user.user_id)
        return None

    def update_password(self, password):
        password = encrypt(password)
        current_time = datetime.now()
        update_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        update = {
            Admin.password: password,
            Admin.update_time: update_time
        }
        db_session.query(Admin).filter(Admin.user_id == self.user_id).update(update)
        try:
            return db_session.commit()
        except:
            db_session.rollback()

    def get_password(self):
        return db_session.query(Admin).filter(Admin.user_id == self.user_id).first().password

    def update_login_info(self, last_login_ip):
        current_time = datetime.now()
        last_login_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        update = {
            Admin.last_login_time: last_login_time,
            Admin.last_login_ip: last_login_ip,
            Admin.login_times: Admin.login_times + 1
        }
        db_session.query(Admin).filter(Admin.user_id == self.user_id).update(update)
        try:
            return db_session.commit()
        except:
            db_session.rollback()

    def update_email(self, email):
        current_time = datetime.now()
        update_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        update = {
            Admin.email: email,
            Admin.update_time: update_time
        }
        db_session.query(Admin).filter(Admin.user_id == self.user_id).update(update)
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
        item = db_session.query(Admin.user_id, Admin.realname, Admin.email, Admin.username,  Admin.last_login_ip,
                                Admin.login_times, Admin.status).filter(Admin.user_id == user_id).first()
        return item and cls.initialize(item)

    @classmethod
    def get_by_uid(cls, user_id):
        item = db_session.query(Admin).filter(Admin.user_id == user_id).first()
        return item and cls.initialize(item)

    @classmethod
    def get_by_email(cls, email):
        item = db_session.query(Admin).filter(Admin.email == email).first()
        return item and cls.initialize(item)

    @classmethod
    def get_by_username(cls, username):
        item = db_session.query(Admin).filter(Admin.username == username).first()
        return item and cls.initialize(item)

    @classmethod
    def update(cls, user_id=0, username='', email='', password='', realname='', role_id=0):
        update = {}
        if username:
            update['username'] = username
        if email:
            update['email'] = email
        if password:
            update['password'] = password
        if realname:
            update['realname'] = realname
        if role_id:
            update['role_id'] = role_id

        current_time = datetime.now()
        update_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        update['update_time'] = update_time

        try:
            db_session.query(Admin).filter(Admin.user_id == user_id).update(update)
            db_session.commit()
            return True
        except:
            db_session.rollback()
            raise

    @classmethod
    def gets(cls, start=0, limit=20):
        rs = db_session.query(Admin.user_id, Admin.realname, Admin.email, Admin.username,  Admin.last_login_ip,
                              Admin.last_login_time, Admin.login_times, Admin.status).offset(start).limit(limit)
        return [obj2dict(r) for r in rs.all()]

    @classmethod
    def get_count(cls):
        return db_session.query(Admin).count()


class AdminRole(Base):

    __tablename__ = 'wmh_admin_role'

    role_id = Column(Integer, primary_key=True)
    role_name = Column(String(50))
    description = Column(String)
    list_order = Column(Integer)
    status = Column(Integer)

    def __init__(self, role_id, role_name, description, list_order, status):
        self.role_id = role_id
        self.role_name = role_name
        self.description = description
        self.list_order = list_order
        self.status = status

    def __repr__(self):
        return "<AdminRole('%s')>" % self.role_name

    @classmethod
    def initialize(cls, item):
        if not item:
            return None
        role_id = item.role_id
        role_name = item.role_name
        description = item.description
        list_order = item.list_order
        status = item.status
        if not role_id:
            return None
        return cls(role_id, role_name, description, list_order, status)

    @classmethod
    def new(cls, role_name, description, list_order, status):
        """
        add new role
        """
        role = AdminRole(None, role_name, description, list_order, status)

        db_session.add(role)
        try:
            db_session.commit()
            return True
        except:
            db_session.rollback()
            return None

    @classmethod
    def update(cls, role_id, role_name, description, list_order, status):
        update = {}
        if role_name:
            update['role_name'] = role_name
        if description:
            update['description'] = description
        if list_order:
            update['list_order'] = list_order
        if status:
            update['status'] = status

        try:
            db_session.query(AdminRole).filter(AdminRole.role_id == role_id).update(update)
            db_session.commit()
            return True
        except:
            db_session.rollback()
            raise

    @classmethod
    def get(cls, role_id):
        item = db_session.query(AdminRole.role_id, AdminRole.role_name, AdminRole.description, AdminRole.list_order,
                                AdminRole.status).filter(AdminRole.role_id == role_id).first()
        return item and cls.initialize(item)

    @classmethod
    def gets(cls, start=0, limit=20, sort='id', order='asc'):
        return db_session.query(AdminRole.role_id, AdminRole.role_name, AdminRole.description, AdminRole.list_order,
                                AdminRole.status).offset(start).limit(limit).all()

    @classmethod
    def get_count(cls):
        return db_session.query(AdminRole).count()

    @classmethod
    def get_by_rolename(cls, role_name):
        item = db_session.query(AdminRole).filter(AdminRole.role_name == role_name).first()
        return item and cls.initialize(item)

