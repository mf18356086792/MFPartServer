#!/usr/bin/env python
# coding:utf-8

import flask
from flask import jsonify
from flask import request
from mf_tool import judge_phone 
from mf_tool import get_uid 
from mf_tool import get_nowtime
from mf_tool import get_md5
from mf_tool import get_timestamp


class register():
    def __init__(self, dbcur):
        self._dbcur = dbcur
        

    def _db_select(self, sql):
        try:
            self._dbcur.execute(sql)
        except Exception, e:
            print e
            sys.exit(0)
        return self._dbcur.fetchall()
        
        
    def construct_insert_sql(self, table, data, db=None):
        fields = '`' + '`,`'.join(data.keys()) + '`'
        values = []
        for v in data.values():
            if not v:
                v = ''
            if type(v) == int or type(v) == long:
                values.append(v.__str__())
            elif v == "now()":
                values.append(v)
            else:
                values.append("'%s'" % v.replace("'", " ").replace("\\", "\\\\"))
        if db:
            sql = 'INSERT INTO `%s`.`%s` (%s) VALUES (%s)' % (db, table, fields, ",".join(values))
        else:
            sql = 'INSERT INTO `%s` (%s) VALUES (%s)' % (table, fields, ",".join(values))
        return sql
    
    
    def run(self, request):
        
        # 判断接口的请求方式是GET还是POST
        if request.method == 'POST':
            
            # 获取请求参数是json格式，返回结果是字典
            phone = request.values.get('phone')
            pwd = request.values.get('pwd')
            equipment = request.values.get('equipment')
            equipment_id = request.values.get('equipmentid')
            system = request.values.get('system')
            app_version = request.values.get('appversion')
            
            res = judge_phone(phone)
            if not res:
                return jsonify({"code":0, "msg": "手机号输入有误", "data":"", 'time': get_timestamp()})
            
            # 判断输入的用户名、密码都不为空
            if len(pwd) >= 6: 
                select_sql_r = 'select * from reg_log_info where phone = "%s";'%phone
                # 查询注册的用户是否存在数据库，如果存在，则username不为空，否则username为空
                res_sql_r = self._db_select(select_sql_r)
                if res_sql_r:
                    return jsonify({"code":0, "msg": "该手机号已注册", "data":"", 'time': get_timestamp()})
                else:
                    uid = get_uid()
                    nowtime = get_nowtime()
                    md5_pwd = get_md5(pwd)
                    insertDic_r = {}
                    insertDic_r['uid'] = uid
                    insertDic_r['phone'] = phone
                    insertDic_r['password'] = md5_pwd
                    insertDic_r['equipment'] = equipment
                    insertDic_r['equipment_id'] = equipment_id
                    insertDic_r['system'] = system
                    insertDic_r['app_version'] = app_version
                    insertDic_r['register_time'] = nowtime
                    insertDic_r['login_time'] = nowtime
                    sql = self.construct_insert_sql('reg_log_info', insertDic_r)
                    self._dbcur.execute(sql)
                    
                    
                    insertDic_u = {}
                    insertDic_u['uid'] = uid
                    insertDic_u['phone'] = phone
                    insertDic_u['nickname'] = '用户'+phone
                    insertDic_u['reload_time'] = nowtime
                    sql = self.construct_insert_sql('user_info', insertDic_u)
                    self._dbcur.execute(sql)                
                    
                    
                    data = {}
                    data['uid'] = uid
                    data['phone'] = phone
                    return jsonify({"code": 1, "msg": "注册成功", "data":data, 'time': get_timestamp()})
            else:
                return jsonify({"code": 0, "msg": "密码不能少于6位", "data":"", 'time': get_timestamp()})
        else:
            return jsonify({"code": 0, "msg": "请求方式不正确", "data":"", 'time': get_timestamp()})


