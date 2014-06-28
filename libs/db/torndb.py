#!/usr/bin/env python
#-*- coding:utf-8 -*-

# database.py
import torndb

db_session = torndb.Connection("localhost", "test", user="", password="")
