#!/usr/bin/env python
#-*- coding:utf-8 -*-

from datetime import datetime
from libs import Base, db_session
from utils import obj2dict
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship, backref
from model.admin import Admin


class News(Base):

    __tablename__ = 'wmh_news'

    news_id = Column(Integer, primary_key=True)
    title = Column(String(50))
    content = Column(Text)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    status = Column(Integer)
    create_uid = Column(Integer, ForeignKey('wmh_admin.user_id'))
    category_id = Column(Integer, ForeignKey('wmh_news_category.category_id'))
    #category = relationship('NewsCategory', backref='News')

    def __init__(self, news_id, category_id, title, content, create_uid=0, status=0, create_time='', update_time=''):
        self.news_id = news_id
        self.category_id = category_id
        self.title = title
        self.content = content
        if create_time:
            self.create_time = create_time
        if update_time:
            self.update_time = update_time
        if create_uid:
            self.create_uid = create_uid
        self.status = status

    def __repr__(self):
        return "<News('%s')>" % self.title

    @classmethod
    def initialize(cls, item):
        if not item:
            return None

        news_id = item.news_id
        category_id = item.category_id
        title = item.title
        content = item.content
        create_time = item.create_time
        update_time = item.update_time
        create_uid = item.create_uid
        status = item.status

        if not news_id:
            return None
        return cls(news_id, category_id, title, content, create_uid, status, create_time, update_time)

    @classmethod
    def new(cls, category_id, title, content, create_uid, status):
        """
        add new news
        """
        news = News(None, category_id, title, content, create_uid, status)

        #TODO optimize
        news.update_time = '0000-00-00 00:00:00'

        db_session.add(news)
        try:
            db_session.commit()
        except:
            db_session.rollback()

        if news.news_id:
            return cls.get(news.news_id)
        return None

    @classmethod
    def update(cls, news_id, category_id, title, content, create_uid, status):

        update = {}
        if category_id:
            update['category_id'] = category_id
        if title:
            update['title'] = title
        if content:
            update['content'] = content
        if create_uid:
            update['create_uid'] = create_uid
        if status:
            update['status'] = status

        current_time = datetime.now()
        update_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        update['update_time'] = update_time

        try:
            db_session.query(News).filter(News.news_id == news_id).update(update)
            db_session.commit()
            return True
        except:
            db_session.rollback()
            raise

    @classmethod
    def get(cls, news_id):
        item = db_session.query(News.news_id, News.category_id, News.title, News.content, News.create_uid, News.status,
                                News.create_time, News.update_time).filter(News.news_id == news_id).first()
        return item and cls.initialize(item)

    @classmethod
    def gets(cls, offset=0, limit=20, title='', begin=0, end=0):
        end = end if end else '2039-12-12'
        rs = db_session.query(News.news_id, News.news_id.label('operate_id'), News.category_id, News.title,
                              News.create_time, News.create_uid, News.update_time, News.status,
                              NewsCategory.category_name, Admin.username).\
            join(NewsCategory, Admin).\
            filter(News.category_id == NewsCategory.category_id, News.create_uid == Admin.user_id).\
            filter(News.title.like('%'+title+'%')).\
            filter(News.create_time >= begin, News.create_time <= end).\
            offset(offset).limit(limit)
        return rs.all()

    @classmethod
    def get_count(cls):
        return db_session.query(News).count()


class NewsCategory(Base):

    __tablename__ = 'wmh_news_category'

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(50))

    def __init__(self, category_id, category_name):
        self.category_id = category_id
        self.category_name = category_name

    def __repr__(self):
        return "<NewsCategory('%s')>" % self.category_name

    @classmethod
    def new(cls, category_name):
        """
        add new news
        """
        newsCategory = NewsCategory(None, category_name)

        db_session.add(newsCategory)
        try:
            db_session.commit()
        except:
            db_session.rollback()

        if newsCategory.category_id:
            return cls.get(newsCategory.category_id)
        return None

    @classmethod
    def update(cls, category_id, category_name):

        update = {}
        if category_name:
            update['category_name'] = category_name

        try:
            db_session.query(NewsCategory).filter(NewsCategory.category_id == category_id).update(update)
            db_session.commit()
            return True
        except:
            db_session.rollback()
            raise

    @classmethod
    def get(cls, category_id):
        item = db_session.query(NewsCategory.category_id, NewsCategory.category_name)\
            .filter(NewsCategory.category_id == category_id).first()
        return item

    @classmethod
    def gets(cls, start=0, limit=20):
        rs = db_session.query(NewsCategory.category_id, NewsCategory.category_name).offset(start).limit(limit)
        return rs.all()

    @classmethod
    def get_count(cls):
        return db_session.query(NewsCategory).count()
