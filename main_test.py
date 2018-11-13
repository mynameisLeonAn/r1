import os
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

from util.flindUtil import ptt_beauty,ptt_gossiping,ptt_AC_In,ptt_find,findPTT,getGoldCorridor,getRateCorridor,getRateArrivalNotice
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

@sched.scheduled_job('interval', minutes=20)
def job_GoldCorridor():
    print('Start job_GoldCorridor') #運行時打印出此行訊息
    sReturn = getGoldCorridor()
    if len(sReturn) > 0:
        pass
    else:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
        sReturn = "{}--查無結果".format(now)

    print('END job_GoldCorridor:'+sReturn)#運行時打印出此行訊息


@sched.scheduled_job('interval', minutes=30)
def job_RateCorridor():
    print('Start job_RateCorridor') #運行時打印出此行訊息
    sReturn = getRateCorridor('USD#@#JPY')
    if len(sReturn) > 0:
        pass
    else:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
        sReturn = "{}--查無結果".format(now)

    print('END job_RateCorridor:'+sReturn)#運行時打印出此行訊息

@sched.scheduled_job('interval', minutes=0.1)
def job_RateArrivalNotice():
    print('Start job_RateArrivalNotice') #運行時打印出此行訊息
    sReturn = getRateArrivalNotice('USD#@#USD#@#JPY',"30.31#@#30.31#@#0.28","即期#@#現金#@#現金")
    if len(sReturn) > 0:
        pass
    else:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
        sReturn = "{}--查無結果".format(now)

    print('END job_RateArrivalNotice:'+sReturn)#運行時打印出此行訊息

sched.start()


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])