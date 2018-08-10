from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, VideoSendMessage,
    TemplateSendMessage,ButtonsTemplate,MessageTemplateAction,ImageSendMessage,
    PostbackTemplateAction
)
from linebot.models import *
import os
import re
import json
# import twitter
import datetime

# ================================
# python 會先去這裡找你企圖要 import 的.py 檔案
# 如果再裡面沒有找到相關檔案的話就會 raise 錯誤訊息
# ================================
# import sys
# sys.path.append("../util")
# import lineUtil
from util.flindUtil import (movie,findPTT)
from util.flindUtil import finRadarUrl
from util.flindUtil import ptt_beauty,ptt_gossiping,ptt_AC_In
# ================================

import random
list4 = list(range(0, 4))

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
        buttons_template = VideoSendMessage(
            original_content_url="https://r2---sn-ipoxu-un5z.googlevideo.com/videoplayback?id=o-AOytmnkLGEmQgZIK9dVXD2xXwK7eNo33O8df0fU7Td6y&ei=7dosW7T9GpjdNonOjIAF&pl=21&ipbits=0&ip=107.178.194.15&ratebypass=yes&dur=258.670&c=WEB&lmt=1528903208423955&source=youtube&clen=9673166&expire=1529687885&key=cms1&mime=video%2Fmp4&gir=yes&requiressl=yes&fexp=23709359&sparams=clen,dur,ei,expire,gir,id,ip,ipbits,itag,lmt,mime,mip,mm,mn,ms,mv,pcm2cms,pl,ratebypass,requiressl,source&signature=20E47DEDD0606C2CA4B36E5DC1A3E572589DDACF.2EA5096770EDBF7FFE337DF8070B383520A01DEF&itag=18&utmg=ytap1&title=(Tubidy.io)%E3%80%90Fate-Grand+Order%E3%80%91%E3%80%8E%E3%81%90%E3%81%A0%E3%81%90%E3%81%A0%E5%B8%9D%E9%83%BD%E8%81%96%E6%9D%AF%E5%A5%87%E8%AD%9A%E3%80%8F%E3%83%86%E3%83%BC%E3%83%9E%E6%9B%B2%E3%80%8C%E4%BA%8C%E8%80%85%E7%A9%BF%E4%B8%80%E3%80%8D+by+%E5%85%AD%E8%8A%B1&cms_redirect=yes&mip=60.250.154.133&mm=31&mn=sn-ipoxu-un5z&ms=au&mt=1529666370&mv=m&pcm2cms=yes"
            ,preview_image_url="https://78.media.tumblr.com/82890f75107edef4fb5b4a4af6c2cd40/tumblr_oxq1209UsI1uzwbyjo1_540.gif"
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        print("找推圖")
    elif  sConfirmText.find("近期上映電影") >= 0 and sConfirmText.find("不找近期上映電影") == -1:
        sReturn = movie(event)   
    elif  sConfirmText.find("Taiwan radar") >= 0 :
        url = finRadarUrl(event)
        if len(url) > 0:
            buttons_template = ImageSendMessage(
                original_content_url=url,
                preview_image_url=url
            )
            line_bot_api.reply_message(event.reply_token, buttons_template)
        else:
            sReturn = "查無結果"   
    elif  sConfirmText.find("ptt_beauty") >= 0 :
        sReturn = ptt_beauty()
        if len(sReturn) > 0:
            pass
        else:
            sReturn = "查無結果"
    elif  sConfirmText.find("ptt_gossiping") >= 0 :
        sReturn = ptt_gossiping()
        if len(sReturn) > 0:
            pass
        else:
            sReturn = "查無結果"
    elif  sConfirmText.find("ptt_AC_In") >= 0 :
        sReturn = ptt_AC_In()
        if len(sReturn) > 0:
            pass
        else:
            sReturn = "查無結果"           
    elif  sConfirmText.find("help") >= 0:
        print("help")
        helpMessage(event)
    else:
        pass
        # sReturn = "你肚子有回聲蟲: {}".format(event.message.text)


    print("sReturn")
    return sReturn

def helpMessage(event):    
    print("Buttons Template")       

    button_template_message =ButtonsTemplate(
        thumbnail_image_url='https://78.media.tumblr.com/82890f75107edef4fb5b4a4af6c2cd40/tumblr_oxq1209UsI1uzwbyjo1_540.gif',
        title='Menu', 
        text="LIN_BOT功能",
        image_size="cover",
        actions=[
            #   PostbackTemplateAction 點擊選項後，
            #   除了文字會顯示在聊天室中，
            #   還回傳data中的資料，可
            #   此類透過 Postback event 處理。
            PostbackTemplateAction(
                label='想吃or要吃-隨機垃圾食物', 
                text='今天要吃什麼',
                data='action=buy&itemid=1'
            ),
            PostbackTemplateAction(
                label='找PTT TypeMoon 日GO', 
                text='找PTT :TypeMoon>日GO',
                data='action=buy&itemid=1'
            ),
            PostbackTemplateAction(
                label='找PTT TypeMoon 兩頁', 
                text='找PTT :TypeMoon',
                data='action=buy&itemid=1'
            ),
            MessageTemplateAction(
                label='近期上映電影',
                text='近期上映電影'
            ),
        ]
    )
                        
    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
            alt_text="Template Example",
            template=button_template_message
        )
    )

    

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
