#!/usr/bin/env python
#-*- coding: utf-8 -*-

from tornado.escape import json_encode
from handlers.admin import BaseHandler
from model.setting import Setting


class AdminSettingSiteHandler(BaseHandler):

    url = 'admin/setting/site.html'

    def get(self):
        self.render(self.url)

    def post(self):
        #fields = self.request.arguments
        fields = self.get_body_arguments('data[]')

        for field in fields:
            v = field.split('#')
            key = v[0]
            value = v[1]
            Setting.update(key, value)

        response = {
            'code': 0,
            'msg': '更新成功'
        }
        return self.write(json_encode(response))


class AdminSettingPropertyGridHandler(BaseHandler):

    url = 'admin/setting/site.html'

    def get(self):
        response = Setting.gets()
        return self.write(json_encode(response))

