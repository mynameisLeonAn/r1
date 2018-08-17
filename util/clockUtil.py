import os
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

from flindUtil import ptt_beauty,ptt_gossiping,ptt_AC_In,ptt_find,findPTT


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

    print('END job_GBF:')#運行時打印出此行訊息

@sched.scheduled_job('interval', minutes=20) #定期執行，每X分鐘執行一次
def job_TypeMoon():
    print('Start job_TypeMoon') #運行時打印出此行訊息
    sReturn = ptt_find("TypeMoon")
    if len(sReturn) > 0:
        pass
    else:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
        sReturn = "{}--查無結果".format(now)

    print('END job_TypeMoon:')#運行時打印出此行訊息
 
sched.start()