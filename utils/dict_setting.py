#!/usr/bin/env python
# -*- coding: utf-8 -*

import config as c

setting =  {
    #前台设置
    'SITE_TITLE' : {
        'name'    : '站点标题',
        'group'   : '前台设置',
        'editor'  : 'text',
        'default' : '',
    },
    'SITE_KEYWORDS' : {
        'name'    : '关键字',
        'group'   : '前台设置',
        'editor'  : 'text',
        'default' : '',
    },
    'SITE_DESCRIPTION' : {
        'name'    : '描述',
        'group'   : '前台设置',
        'editor'  : 'textarea',
        'default' : '',
    },
    'SITE_ICP' : {
        'name'    : '备案号',
        'group'   : '前台设置',
        'editor'  : 'text',
        'default' : '',
    },

    #后台设置
    'SAVE_LOG_OPEN' : {
        'name'    : '开启后台日志记录',
        'group'   : '后台设置',
        'editor'  : {'type':'checkbox','options':{'on':'开启','off':'关闭'}},
        'default' : '开启' if c.SAVE_LOG_OPEN else '关闭',
    },
    'MAX_LOGIN_TIMES' : {
        'name'    : '登录失败后允许最大次数',
        'group'   : '后台设置',
        'editor'  : 'numberbox',
        'default' : c.MAX_LOGIN_TIMES,
    },
    'LOGIN_WAIT_TIME' : {
        'name'    : '错误等待时间(分钟)',
        'group'   : '后台设置',
        'editor'  : 'numberbox',
        'default' : c.LOGIN_WAIT_TIME,
    },
    'DATAGRID_PAGE_SIZE' : {
        'name'    : '列表默认分页数',
        'group'   : '后台设置',
        'editor'  : 'numberbox',
        'default' : c.DATAGRID_PAGE_SIZE,
    },

    #上传设置
    'FILE_UPLOAD_CONFIG.exts' : {
        'name'    : '允许上传扩展(全局)',
        'group'   : '上传设置',
        'editor'  : 'text',
        'default' : c.FILE_UPLOAD_CONFIG['exts'],
    },
    'FILE_UPLOAD_CONFIG.maxSize' : {
        'name'    : '允许上传大小(全局)',
        'group'   : '上传设置',
        'editor'  : 'numberbox',
        'default' : c.FILE_UPLOAD_CONFIG['maxSize'],
    },
    'FILE_UPLOAD_LINK_CONFIG.exts' : {
        'name'    : '允许上传扩展(附件)',
        'group'   : '上传设置',
        'editor'  : 'text',
        'default' : c.FILE_UPLOAD_LINK_CONFIG['exts'],
    },
    'FILE_UPLOAD_IMG_CONFIG.exts' : {
        'name'    : '允许上传扩展(图片)',
        'group'   : '上传设置',
        'editor'  : 'text',
        'default' : c.FILE_UPLOAD_IMG_CONFIG['exts'],
    },
    'FILE_UPLOAD_FLASH_CONFIG.exts' : {
        'name'    : '允许上传扩展(动画)',
        'group'   : '上传设置',
        'editor'  : 'text',
        'default' : c.FILE_UPLOAD_FLASH_CONFIG['exts'],
    },
    'FILE_UPLOAD_MEDIA_CONFIG.exts' : {
        'name'    : '允许上传扩展(媒体)',
        'group'   : '上传设置',
        'editor'  : 'text',
        'default' : c.FILE_UPLOAD_MEDIA_CONFIG['exts']
    },

    #邮箱设置
    'EMAIL_SMTP' : {
        'name'    : 'SMTP',
        'group'   : '邮箱设置',
        'editor'  : 'text',
        'default' : '',
    },
    'EMAIL_PORT' : {
        'name'    : '端口',
        'group'   : '邮箱设置',
        'editor'  : 'numberbox',
        'default' : '25',
    },
    'EMAIL_EMAIL' : {
        'name'    : '邮箱地址',
        'group'   : '邮箱设置',
        'editor'  : 'text',
        'default' : '',
    },
    'EMAIL_USER' : {
        'name'    : '用户名',
        'group'   : '邮箱设置',
        'editor'  : 'text',
        'default' : '',
    },
    'EMAIL_PWD' : {
        'name'    : '密码',
        'group'   : '邮箱设置',
        'editor'  : 'text',
        'default' : '',
    },

    #飞信设置
    'FETION_USER' : {
        'name'    : '用户名',
        'group'   : '飞信设置',
        'editor'  : 'text',
        'default' : '',
    },
    'FETION_PWD' : {
        'name'    : '密码',
        'group'   : '飞信设置',
        'editor'  : 'text',
        'default' : '',
    },

    #登录接口设置
    'THINK_SDK_SINA.APP_KEY' : {
        'name'    : 'sina APP ID',
        'group'   : '登录接口设置',
        'editor'  : 'text',
        'default' : '',
    },
    'THINK_SDK_SINA.APP_SECRET' : {
        'name'    : 'sina KEY',
        'group'   : '登录接口设置',
        'editor'  : 'text',
        'default' : '',
    },

    'THINK_SDK_BAIDU.APP_KEY' : {
        'name'    : 'baidu APP ID',
        'group'   : '登录接口设置',
        'editor'  : 'text',
        'default' : '',
    },
    'THINK_SDK_BAIDU.APP_SECRET' : {
        'name'    : 'baidu KEY',
        'group'   : '登录接口设置',
        'editor'  : 'text',
        'default' : '',
    },

    'THINK_SDK_GOOGLE.APP_KEY' : {
        'name'    : 'Google APP ID',
        'group'   : '登录接口设置',
        'editor'  : 'text',
        'default' : '',
    },
    'THINK_SDK_GOOGLE.APP_SECRET' : {
        'name'    : 'Google KEY',
        'group'   : '登录接口设置',
        'editor'  : 'text',
        'default' : '',
    },

    'THINK_SDK_QQ.APP_KEY' : {
        'name'    : 'QQ APP ID',
        'group'   : '登录接口设置',
        'editor'  : 'text',
        'default' : '',
    },
    'THINK_SDK_QQ.APP_SECRET' : {
        'name'    : 'QQ KEY',
        'group'   : '登录接口设置',
        'editor'  : 'text',
        'default' : '',
    },

    'THINK_SDK_TAOBAO.APP_KEY' : {
        'name'    : 'taobao APP ID',
        'group'   : '登录接口设置',
        'editor'  : 'text',
        'default' : '',
    },
    'THINK_SDK_TAOBAO.APP_SECRET' : {
        'name'    : 'taobao KEY',
        'group'   : '登录接口设置',
        'editor'  : 'text',
        'default' : '',
    }
}