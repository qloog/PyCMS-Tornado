#!/usr/bin/env python
#-*- coding:utf-8 -*-

from libs import Base, db_session
from utils import obj2dict
from sqlalchemy import Column, String
from utils.dict_setting import setting


class Setting(Base):

    __tablename__ = 'wmh_setting'

    key = Column(String(100), primary_key=True)
    value = Column(String(255))

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return "<Settings('%s')>" % (self.key)


    @classmethod
    def update(cls, key, value):
        update = {}
        if key and value:
            update['value'] = value

        try:
            db_session.query(Setting).filter(Setting.key == key).update(update)
            db_session.commit()
            return True
        except:
            db_session.rollback()
            raise

    @classmethod
    def gets(cls):
        _dict = {}
        #get current config list
        fields = setting
        settingFields = setting.keys()

        #get data from db
        data = db_session.query(Setting.key, Setting.value).filter(Setting.key.in_(settingFields))
        _dict['total'] = data.count()
        data = data.all()

        _data_dict = dict(data)

        for key in fields:
            #如果数据库不存在该设置项则从默认值中获取
            fields[key]['value'] = _data_dict[key] if _data_dict[key] else fields[key]['default']
            fields[key]['key'] = key

        _dict['rows'] = fields.values()
        return _dict


