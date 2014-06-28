#!/usr/bin/env python
#-*- coding:utf8 -*-

import tornado.web
from utils import encrypt
from handlers.home import BaseHandler
from model.user import User, UserInfo


class ProfileHandler(BaseHandler):

    error_message = {
        '130': 'update success!',
        '131': 'realname empty',
        '132': 'username empty',
        '133': 'email empty',
    }

    @tornado.web.authenticated
    def get(self):
        user = self.current_user
        user_info = UserInfo.get_info_by_uid(user.user_id)
        self.render('home/settings_profile.html', error=None, user=user, user_info=user_info)

    def post(self):
        user = self.current_user
        realname = self.get_argument('realname', '')
        username = self.get_argument('username', '')
        email = self.get_argument('email', '')
        about_me = self.get_argument('about_me', '')
        avatar_src = self.get_argument('avatar_src', '')
        if not realname:
            self.render('home/settings_profile.html', error=131)
            return
        if not username:
            self.render('home/settings_profile.html', error=132)
            return
        if not email:
            self.render('home/settings_profile.html', error=133)
            return

        user.update(username, email, realname, about_me, avatar_src)
        self.redirect('/settings/profile')


class PasswordHandler(BaseHandler):

    error_message = {
        '140': '密码修改成功',
        '141': '原始密码填写错误',
        '142': '新密码不能为空',
        '143': '校验密码不能为空',
        '144': '两次密码不一致',
        '145': '密码修改出错，请稍后再试'
    }

    @tornado.web.authenticated
    def get(self):
        self.render('home/settings_password.html', error=None)

    @tornado.web.authenticated
    def post(self):
        user = self.current_user
        password = self.get_argument('password', '')
        new_password = self.get_argument('new_password', '')
        verify_password = self.get_argument('verify_password', '')

        if user.get_password() != encrypt(password):
            self.render('home/settings_password.html', error=141)
            return
        if new_password == '':
            self.render('home/settings_password.html', error=142)
            return
        if verify_password == '':
            self.render('home/settings_password.html', error=143)
            return
        if new_password != verify_password:
            self.render('home/settings_password.html', error=144)
            return

        result = user.update_password(new_password)
        if not result:
            self.render('home/settings_password.html', error=145)
            return
        self.render('home/settings_password.html', error=140)


class NotificationsHandler(BaseHandler):

    def get(self):
        self.render('home/settings_notifications.html')

    def post(self):
        pass


