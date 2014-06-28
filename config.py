#!/usr/bin/env python
# encoding: utf-8

#后台自定义设置
SAVE_LOG_OPEN = 0           # 开启后台日志记录
MAX_LOGIN_TIMES = 9         # 最大登录失败次数，防止为0时不能登录，因此不包含第一次登录
LOGIN_WAIT_TIME = 60        # 登录次数达到后需要等待时间才能再次登录，单位：分钟

DATAGRID_PAGE_SIZE = 20     # 列表默认分页数

# 单独配置，会覆盖全局配置
FILE_UPLOAD_CONFIG = {
    'exts': ['zip', 'rar', 'tar', 'gz', '7z', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt'],
    'maxSize': 102400
}
FILE_UPLOAD_LINK_CONFIG = {
    'exts': ['zip', 'rar', 'tar', 'gz', '7z', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt']
}
FILE_UPLOAD_IMG_CONFIG = {
    'exts': ['jpg', 'jpeg', 'gif', 'png']
}
FILE_UPLOAD_FLASH_CONFIG = {
    'exts': ['swf']
}
FILE_UPLOAD_MEDIA_CONFIG = {
    'exts':  ['avi']
}

# the sql database settings
DATABASE = {
    'default': {
        'driven': 'mysql',
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'port': 'port',
        'database': 'utf-8',
    },
}

# TODO: the reids database settings
REDIS = {

}

# TODO: the log settings


# TODO: memcahce usage
