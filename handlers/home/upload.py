#!/usr/bin/env python
#-*- coding:utf8 -*-

# see: http://www.afewords.com/book/502e5cff3725176a91000004/catalog/16

import tornado.web
import tempfile
import Image
#import time
import logging

class UploadHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('home/upload.html')

    def post(slef):
        if self.request.files == {} or 'mypicutre' not in self.request.files:
            """ 看是否有文件且name为picture，跟HTML代码对应 """
            self.write('<script>alert("请选择图片")</script>')
            return

        image_type_list = ['image/gif', 'image/jpeg', 'image/pjpeg', 'image/bmp', 'image/png', 'image/x-png']
        send_file = self.request.files['mypicutre'][0]
        if send_file['content_type'] not in  image_type_list:
            self.write('<script>alert("仅支持jpg,jpeg,bmp,gif,png格式的图片！")</script>')
            return

        if len(send_file['body']) > 4*1024*1024:
            self.write('<script>alert("请上传4M以下的图片");</script>')
            return

        tmp_file = tempfile.NamedTemporaryFile(delete=True)
        tmp_file.write(send_file['body'])
        tmp_file.seek(0)

        try:
            image_one = Image.open(tmp_file.name)
        except IOError, error:
            logging.info(error)
            logging.info('+'*30 + '\n')
            tmp_file.close()
            self.write('<script>alert("图片不合法！")</script>')
            return

        image_path = "./static/picture/"
        image_format = send_file['filename'].split('.').pop().lower()
        tmp_name = image_path + str(int(time.time())) + image_format
        image_one.save(tmp_name)

        tmp_file.close()
        self.write('<script>alert("文件上传成功，路径为：" + image_path[1:])</script>')
        return

