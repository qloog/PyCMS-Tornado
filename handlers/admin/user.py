#!/usr/bin/env python
#-*- coding: utf-8 -*-

import tornado.web
from tornado.escape import json_encode
from handlers.admin import BaseHandler
from model.admin import AdminRole, Admin as User
from utils import encrypt, obj2dict, date_encode
import re


class AdminEditInfoHandler(BaseHandler):

    error_message = {
        '110': '信息填写不完整',
        '111': '该用户不存在',
        '112': '更新失败'
    }
    url = 'admin/user/edit_info.html'

    @tornado.web.authenticated
    def get(self):
        self.render(self.url, user=self.current_user)

    def post(self):
        realname = self.get_argument('realname', '')
        email = self.get_argument('email', '')

        self.set_header("Content-Type", "application/json")

        if not (realname and email):
            ret = {'code': 110, 'msg': self.error_message['110'], 'url': self.url}
            return self.write(json_encode(ret))

        user = User.get_by_uid(self.get_secure_cookie("admin_user_id"))
        if not user:
            ret = {'code': 111, 'msg': self.error_message['111']}
            return self.write(json_encode(ret))

        user.update('', email, realname)
        ret = {'code': 0, 'msg': '更新成功', 'url': self.url}
        return self.write(json_encode(ret))


class AdminCheckUsernameHandler(BaseHandler):

    def post(self):
        username = self.get_argument('username', '')

        self.set_header("Content-Type", "application/json")

        user = User.get_by_username(username)
        if not user:
            ret = {'code': 0}
        else:
            ret = {'code': 1}
        return self.write(json_encode(ret))


class AdminCheckEmailHandler(BaseHandler):

    def post(self):
        email = self.get_argument('email', '')

        self.set_header("Content-Type", "application/json")

        user = User.get_by_email(email)
        if not user:
            ret = {'code': 0}
        else:
            ret = {'code': 1}
        return self.write(json_encode(ret))


class AdminEditPasswordHandler(BaseHandler):

    error_message = {
        '210': '信息填写不完整',
        '211': '该用户不存在',
        '212': '更新失败'
    }
    url = 'admin/user/edit_password.html'

    @tornado.web.authenticated
    def get(self):
        self.render(self.url, user=self.current_user)

    def post(self):
        password = self.get_argument('new_password', '')

        self.set_header("Content-Type", "application/json")

        if not password:
            ret = {'code': 210, 'msg': self.error_message['210'], 'url': self.url}
            return self.write(json_encode(ret))

        user = User.get_by_uid(self.get_secure_cookie("admin_user_id"))
        if not user:
            ret = {'code': 211, 'msg': self.error_message['211']}
            return self.write(json_encode(ret))

        user.update_password(password)
        ret = {'code': 0, 'msg': '更新成功', 'url': self.url}
        return self.write(json_encode(ret))


class AdminCheckPasswordHandler(BaseHandler):

    def post(self):
        password = self.get_argument('password', '')

        self.set_header("Content-Type", "application/json")

        user = User.get_by_uid(self.get_secure_cookie("admin_user_id"))
        if user.get_password() == encrypt(password):
            ret = {'code': 0}
        else:
            ret = {'code': 1}
        return self.write(json_encode(ret))


class AdminMemberListHandler(BaseHandler):

    url = 'admin/user/member_list.html'

    def get(self):
        self.render(self.url)

    def post(self):
        pass


class AdminMemberListDatagridHandler(BaseHandler):

    def get(self):
        page = self.get_argument('page', 1)
        rows = self.get_argument('rows', 20)

        start = (int(page) - 1) * int(rows)
        limit = rows
        user_list = User.gets(start, limit)
        total = User.get_count()

        response = {
            'total': total,
            'rows': user_list
        }
        return self.write(date_encode(response))


class AdminMemberAddHandler(BaseHandler):

    error_message = {
        '110': '用户名不能为空',
        '111': '密码不能为空',
        '112': '邮箱不匹配',
        '113': '角色不能为空',
        '114': '添加失败'
    }

    url = 'admin/user/member_add.html'

    def get(self):
        self.render(self.url)

    def post(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        email = self.get_argument('email', '')
        realname = self.get_argument('realname', '')
        role_id = self.get_argument('role_id', 0)

        if not username or len(username) > 15:
            ret = {'code': 110, 'msg': self.error_message['110']}
            return self.write(json_encode(ret))

        if not password:
            ret = {'code': 111, 'msg': self.error_message['111']}
            return self.write(json_encode(ret))

        match = re.search(r'[\w.-]+@[\w.-]+', email)
        if not match:
            ret = {'code': 112, 'msg': self.error_message['112']}
            return self.write(json_encode(ret))

        if not role_id:
            ret = {'code': 113, 'msg': self.error_message['111']}
            return self.write(json_encode(ret))

        result = User.new(username, email, password, realname, role_id)
        if result:
            ret = {'code': 0, 'msg': '添加成功'}
            return self.write(json_encode(ret))
        else:
            ret = {'code': 114, 'msg': self.error_message['114']}
            return self.write(json_encode(ret))



class AdminMemberEditHandler(BaseHandler):

    error_message = {
        '110': '用户名不能为空',
        '111': '密码不能为空',
        '112': '邮箱不匹配',
        '113': '角色不能为空',
        '114': '更新失败'
    }

    url = 'admin/user/member_edit.html'

    def get(self):
        user_id = int(self.get_argument('id', 0))
        user = User.get(user_id)
        roles = AdminRole.gets()

        return self.render(self.url, info=user, roles=roles)

    def post(self):
        user_id = int(self.get_argument('id', 0))
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        email = self.get_argument('email', '')
        realname = self.get_argument('realname', '')
        role_id = int(self.get_argument('role_id', 0))


        match = re.search(r'[\w.-]+@[\w.-]+', email)
        if not match:
            ret = {'code': 112, 'msg': self.error_message['112']}
            return self.write(json_encode(ret))

        if not role_id:
            ret = {'code': 113, 'msg': self.error_message['113']}
            return self.write(json_encode(ret))

        result = User.update(user_id, username, email, password, realname, role_id)
        if result:
            ret = {'code': 0, 'msg': '更新成功'}
            return self.write(json_encode(ret))
        else:
            ret = {'code': 114, 'msg': self.error_message['114']}
            return self.write(json_encode(ret))


class AdminCheckRoleHandler(BaseHandler):

    def post(self):
        role_name = self.get_argument('role_name', '')

        self.set_header("Content-Type", "application/json")

        role = AdminRole.get_by_rolename(role_name)
        if not role:
            ret = {'code': 0}
        else:
            ret = {'code': 1}
        return self.write(json_encode(ret))


class AdminRoleListHandler(BaseHandler):

    url = 'admin/user/role_list.html'

    def get(self):
        self.render(self.url)

    def post(self):
        pass


class AdminRoleListDatagridHandler(BaseHandler):

    def get(self):
        page = self.get_argument('page', 1)
        rows = self.get_argument('rows', 20)
        sort = self.get_argument('sort', '')
        order = self.get_argument('order', 'ASC')

        start = (int(page) - 1) * int(rows)
        limit = rows
        role_list = AdminRole.gets(start, limit)
        total = AdminRole.get_count()

        response = {
            'total': total,
            'rows': [obj2dict(role) for role in role_list]
        }
        return self.write(json_encode(response))


class AdminRoleAddHandler(BaseHandler):

    error_message = {
        '310': '角色名称不能为空',
        '311': '添加失败'
    }

    url = 'admin/user/role_add.html'

    def get(self):
        self.render(self.url)

    def post(self):
        role_name = self.get_argument('role_name', '')
        description = self.get_argument('description', '')
        list_order = int(self.get_argument('list_order', 0))
        status = int(self.get_argument('status', 0))

        if not role_name:
            ret = {'code': 310, 'msg': self.error_message['310']}
            return self.write(json_encode(ret))

        result = AdminRole.new(role_name, description, list_order, status)
        if result:
            ret = {'code': 0, 'msg': '添加成功'}
            return self.write(json_encode(ret))
        else:
            ret = {'code': 311, 'msg': self.error_message['311']}
            return self.write(json_encode(ret))


class AdminRoleEditHandler(BaseHandler):

    error_message = {
        '310': '角色名称不能为空',
        '311': '更新失败'
    }

    url = 'admin/user/role_edit.html'

    def get(self):
        role_id = int(self.get_argument('id', 0))
        role = AdminRole.get(role_id)

        return self.render(self.url, info=role)

    def post(self):
        role_id = int(self.get_argument('id', 0))
        role_name = self.get_argument('role_name', '')
        description = self.get_argument('description', '')
        list_order = int(self.get_argument('list_order', 0))
        status = int(self.get_argument('status', 0))

        if not role_name:
            ret = {'code': 310, 'msg': self.error_message['310']}
            return self.write(json_encode(ret))

        result = AdminRole.update(role_id, role_name, description, list_order, status)
        if result:
            ret = {'code': 0, 'msg': '更新成功'}
            return self.write(json_encode(ret))
        else:
            ret = {'code': 311, 'msg': self.error_message['311']}
            return self.write(json_encode(ret))


class AdminRoleOrderHandler(BaseHandler):

    def get(self):
        order_role = self.request.arguments

        for key, list_order in enumerate(order_role):
            role_id = list_order[:]

            list_order = order_role[list_order][0]
            AdminRole.update(role_id, '', '', list_order, 0)

        ret = {'code': 0, 'msg': '更新成功'}
        return self.write(json_encode(ret))







