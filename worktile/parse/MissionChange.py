#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time

DICT = {
    "time": "时间",
    "created": "新增任务数",
    "completed": "完成任务数"
}

MISSIONCHANGE_URL = "https://degree.worktile.com/api/mission/analytics/panels/default-panel:team-summary/widgets/default-widget:team-tasks-new-completed?from={}&to={}"

def parse(session):
    startTime = int(time.mktime(time.strptime(time.strftime("%a %b %d 00:00:00 %Y"))))
    toTime = startTime + 86399
    
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
        "Connection": "keep-alive"
    }
    
    response = session.get(MISSIONCHANGE_URL.format(startTime,toTime),headers=headers)
    htmlJson = response.json()
    data = htmlJson.get('data')
    if not data: return
    result = data.get("result")
    if result:
        outList = []
        outList.append({"time": time.strftime("%Y-%m-%d")})
        outList.append({"created": result[0].get("created")})
        outList.append({"completed": result[0].get("completed")})
        return outList
    return
    
if __name__ == "__main__":
    from login import login
    session = login(user="15984284317", pwd="1q2w3e4r5t6y")
    print parse(session)
    