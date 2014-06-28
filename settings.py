#!/usr/bin/env python
# encoding: utf-8

from os import path
from urls import urls_pattern as url_handlers

DEBUG = True

# the application settings
settings = {
    'debug': DEBUG,
    'cookie_secret': 'test',    # TODO: get the real secret
    'login_url': '/admin/login',
    'xsrf_cookies': True,
    'static_path': path.join(path.dirname(__file__), 'static'),
    'template_path': path.join(path.dirname(__file__), 'templates'),
    #'ui_modules': '' # TODO: the ui modules file
}

