#!/usr/bin/env python
# -*- coding: utf-8 -*

import hashlib
from datetime import datetime
import json



def encrypt(key):
    hash = hashlib.md5()
    hash.update(key)
    return hash.hexdigest()


def obj2dict2(obj):
    """
    summary:
        将object转换成dict类型
    """
    memberlist = [m for m in dir(obj)]
    _dict = {}
    for m in memberlist:
        if m[0] != "_" and not callable(m):
            _dict[m] = getattr(obj, m)

    return _dict


def obj2dict(obj):
    """
    summary:
        将object转换成dict类型
    """
    _dict = {}
    for key, value in vars(obj).iteritems():
        if key[0] != "_":
            _dict[key] = value
    return _dict


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.__str__()
        return json.JSONEncoder.default(self, obj)


def date_encode(my_dict):
    """
    question: TypeError: datetime.datetime(2011, 11, 11, 0, 0) is not JSON serializable
    see: http://www.tuicool.com/articles/rYJzIv
    :param my_dict:
    :return: json
    """
    return json.dumps(my_dict, cls=DateEncoder)




