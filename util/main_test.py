import os
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

from flindUtil import ptt_beauty,ptt_gossiping,ptt_AC_In,ptt_find,findPTT,getGoldCorridor
from flask import Flask, request, abort


app = Flask(__name__)
@app.route("/")
def hello():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')       
    return "Hello !:"+now

sched = BlockingScheduler()
@sched.scheduled_job('interval', minutes=20) #定期執行，每X分鐘執行一次
def job_GBF():
    print('Start job_GBF') #運行時打印出此行訊息
    sReturn = ptt_find("GBF")
    if len(sReturn) > 0:
        pass
    else:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
        sReturn = "{}--查無結果".format(now)

    print('END job_GBF:'+sReturn)#運行時打印出此行訊息

@sched.scheduled_job('interval', minutes=10) #定期執行，每X分鐘執行一次
def job_TypeMoon():
    print('Start job_TypeMoon') #運行時打印出此行訊息
    sReturn = ptt_find("TypeMoon")
    if len(sReturn) > 0:
        pass
    else:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
        sReturn = "{}--查無結果".format(now)

    print('END job_TypeMoon:'+sReturn)#運行時打印出此行訊息

@sched.scheduled_job('cron', hour='10,14,18')
def job_GoldCorridor():
    print('Start scheduled_job') #運行時打印出此行訊息
    sReturn = getGoldCorridor()
    if len(sReturn) > 0:
        pass
    else:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
        sReturn = "{}--查無結果".format(now)

    print('END scheduled_job:'+sReturn)#運行時打印出此行訊息


sched.start()


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])