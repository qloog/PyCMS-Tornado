#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

from tornado.options import define, options

from libs import db_session, engine  # import the engine to bind
#from libs.memcache import cache
from settings import url_handlers, settings

define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self, handlers, **settings):
        tornado.web.Application.__init__(self, handlers, **settings)
        # Have one global connection. or call:session
        self.db = db_session
        #self.cache = cache
        #self.redis = redis.StrictRedis()

application = Application(url_handlers, **settings)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
