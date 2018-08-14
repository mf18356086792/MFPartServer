#!/usr/bin/env python
# coding:utf-8

import MySQLdb
import flask
from flask import jsonify
from flask import request
from mf_login import login
from mf_register import register
from mf_userinfo import userinfo
from mf_headupload import headupload


# 开启服务
server = flask.Flask(__name__)
server.config['upload_folder'] = 'static/uploads/'  
server.config['allowed_extensions'] = set(['png', 'jpg', 'jpeg', 'gif'])



# 配置mysql连接
dbconfig = {'host': '127.0.0.1',
            'user': 'root',
            'passwd': 'mf911130',
            'charset': 'utf8',
            'db': 'PPYLLQ'
            }
dbcon = MySQLdb.connect(**dbconfig)
dbcon.autocommit(False)
dbcur = dbcon.cursor(MySQLdb.cursors.DictCursor)
dbcur.execute('set names utf8')


# 注册接口
@server.route('/register', methods=['post'])
def main_register():
    return register(dbcur).run(request)


# 登录接口
@server.route('/login', methods=['post'])
def main_login():
     return login(dbcur).run(request)
 
 
# 获取用户信息接口
@server.route('/userinfo', methods=['post'])
def main_userinfo():
    return userinfo(dbcur).run(request) 


# 修改用户信息接口
@server.route('/userinfo_edit', methods=['post'])
def main_userinfo_edit():
    return userinfo(dbcur).edit(request)


# 上传头像的接口
@server.route('/headupload', methods=['post'])
def main_headupload():
    return headupload(dbcur).run(request, server)




# 开启服务，用flask做接口服务
if __name__ == '__main__':
    # port可以指定端口，默认端口是5000
    # host写成0.0.0.0的话，其他人可以访问，代表监听多块网卡上面，默认是127.0.0.1
    #server.run(debug=False, port=80, host='0.0.0.0')
    server.run(debug=False, host='0.0.0.0') 
    #server.run(debug=False, host='118.25.95.202') 

