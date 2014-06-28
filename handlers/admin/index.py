#!/usr/bin/env python
#-*- coding: utf-8 -*-

import tornado.web
from handlers.admin import BaseHandler

class AdminIndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('admin/index.html', user=self.current_user)
