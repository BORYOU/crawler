#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time

DICT = {
    "name": "成员", 
    "projectsNum": "项目数",
    "pending": "待完成",
    "delay": "已延期",
    "completed": "已完成",
    "total": "任务总数",
    "delayRate": "延误率",
    "completedRate": "成员完成度"
}

MISSION_URL = "https://degree.worktile.com/api/mission/analytics/panels/default-panel:team-members-progress/widgets/default-widget:team-members?__ps=20&__pn=0&__search="

def parse(session):
    
    aid = session.cookies.get("aid")
    s_58 = session.cookies.get("s-58ad6e78bc517f6097986b56")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
        "Host": "degree.worktile.com",
        "Referer": "https://degree.worktile.com/tasks/stat/default-panel:team-members-progress",
        "Cookie": "aid={}; s-58ad6e78bc517f6097986b56={}".format(aid, s_58),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding":"gzip",
        "Connection": "keep-alive"
    }
    
    response = session.get(MISSION_URL,headers=headers)
    htmlJson = response.json()
    data = htmlJson.get('data')
    if not data: return
    results = data.get("result")
    if results:
        for result in results:
            outList = {}
            try:
                name = result['details']['name']
            except:
                name = ""
            outList.update({"name":name})
            outList.update({"projectsNum": result.get("n_projects", 0)})
            outList.update({"pending": result.get("n_tasks_pending", 0)})
            outList.update({"delay": result.get("n_tasks_delay", 0)})
            outList.update({"completed": result.get("n_tasks_completed", 0)})
            outList.update({"total": result.get("n_tasks", 0)})
            outList.update({"delayRate": result.get("tasks_delay_rate", 0)})
            outList.update({"completedRate": ""})
            yield outList
    return
    
if __name__ == "__main__":
    from login import login
    session = login(user="15984284317", pwd="1q2w3e4r5t6y")
    for result in parse(session):
        print result
    