from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage,
)
from linebot.models import *
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

    content = confirmMessage(event)
    if content != None:
        #reply_token message to one user
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
   
    userId = event.source.user_id
    contentrd = "ID: {}傳給LINE Bot: {} ，系統回傳:\n{}".format(userId, event.message.text,content)

    print("push_message="+contentrd)
    #push message to one user
    line_bot_api.push_message(
        to_myuserid,
        TextSendMessage(text=contentrd))

def confirmMessage(event):
    sReturn = ""
    sConfirmText = event.message.text

    if sConfirmText.find("想吃") >= 0 and sConfirmText.find("不想吃") == -1:
        sReturn = switch()
    elif  sConfirmText.find("要吃") >= 0 and sConfirmText.find("不要吃") == -1:
        sReturn = switch()
    elif  sConfirmText.find("找PTT") >= 0 and sConfirmText.find("不找PTT") == -1:
        print("找PTT")
        sReturn = findPTT(event)
    elif  sConfirmText.find("找推圖") >= 0 and sConfirmText.find("不找推圖") == -1:
        buttons_template = TemplateSendMessage(
            alt_text='找推圖 template',
            template=ButtonsTemplate(
                title='選擇服務',
                text='請選擇',
                thumbnail_image_url='https://78.media.tumblr.com/82890f75107edef4fb5b4a4af6c2cd40/tumblr_oxq1209UsI1uzwbyjo1_540.gif',
                actions=[
                    MessageTemplateAction(
                        label='PTT 表特版 近期大於 10 推的文章',
                        text='PTT 表特版 近期大於 10 推的文章'
                    ),
                    MessageTemplateAction(
                        label='來張 imgur 正妹圖片',
                        text='來張 imgur 正妹圖片'
                    ),
                    MessageTemplateAction(
                        label='隨便來張正妹圖片',
                        text='隨便來張正妹圖片'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        print("找推圖")
        
    elif  sConfirmText.find("help") >= 0:
        print("help")
        sReturn = helpMessage()
    else:
        pass
        # sReturn = "你肚子有回聲蟲: {}".format(event.message.text)


    print("sReturn")
    return sReturn

def helpMessage():
    shelpMessage = "LIN_BOT功能: \n *{} \n *{} \n *{}"
    sToolName1 = "想吃or要吃 :隨機垃圾食物"
    sToolName2 = "找PTT :XX版>[XX]標籤，ex: 找PTT :Gossiping>問卦、找PTT :TypeMoon>日GO"
    sToolName3 = "找推特圖 :#XX標籤，ex: 找推圖 :#FGO"

    return shelpMessage.format(sToolName1,sToolName2,sToolName3)

def switch():
    iRandom = random.sample(list4, 1)[0]
    print("x={}".format(iRandom))
    return {
        0 :">>>>今天吃麥當當",
        1 :">>>>今天吃KFC",
        2 :">>>>今天吃頂呱呱",
        3 :">>>>今天吃拿坡里",
        4 :">>>>今天吃八方",
    }.get(iRandom,">>>>今天吃XXX")

def notification(title, link):
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

def findPTT(event):
    print("Action findPTT")
    # Chrome
    options = Options()
    options.binary_location = '/app/.apt/usr/bin/google-chrome'
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(chrome_options=options)

    sMessgge = ""
    sNotificationMulticast = ""
    sfind = event.message.text
    sfind = sfind.replace("找PTT","")
    sfind = sfind.replace(":","").replace(" ","").replace("[","").replace("]","")
    slfindList = sfind.split(">")

    if len(slfindList) < 2 :
        sMessgge = "{},查詢格式有誤，請參閱help:{}".format(sfind,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    else:
        print("slfindList[0]="+slfindList[0])
        print("slfindList[1]="+slfindList[1])

        driver.get('https://www.ptt.cc/bbs/{}/index.html'.format(slfindList[0]))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        re_gs_title = re.compile(r'\['+slfindList[1]+'\s*\]\s*', re.I)
        re_gs_id = re.compile(r'.*\/'+slfindList[0]+'\/M\.(\S+)\.html')

        match = []
        for article in soup.select('.r-list-container .r-ent .title a'):
            title = article.string
            if re_gs_title.match(title) != None:
                link = 'https://www.ptt.cc' + article.get('href')
                article_id = re_gs_id.match(link).group(1)
                match.append({'title':title, 'link':link, 'id':article_id})

        if len(match) > 0:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')       
                
            for article in match:
                print("{}: New Article: {} {}".format(now, article['title'], article['link']))
                sNotificationMulticast +="{}\n{}\n".format(article['title'], article['link'])

            sMessgge = "{},查成功:{}".format(sfind,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        else:
            sMessgge = "{},查無結果:{}".format(sfind,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        if len(match) > 0:
            sMessgge = sNotificationMulticast

    print("Action findPTT_END")

    return sMessgge

def scheduled_job():
    print("Action scheduled_job")
    # Chrome
    options = Options()
    options.binary_location = '/app/.apt/usr/bin/google-chrome'
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(chrome_options=options)

    # driver.get('https://www.ptt.cc/bbs/Gamesale/index.html')
    # re_gs_title = re.compile(r'\[PS4\s*\]\s*售.*pro.*', re.I)
    # re_gs_id = re.compile(r'.*\/Gamesale\/M\.(\S+)\.html')

    driver.get('https://www.ptt.cc/bbs/{}/index.html'.format("TypeMoon"))
    soup = BeautifulSoup(driver.page_source, "html.parser")
    re_gs_title = re.compile(r'\[日GO\s*\]\s*', re.I)
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
                notification(article['title'], article['link'])
                
            if new_flag == True:
                file.seek(0)
                file.truncate()
                file.write(json.dumps(history))
            else:
                print("{}: Nothing".format(now))

    print("Action scheduled_job_END")

    return True

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])


# Job
sched = BlockingScheduler()
sched.add_job(func=scheduled_job, trigger='cron', second='*/3000')
sched.start()
