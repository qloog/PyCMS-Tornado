#!/usr/bin/env python
# -*- coding:utf-8 -*-

from tornado.web import RequestHandler
from model.user import User

class BaseHandler(RequestHandler):
    @property
    def db(self):
        return self.application.db

    @property
    def cache(self):
        return self.application.cache

    def get_current_user(self):
        user_id = self.get_secure_cookie('user_id')
        if not user_id:
            return None
        return User.get(user_id)


