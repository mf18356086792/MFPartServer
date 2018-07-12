#!/usr/bin/env python
# coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import re
import os
import datetime
import uuid
import hashlib
import time
#import pdb;pdb.set_trace()
#binary_data = request.files['uploadname'].stream.read
#img_data = StringIO(binary_data)
#img = Image.open(img_data)       
#plt.imshow(img)  
#plt.show() 


# 验证手机号是否正确
def judge_phone(phone):
    phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
    res = re.search(phone_pat, phone)
    if res:
        return True
    else:
        return False
    
    
# 生成uid
def get_uid():
    uid = str(uuid.uuid1()).replace("-", "")
    #print uid
    #print uuid.uuid3(namespace,name)
    #print uuid.uuid4()
    #print uuid.uuid5(namespace,name)    
    return uid


# 当前时间
def get_nowtime():
    nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
    return nowtime


# 当前时间戳
def get_timestamp():
    return int(time.time())


# 加密后的密码
def get_md5(password):
    new_pwd = hashlib.md5(password).hexdigest()
    return new_pwd
