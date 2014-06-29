#!/usr/bin/env python
#-*- coding: utf-8 -*-

from tornado.escape import json_encode
from handlers.admin import BaseHandler
from model.news import News, NewsCategory
from utils import date_encode, obj2dict


class NewsListHandler(BaseHandler):

    url = 'admin/news/news_list.html'

    def get(self):
        self.render(self.url)


class NewsListDatagridHandler(BaseHandler):

    def get(self):
        page = self.get_argument('page', 1)
        rows = self.get_argument('rows', 20)

        title = self.get_argument('title', '')
        begin = self.get_argument('begin', '')
        end = self.get_argument('end', '')

        query = {}
        if title:
            query['title'] = title
        if begin:
            query['begin'] = begin
        if end:
            query['end'] = end

        offset = (int(page) - 1) * int(rows)
        limit = rows
        rows = News.gets(offset, limit, **query)
        rows = [obj2dict(r) for r in rows]
        total = News.get_count()

        response = {'total': total, 'rows': rows}
        return self.write(date_encode(response))


class NewsEditHandler(BaseHandler):

    error_message = {
        '110': '请选择分类',
        '111': '请填写标题',
        '112': '请填写内容',
        '113': '请填写发布者',
        '114': '添加失败'
    }

    url = 'admin/news/news_edit.html'

    def get(self):
        news_id = self.get_argument('id', '')
        news = News.get(news_id)
        category = NewsCategory.gets()
        self.render(self.url, info=news, categorys=category)

    def post(self):

        news_id = int(self.get_argument('id', 0))
        category_id = int(self.get_argument('category_id', 0))
        title = self.get_argument('title', '')
        content = self.get_argument('content', '')
        create_uid = self.get_secure_cookie('admin_user_id')
        status = int(self.get_argument('status', 0))

        if not category_id:
            response = {'code': 110, 'msg': self.error_message['110']}
            return self.write(json_encode(response))
        if not title:
            response = {'code': 111, 'msg': self.error_message['111']}
            return self.write(json_encode(response))
        if not content:
            response = {'code': 112, 'msg': self.error_message['112']}
            return self.write(json_encode(response))
        if not create_uid:
            response = {'code': 113, 'msg': self.error_message['113']}
            return self.write(json_encode(response))

        result = News.update(news_id, category_id, title, content, create_uid, status)
        if result:
            response = {'code': 0, 'msg': '添加成功'}
            return self.write(json_encode(response))
        else:
            response = {'code': 114, 'msg': self.error_message['114']}
            return self.write(json_encode(response))


class NewsAddHandler(BaseHandler):

    error_message = {
        '110': '请选择分类',
        '111': '请填写标题',
        '112': '请填写内容',
        '113': '请填写发布者',
        '114': '添加失败'
    }

    url = 'admin/news/news_add.html'

    def get(self):
        self.render(self.url)

    def post(self):

        category_id = int(self.get_argument('category_id', 0))
        title = self.get_argument('title', '')
        content = self.get_argument('content', '')
        create_uid = self.get_secure_cookie('admin_user_id')
        status = int(self.get_argument('status', 0))

        if not category_id:
            response = {'code': 110, 'msg': self.error_message['110']}
            return self.write(json_encode(response))
        if not title:
            response = {'code': 111, 'msg': self.error_message['111']}
            return self.write(json_encode(response))
        if not content:
            response = {'code': 112, 'msg': self.error_message['112']}
            return self.write(json_encode(response))

        result = News.new(category_id, title, content, create_uid, status)
        if result:
            response = {'code': 0, 'msg': '添加成功'}
            return self.write(json_encode(response))
        else:
            response = {'code': 114, 'msg': self.error_message['114']}
            return self.write(json_encode(response))


class NewsCategoryListHandler(BaseHandler):

    url = 'admin/news/news_category_list.html'

    def get(self):
        self.render(self.url)


class NewsCategoryListDatagridHandler(BaseHandler):

    def get(self):
        page = self.get_argument('page', 1)
        rows = self.get_argument('rows', 20)

        start = (int(page) - 1) * int(rows)
        limit = rows
        rows = NewsCategory.gets(start, limit)
        rows = [obj2dict(r) for r in rows]
        total = NewsCategory.get_count()
        response = {'total': total, 'rows': rows}
        return self.write(date_encode(response))


class NewsCategoryEditHandler(BaseHandler):

    error_message = {
        '110': '请选择分类',
        '111': '分类名为空',
        '112': '更新失败'
    }

    url = 'admin/news/news_category_edit.html'

    def get(self):
        category_id = self.get_argument('id', '')
        news_category = NewsCategory.get(category_id)
        self.render(self.url, info=news_category)

    def post(self):

        category_id = int(self.get_argument('id', 0))
        category_name = self.get_argument('category_name', '')

        if not category_id:
            response = {'code': 110, 'msg': self.error_message['110']}
            return self.write(json_encode(response))
        if not category_name:
            response = {'code': 111, 'msg': self.error_message['111']}
            return self.write(json_encode(response))

        result = NewsCategory.update(category_id, category_name)
        if result:
            response = {'code': 0, 'msg': '更新成功'}
            return self.write(json_encode(response))
        else:
            response = {'code': 112, 'msg': self.error_message['112']}
            return self.write(json_encode(response))


class NewsCategoryAddHandler(BaseHandler):

    error_message = {
        '110': '请填写分类',
        '111': '分类名为空',
        '112': '添加失败'
    }

    url = 'admin/news/news_category_add.html'

    def get(self):
        self.render(self.url)

    def post(self):

        category_name = self.get_argument('category_name', '')

        if not category_name:
            response = {'code': 110, 'msg': self.error_message['110']}
            return self.write(json_encode(response))

        result = NewsCategory.new(category_name)
        if result:
            response = {'code': 0, 'msg': '添加成功'}
            return self.write(json_encode(response))
        else:
            response = {'code': 112, 'msg': self.error_message['112']}
            return self.write(json_encode(response))