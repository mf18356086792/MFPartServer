#!/usr/bin/env python
# coding:utf-8

import flask
from flask import jsonify
from flask import request
import mf_tool
from mf_tool import judge_phone
from mf_tool import get_md5
from mf_tool import get_timestamp
from mf_tool import get_nowtime


class login():
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
            if len(pwd) >= 6 : 
                
                # 查询注册的用户是否存在数据库
                md5_pwd = get_md5(pwd)
                select_sql_r = 'select * from reg_log_info where phone="%s" and password="%s";'%(phone, md5_pwd)
                res_mysql_r = self._db_select(select_sql_r)                              
                if res_mysql_r:
                    
                    nowtime = get_nowtime()
                    insertDic_r = {}
                    insertDic_r['equipment'] = equipment
                    insertDic_r['equipment_id'] = equipment_id
                    insertDic_r['system'] = system
                    insertDic_r['app_version'] = app_version
                    insertDic_r['login_time'] = nowtime
                    sql = 'update reg_log_info set equipment="%s",equipment_id="%s",system="%s",app_version="%s",login_time="%s" where phone="%s" and password="%s";'%(equipment,equipment_id,system,app_version,nowtime,phone, md5_pwd)
                    self._dbcur.execute(sql)
                    
                    data = {}
                    data['uid'] = res_mysql_r[0]['uid']
                    data['phone'] = res_mysql_r[0]['phone']
                    return jsonify({"code":1, "msg": "登录成功", "data":data, 'time': get_timestamp()})
                else:
                    return jsonify({"code":0, "msg":"手机号或密码输入有误", "data":'', 'time': get_timestamp()})
            else:
                return jsonify({"code": 0, "msg": "密码不能少于6位", "data":'', 'time': get_timestamp()})
        else:
            return jsonify({"code": 0, "msg": "请求方式不正确", "data":'', 'time': get_timestamp()})



