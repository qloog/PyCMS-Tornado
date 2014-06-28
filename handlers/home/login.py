#!/usr/bin/env python
#-*- coding: utf-8 -*-

import re
import tornado.web
from utils import encrypt
import libs.captcha
from model.user import User
from handlers.home import BaseHandler

class RegisterHandler(BaseHandler):

    error_message = {
        '110': '填写信息不完整',
        '111': '用户名最多15个字符',
        '112': '用户名已经被使用',
        '113': 'Email不正确',
        '114': 'Email已经被使用',
        '115': '注册失败，请稍后再试'
    }

    def get(self):
        self.render('home/register.html', error=None, username='', email='')

    def post(self):
        username = self.get_argument('username', '')
        email = self.get_argument('email', '')
        password = self.get_argument('password', '')

        if not username or len(username) > 15:
            self.render('home/register.html', error=111, username=username, email=email)
            return
        match = re.search(r'[\w.-]+@[\w.-]+', email)
        if not match:
            self.render('home/register.html', error=113, username=username, email=email)
            return
        if not password:
            self.render('home/register.html', error=110, username=username, email=email)
            return

        user = User.get_by_username(username)
        if user:
            self.render('home/register.html', error=112, username=username, email=email)
            return

        user = User.get_by_email(email)
        if user:
            self.render('home/register.html', error=114, username=username, email=email)
            return

        #走代理获取ip方式
        reg_ip = self.request.headers['X-Real-Ip']
        user = User.new(username, email, password, reg_ip)
        if user:
            self.set_secure_cookie('user_id', str(user.user_id), expires_days=30)
            self.redirect(self.get_argument('next', '/'))
        else:
            self.render('home/register.html', error=115)


class LoginHandler(BaseHandler):

    error_message = {
        '100': '信息填写不完整',
        '101': '该用户不存在',
        '102': '密码错误',
        '103': '验证码错误'
    }

    def get(self):
        self.render('home/login.html', error=None, email='')

    def post(self):
        email = self.get_argument('email', '')
        password = self.get_argument('password', '')

        if not (email and password):
            self.render('home/login.html', error=100, email=email)

        user = User.get_by_email(email)
        if not user:
            self.render('home/login.html', error=101, email=email)

        if user.get_password() == encrypt(password):
            last_login_ip = self.request.headers['X-Real-Ip']
            user.update_login_info(last_login_ip)
            self.set_secure_cookie("user_id", str(user.user_id), expires_days=7)
            self.redirect(self.get_argument('next', '/'))
        else:
            self.render('home/login.html', error=102, email=email)

        #获取远程ip
        remote_ip = self.request.headers['X-Real-Ip']
        challenge = self.get_argument('recaptcha_challenge_field', None)
        response =  self.get_argument('recaptcha_response_field', None)
        rsp = captcha.check_google_captcha(self,remote_ip, challenge, response)
        if not rsp.is_valid:
            self.render('home/login.html', error=103, email=email)

        self.render('home/login.html', error=100, email=email)


class LogoutHandler(tornado.web.RequestHandler):

    def get(self):
        self.clear_cookie('user_id')
        self.redirect('/bye')

class ByeHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('home/bye.html')
