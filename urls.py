#!/usr/bin/env python
# encoding: utf-8

__all__ = ['urls_pattern']

#home
from handlers.home.index import IndexHandler
from handlers.home.login import RegisterHandler, LoginHandler, LogoutHandler, ByeHandler
from handlers.home.settings import ProfileHandler, PasswordHandler, NotificationsHandler
#from handlers.home.upload import UploadHandler
from handlers.home.help import AboutUsHandler, ContactUsHandler, JoinUsHandler, OfficialNewsHandler

urls_pattern = [
    ('/', IndexHandler),
    ('/login', LoginHandler),
    ('/register', RegisterHandler),
    ('/logout', LogoutHandler),
    ('/bye', ByeHandler),
    #('/upload', UploadHandler)
    ('/settings/profile', ProfileHandler),
    ('/settings/notifications', NotificationsHandler),
    ('/settings/password', PasswordHandler),
    ('/help/about_us', AboutUsHandler),
    ('/help/contact_us', ContactUsHandler),
    ('/help/join_us', JoinUsHandler),
    ('/help/official_news', OfficialNewsHandler)
]


#admin
from handlers.admin.login import AdminLoginHandler, AdminLogoutHandler
from handlers.admin.index import AdminIndexHandler
from handlers.admin.user import (
    AdminEditInfoHandler,
    AdminCheckUsernameHandler,
    AdminCheckEmailHandler,
    AdminEditPasswordHandler,
    AdminCheckPasswordHandler,
    AdminMemberListHandler,
    AdminMemberListDatagridHandler,
    AdminMemberAddHandler,
    AdminMemberEditHandler,
    AdminRoleListHandler,
    AdminRoleAddHandler,
    AdminRoleListDatagridHandler,
    AdminRoleEditHandler,
    AdminCheckRoleHandler,
    AdminRoleOrderHandler
)
from handlers.admin.setting import AdminSettingPropertyGridHandler, AdminSettingSiteHandler
from handlers.admin.news import (
    NewsAddHandler,
    NewsListHandler,
    NewsListDatagridHandler,
    NewsEditHandler,
    NewsCategoryListHandler,
    NewsCategoryEditHandler,
    NewsCategoryAddHandler,
    NewsCategoryListDatagridHandler
)


urls_pattern_admin = [
    ('/admin/login', AdminLoginHandler),
    ('/admin/logout', AdminLogoutHandler),
    ('/admin/index', AdminIndexHandler),
    ('/admin/user/check_username', AdminCheckUsernameHandler),
    ('/admin/user/edit_info', AdminEditInfoHandler),
    ('/admin/user/check_email', AdminCheckEmailHandler),
    ('/admin/user/edit_password', AdminEditPasswordHandler),
    ('/admin/user/check_password', AdminCheckPasswordHandler),
    ('/admin/user/member_list', AdminMemberListHandler),
    ('/admin/user/member_list/datagrid', AdminMemberListDatagridHandler),
    ('/admin/user/member_add', AdminMemberAddHandler),
    ('/admin/user/member_edit', AdminMemberEditHandler),
    ('/admin/user/role_list', AdminRoleListHandler),
    ('/admin/user/role_list/datagrid', AdminRoleListDatagridHandler),
    ('/admin/user/role_add', AdminRoleAddHandler),
    ('/admin/user/role_edit', AdminRoleEditHandler),
    ('/admin/user/check_role_name', AdminCheckRoleHandler),
    ('/admin/user/role_order', AdminRoleOrderHandler),
    ('/admin/setting/site', AdminSettingSiteHandler),
    ('/admin/setting/site/propertygrid', AdminSettingPropertyGridHandler),
    ('/admin/news/news_list', NewsListHandler),
    ('/admin/news/news_list/datagrid', NewsListDatagridHandler),
    ('/admin/news/news_edit', NewsEditHandler),
    ('/admin/news/news_add', NewsAddHandler),
    ('/admin/news/news_category_list', NewsCategoryListHandler),
    ('/admin/news/news_category_list/datagrid', NewsCategoryListDatagridHandler),
    ('/admin/news/news_category_edit', NewsCategoryEditHandler),
    ('/admin/news/news_category_add', NewsCategoryAddHandler)
]

urls_pattern.extend(urls_pattern_admin)
