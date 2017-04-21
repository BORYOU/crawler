#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time

DICT = {
    "name": "项目",
    "starttime": "开始时间",
    "endtime": "结束时间",
    "chargeman": "负责人",
    "status": "状态",
    "pending": "待完成",
    "delay": "延期任务",
    "completed": "已完成",
    "Rate": "项目进度"
}

MISSION_URL = "https://degree.worktile.com/api/mission/analytics/panels/default-panel:team-projects-progress/widgets/default-widget:team-projects?__pn=0&__ps=20"
def parse(session):
    
    aid = session.cookies.get("aid")
    s_58 = session.cookies.get("s-58ad6e78bc517f6097986b56")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
        "Host": "degree.worktile.com",
        "Referer": "https://degree.worktile.com/tasks/stat/default-panel:team-summary",
        "Cookie": "aid={}; s-58ad6e78bc517f6097986b56={}".format(aid, s_58),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding":"gzip",
        "Content-Type": "application/json;charset=utf-8",
        "Connection": "keep-alive"
    }
    
    response = session.get(MISSION_URL,headers=headers)
    htmlJson = response.json()
    data = htmlJson.get('data')
    if not data: return
    result = data.get("result")
    if not result: return
    projects = result.get("project")
    if projects:
        for project in projects:
            outList = {}
            outList.update({"name": result.get("name", "")})
            outList.update({"starttime": ""})
            outList.update({"endtime": ""})
            outList.update({"chargeman": ""})
            outList.update({"status": ""})
            outList.update({"pending": result.get("pending", "0")})
            outList.update({"delay": result.get("delay", "0")})
            outList.update({"completed": result.get("completed", "0")})
            outList.update({"Rate": result.get("Rate", 0)})
            yield outList
    return
    
if __name__ == "__main__":
    from login import login
    session = login(user="15984284317", pwd="1q2w3e4r5t6y")
    for project in parse(session):
        print project
    