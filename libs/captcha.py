#!/usr/bin/env python
#-*- coding:utf-8 -*-

import urllib,urllib2
import os

GOOGLE_CAPTCHA_API = 'http://www.google.com/recaptcha/api/verify'

class RecaptchaResponse:
    def __init__(self, is_valid, error_code=None):
        self.is_valid = is_valid
        self.error_code = error_code

def check_google_captcha(request,remote_ip,recaptcha_challenge_field,recaptcha_response_field):
    if not (recaptcha_challenge_field and recaptcha_response_field):
        return RecaptchaResponse (is_valid = False, error_code = 'incorrect-captcha-sol')

    def encode_if_necessary(s):
        if isinstance(s, unicode):
            return s.encode('utf-8')
        return s

    params = urllib.urlencode ({
            'privatekey': encode_if_necessary('6Ld58vISAAAAANJmi5SeL_3JrVooeLGw2kmo7kK5'),  #这里是我的私钥
            'remoteip' :  encode_if_necessary(remote_ip), #远程主机ip
            'challenge':  encode_if_necessary(recaptcha_challenge_field),
            'response' :  encode_if_necessary(recaptcha_response_field),  #填入的数据
            })
    request = urllib2.Request(
        url = GOOGLE_CAPTCHA_API,
        data = params,
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "User-agent": "reCAPTCHA Python"
            }
        )

    httpresp = urllib2.urlopen(request)
    return_values = httpresp.read().splitlines();
    httpresp.close();
    return_code = return_values[0]

    if (return_code == "true"):
        return RecaptchaResponse(is_valid=True)
    else:
        return RecaptchaResponse(is_valid=False, error_code = return_values[1])
