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
import requests
import datetime
from bs4 import BeautifulSoup

from apscheduler.schedulers.blocking import BlockingScheduler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def movie(event):
    target_url = 'http://www.atmovies.com.tw/movie/next/0/'
    print('Start parsing movie ...')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('ul.filmNextListAll a')):
        if index == 20:
            return content
        title = data.text.replace('\t', '').replace('\r', '')
        link = "http://www.atmovies.com.tw" + data['href']
        content += '{}\n{}\n'.format(title, link)
    return content


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