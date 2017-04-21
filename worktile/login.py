#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from timeout_session import Session
from exception_handler import CodeException

import time
import json
import hashlib

FIRAT_URL = "https://degree.worktile.com/signin"
LOGIN_URL = "https://degree.worktile.com/api/user/signin?t={}"

def md5(string):
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()

def get_session(session, user_name, passwd):
    session.get(FIRAT_URL)
    aid = session.cookies.items()[0][-1]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
        "Host": "degree.worktile.com",
        "Referer": "https://degree.worktile.com/signin",
        "Origin": "https://degree.worktile.com",
        "Cookie": "aid={}".format(aid),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding":"gzip",
        "Content-Type": "application/json;charset=utf-8",
        "Connection": "keep-alive",
        "Content-Length":"122"
    }
    
    password = md5(passwd)
    #"ede6b50e7b5826fe48fc1f0fe772c48f"
    
    data = {
        "team_id": "58ad6e78bc517f6097986b56",
        "name": user_name,
        "password": password,
        "locale": "zh-cn"
    }
    dataJson = json.dumps(data)
    timeStr = int(round(time.time(),3)*1000)
    passUrl = LOGIN_URL.format(timeStr)
    response = session.post(passUrl, data = dataJson, headers = headers)
    responseJson = response.json()
    code = responseJson.get("code",None)
    if None == code or code != 200:
        raise CodeException(-2, "用户名或密码错误")
        
def login(**kwargs):
    user_name = kwargs.get("user", "")
    password = kwargs.get("pwd", "")
    if not user_name:
        raise CodeException(-4, "参数user缺失")
    if not password:
        raise CodeException(-4, "参数pwd缺失")
    session = Session()
    get_session(session, user_name, password)
    return session


if __name__ == "__main__":
    print login(user="15984284317", pwd="1q2w3e4r5t6y")