#!/usr/bin/env python
#-*- coding:utf-8 -*-

# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

"""
Problem:
 1.StatementError: Can't reconnect until invalid transaction is rolled back
 2.MYSQL has gone away
See: http://mofanim.wordpress.com/2013/01/02/sqlalchemy-mysql-has-gone-away/
Solution: http://docs.sqlalchemy.org/en/rel_0_7/core/pooling.html#setting-pool-recycle
"""
#engine = create_engine('mysql://root:123456@localhost/wuminghui', pool_recycle=3600, encoding="utf-8", echo=True) #会乱码
engine = create_engine('mysql://root:123456@localhost/wuminghui', pool_recycle=60, connect_args={"charset": "utf8"}, echo=True)

Base = declarative_base()
db_session = scoped_session(sessionmaker(bind=engine))


def create_all():
    Base.metadata.create_all(bind=engine)


def drop_all():
    Base.metadata.drop_all(bind=engine)
