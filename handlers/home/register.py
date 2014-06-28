#!/usr/bin/env python
#-*- coding: utf-8 -*-

import tornado.web

class RegisterHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('home/register.html', error=None)
