#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time

DICT = {
    "任务完成率": "completion_rate",
    "任务延期率": "delay_rate",
    "待完成数": "pending",
    "延期数": "delay",
    "已完成数": "completed",
    "任务总数": "total",
    "时间": "time",
}


MISSION_URL = "https://degree.worktile.com/api/mission/analytics/panels/default-panel:team-summary/widgets/default-widget:team-summary"

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
    if result:
        outList = []
        outList.append({"completion_rate": result.get("completion_rate", 0)})
        outList.append({"delay_rate": result.get("delay_rate", 0)})
        outList.append({"pending": result.get("pending", 0)})
        outList.append({"delay": result.get("delay", 0)})
        outList.append({"completed": result.get("completed", 0)})
        outList.append({"total": result.get("total", 0)})
        outList.append({"time": time.strftime("%Y-%m-%d")})
        return outList
    return
    
if __name__ == "__main__":
    from login import login
    session = login(user="15984284317", pwd="1q2w3e4r5t6y")
    print parse(session)
    