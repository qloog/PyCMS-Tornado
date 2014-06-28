#!/usr/bin/env python
#-*- coding: utf-8 -*-

import tornado.web
from tornado.escape import json_encode
from utils import encrypt
from handlers.admin import BaseHandler
from model.admin import Admin as User


class AdminLoginHandler(BaseHandler):

    error_message = {
        '110': '填写信息不完整',
        '121': '该用户不存在',
        '122': '密码错误'
    }

    def get(self):
        self.render('admin/login.html', error=None, email='')

    def post(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')

        self.set_header("Content-Type", "application/json")

        if not (username and password):
            ret = {'error': 110, 'msg': self.error_message['110'], 'url': '/admin/index'}
            return self.write(json_encode(ret))

        user = User.get_by_username(username)
        if not user:
            ret = {'error': 121, 'msg': self.error_message['121']}
            return self.write(json_encode(ret))

        if user.get_password() != encrypt(password):
            ret = {'error': 122, 'msg': self.error_message['122']}
            return self.write(json_encode(ret))

        self.set_secure_cookie("admin_user_id", str(user.user_id), expires_days=7)
        ret = {'error': 0, 'msg': '登录成功', 'url': '/admin/index'}
        return self.write(json_encode(ret))


class AdminLogoutHandler(tornado.web.RequestHandler):

    def get(self):
        self.clear_cookie('admin_user_id')
        self.redirect('/admin/login')
