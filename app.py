from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
import re
import json
# import twitter
import datetime
from bs4 import BeautifulSoup

from apscheduler.schedulers.blocking import BlockingScheduler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


app = Flask(__name__)

# 填入你的 message api 資訊
# Channel access token
line_bot_api = LineBotApi('kKnqWh2H18SIBXfwovAY5ScSfsH9fOOTxVAHkV/IRBkHi+kg+j5lJUKmnbMrcHQKdqnESugkPYahGCUXFOOC9cUWW0uUZgGSifYDeygynCdaZE7ABXgLfJ2kRKLyJeGujLVag6Df61W5pHQsPLYKxwdB04t89/1O/w1cDnyilFU=')
# Channel secret
handler = WebhookHandler('fedfc3d7af2d1fd102ddf854fefd7141')

#User ID
to_myuserid='Ud0d8235b4696d1cab3da6b1e46f39598'

import random
list4 = list(range(0, 4))

@app.route("/")
def hello():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')       
    return "Hello !:"+now

# 設定你接收訊息的網址，如 https://wlinebot7test.herokuapp.com/callback
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body, "Signature: " + signature)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("Handle: reply_token: " + event.reply_token + ", message: " + event.message.text)
    msg = event.message.text
    msg = msg.encode('utf-8')

    # content = "你肚子有回聲蟲: {}".format(event.message.text)
    content = confirmMessage(event)
    
    #reply_token message to one user
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=content))
   
    userId = event.source.user_id
    contentrd = "ID: {}傳給LINE Bot: {} ，系統回傳:{}".format(userId, event.message.text,content)

    print("push_message="+contentrd)
    #push message to one user
    line_bot_api.push_message(
        to_myuserid,
        TextSendMessage(text=contentrd))

def confirmMessage(event):
    sReturn = ""
    sConfirmText = event.message.text
   
    iRandom = random.sample(list4, 1)[0]
<<<<<<< HEAD
    print("123=")
=======
>>>>>>> ce8c5c1b15fdec9313ce46fa68562b6aee95ca9c
    print("iRandom={}".format(iRandom))
    print("sConfirmText={}".format(sConfirmText.find("找PTT")))

    if sConfirmText.find("想吃") >= 0 and sConfirmText.find("不想吃") == -1:
        sReturn = switch(iRandom)
    elif  sConfirmText.find("要吃") >= 0 and sConfirmText.find("不要吃") == -1:
        sReturn = switch(iRandom)
<<<<<<< HEAD
    elif  sConfirmText.find("find") >= 1 :
        print("find={}".format(sConfirmText))
        sReturn = "你肚子有回聲蟲: {}".format(event.message.text)
=======
    elif  sConfirmText.find("找PTT") >= 0 and sConfirmText.find("不找PTT") == -1:
        print("找PTT")
        sReturn = scheduled_job(event)
>>>>>>> ce8c5c1b15fdec9313ce46fa68562b6aee95ca9c
    else:
        sReturn = "你肚子有回聲蟲: {}".format(event.message.text)

    # print("找789")
    # sReturn = scheduled_job(sReturn)

    print("sReturn")
    return sReturn

    

def switch(x):
    print("x={}".format(x))
    return {
        0 :">>>>今天吃麥當當",
        1 :">>>>今天吃KFC",
        2 :">>>>今天吃頂呱呱",
        3 :">>>>今天吃拿坡里",
        4 :">>>>今天吃八方",
    }.get(x,">>>>今天吃XXX")

def notification(event, title, link):
    # with open('data/notify_list.json', 'r') as file:
    #     notify_list = json.load(file)
    # if len(notify_list) == 0:
    #     return False
    
    content = "{}\n{}".format(title, link)
        #push message to one user
    line_bot_api.push_message(
        to_myuserid,
        TextSendMessage(text=content))

    # line_bot_api.multicast(to_myuserid, TextSendMessage(text=content))
    return True


def scheduled_job(event):
    print("Action scheduled_job")
    # Chrome
    options = Options()
    options.binary_location = '/app/.apt/usr/bin/google-chrome'
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(chrome_options=options)
    # driver.implicitly_wait(10)
    # driver.set_page_load_timeout(60)

    sMessgge = ""
    sfind = event.message.text
    sfind = sfind.replace("找PTT","")
    sfind = sfind.replace(":","").replace(" ","")

    # driver.get('https://www.ptt.cc/bbs/Gamesale/index.html')
    # re_gs_title = re.compile(r'\[PS4\s*\]\s*售.*pro.*', re.I)
    # re_gs_id = re.compile(r'.*\/Gamesale\/M\.(\S+)\.html')

    driver.get('https://www.ptt.cc/bbs/TypeMoon/index.html')
    soup = BeautifulSoup(driver.page_source, "html.parser")
    re_gs_title = re.compile(r'\['+sfind+'\s*\]\s*', re.I)
    re_gs_id = re.compile(r'.*\/TypeMoon\/M\.(\S+)\.html')

    match = []
    for article in soup.select('.r-list-container .r-ent .title a'):
        title = article.string
        if re_gs_title.match(title) != None:
            link = 'https://www.ptt.cc' + article.get('href')
            article_id = re_gs_id.match(link).group(1)
            match.append({'title':title, 'link':link, 'id':article_id})

    if len(match) > 0:
        with open('data/history/gamesale.json', 'r+') as file:
            print (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'open')

            history = json.load(file)
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')       
            new_flag = False
            for article in match:
                if article['id'] in history:
                    continue
                new_flag = True
                history.append(article['id'])

                print("{}: New Article: {} {}".format(now, article['title'], article['link']))
                notification(event,article['title'], article['link'])
                

            if new_flag == True:
                file.seek(0)
                file.truncate()
                file.write(json.dumps(history))
            else:
                print("{}: Nothing".format(now))

        sMessgge = "{},查成功:{}".format(sfind,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    else:
        sMessgge = "{},查無結果:{}".format(sfind,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    print("Action scheduled_job_END")

    return sMessgge



import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])


# Job
sched = BlockingScheduler()
sched.add_job(func=scheduled_job, trigger='cron', second='*/3000')
sched.start()
