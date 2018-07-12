#!/usr/bin/env python
# coding:utf-8

import flask
from flask import jsonify
from flask import request
import sys
from mf_tool import judge_phone
from mf_tool import get_md5
from mf_tool import get_timestamp
from mf_tool import get_nowtime


class userinfo():
    def __init__(self, dbcur):
        self._dbcur = dbcur
        
    
    def _db_select(self, sql):
        try:
            self._dbcur.execute(sql)
        except Exception, e:
            print e
            sys.exit(0)
        return self._dbcur.fetchall()
    
        
    def run(self, request):
        # 判断接口的请求方式是GET还是POST
        if request.method == 'POST':
            # 获取请求参数是json格式，返回结果是字典
            uid = request.values.get('uid')
            select_sql_u = 'select * from user_info where uid = "%s";'%uid
            res_sql_u = self._db_select(select_sql_u)
            data = {}
            data['phone'] = res_sql_u[0]['phone']
            data['nickname'] = res_sql_u[0]['nickname']        
            data['face_url'] = request.host_url+res_sql_u[0]['face_url']
            data['sex'] = res_sql_u[0]['sex']
            data['city'] = res_sql_u[0]['city']                    
            return jsonify({"code":1, "msg": "获取成功", "data":data, 'time': get_timestamp()})
        else:
            return jsonify({"code": 0, "msg": "请求方式不正确", "data":'', 'time': get_timestamp()})
        
        
    def edit(self, request):
        # 判断接口的请求方式是GET还是POST
        if request.method == 'POST':
            # 获取请求参数是json格式，返回结果是字典
            uid = request.values.get('uid')
            profile_type = request.values.get('profile_type')
            new_profile = request.values.get('new_profile')
            nowtime = get_nowtime()
            
            sql = 'update user_info set %s="%s", reload_time="%s" where uid="%s";'%(profile_type,new_profile,nowtime,uid)
            self._dbcur.execute(sql)
            
            select_sql_u = 'select * from user_info where uid = "%s";'%uid
            res_sql_u = self._db_select(select_sql_u)
            data = {}
            data['phone'] = res_sql_u[0]['phone']
            data['nickname'] = res_sql_u[0]['nickname']        
            data['face_url'] = request.host_url+res_sql_u[0]['face_url']
            data['sex'] = res_sql_u[0]['sex']
            data['city'] = res_sql_u[0]['city']                    
            return jsonify({"code":1, "msg": "获取成功", "data":data, 'time': get_timestamp()})
        else:
            return jsonify({"code": 0, "msg": "请求方式不正确", "data":'', 'time': get_timestamp()})


