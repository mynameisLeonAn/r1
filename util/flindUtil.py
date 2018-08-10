import os
import re
import json
import requests
import datetime
from bs4 import BeautifulSoup
import time
import urllib3

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
        sMessgge = findPTT2Page(driver,slfindList,sfind)
        # sMessgge = "{},查詢格式有誤，請參閱help:{}".format(sfind,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    else:
        print("slfindList[0]="+slfindList[0])
        print("slfindList[1]="+slfindList[1])
        try:
            driver.get('https://www.ptt.cc/bbs/{}/index.html'.format(slfindList[0]), verify=False)
            # soup = BeautifulSoup(driver.page_source, "html.parser")
            soup = over18(slfindList[0])
            re_gs_title = re.compile(r'\['+slfindList[1]+'\s*\]\s*', re.I)
            re_gs_id = re.compile(r'.*\/'+slfindList[0]+'\/M\.(\S+)\.html')

            match = []

            page_term = 2  # crawler count
            all_page_url = soup.select('.btn.wide')[1]['href']
            start_page = get_page_number(all_page_url)
            index_list = []
            for page in range(start_page, start_page - page_term, -1):
                page_url = 'https://www.ptt.cc/bbs/{}/index{}.html'.format(slfindList[0], page)
                index_list.append(page_url)

            while index_list:
                index = index_list.pop(0)
                driver.get(index, verify=False)
                soup2 = BeautifulSoup(driver.page_source, "html.parser")
                
                # 如網頁忙線中,則先將網頁加入 index_list 並休息1秒後再連接
                if driver.status_code != 200:
                    time.sleep(1)
                else:
                    time.sleep(0.05)
                
                for article in soup2.select('.r-list-container .r-ent .title a'):
                    title = article.string
                    if re_gs_title.match(title) != None:
                        link = 'https://www.ptt.cc' + article.get('href')
                        article_id = re_gs_id.match(link).group(1)
                        match.append({'title':title, 'link':link, 'id':article_id})

            if len(match) > 0:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')       
                    
                for article in match:
                    ilen = len(sNotificationMulticast)+len(article['title'])*3+len(article['link'])
                    # Line only 0~2000
                    if ilen < 2000:
                        print(">>>>>>{}: New Article: {} {}".format(ilen, article['title'], article['link']))
                        sNotificationMulticast +="{}\n{}\n".format(article['title'], article['link'])

                sMessgge = "{},查成功:{}".format(sfind,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            else:
                sMessgge = "{},查無結果:{}".format(sfind,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            if len(match) > 0:
                sMessgge = sNotificationMulticast
                
        except :
            sMessgge = "{},查無結果:{}".format(sfind,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    print("Action findPTT_END")

    return sMessgge

def findPTT2Page(driver,slfindList,sfind):
    print("Action findPTT2Page")
    print("slfindList[0]="+slfindList[0])
    sNotificationMulticast = ""
    match = []

    # re_gs_title = re.compile(r'\['+slfindList[1]+'\s*\]\s*', re.I)
    re_gs_id = re.compile(r'.*\/'+slfindList[0]+'\/M\.(\S+)\.html')
    driver.get('https://www.ptt.cc/bbs/{}/index.html'.format(slfindList[0]), verify=False)
    soup = over18(slfindList[0])

    page_term = 2  # crawler count
    try:
        all_page_url = soup.select('.btn.wide')[1]['href']
        start_page = get_page_number(all_page_url)
      
  
        index_list = []
        for page in range(start_page, start_page - page_term, -1):
            page_url = 'https://www.ptt.cc/bbs/{}/index{}.html'.format(slfindList[0], page)
            index_list.append(page_url)

        while index_list:
            index = index_list.pop(0)
            driver.get(index, verify=False)
            soup2 = BeautifulSoup(driver.page_source, "html.parser")
             # 如網頁忙線中,則先將網頁加入 index_list 並休息1秒後再連接
            if driver.status_code != 200:
                time.sleep(1)
            else:
                time.sleep(0.05)

            for article in soup2.select('.r-list-container .r-ent .title a'):
                title = article.string
                # if re_gs_title.match(title) != None:
                link = 'https://www.ptt.cc' + article.get('href')
                article_id = re_gs_id.match(link).group(1)
                match.append({'title':title, 'link':link, 'id':article_id})

        if len(match) > 0:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')       
                
            for article in match:
                ilen = len(sNotificationMulticast)+len(article['title'])*3+len(article['link'])
                # Line only 0~2000
                if ilen < 2000:
                    print(">>>>>>{}: New Article: {} {}".format(ilen, article['title'], article['link']))
                    sNotificationMulticast +="{}\n{}\n".format(article['title'], article['link'])

                sMessgge = "{},查成功:{}".format(sfind,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            else:
                sMessgge = "{},查無結果:{}".format(sfind,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        if len(match) > 0:
            sMessgge = sNotificationMulticast

    except :
        sMessgge = "{},查無結果:{}".format(sfind,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    print("Action findPTT2Page_END")

    return sMessgge

def get_page_number(content):
    start_index = content.find('index')
    end_index = content.find('.html')
    page_number = content[start_index + 5: end_index]
    return int(page_number) + 1



def finRadarUrl(event):
    url = ""
    print("Action finRadarUrl")
    # # Chrome
    # options = Options()
    # options.binary_location = '/app/.apt/usr/bin/google-chrome'
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    # options.add_argument('--no-sandbox')
    # driver = webdriver.Chrome(chrome_options=options)

    tag = re.compile(r'/V7/observe/radar/Data/HD_Radar/CV1_1000_\d{12}.png')
    quote_page = 'http://www.cwb.gov.tw/V7/js/HDRadar_1000_n_val.js'
    res = requests.get(quote_page)
    soup = BeautifulSoup(res.text, 'html.parser')
    print(">>>>soup.get_text()="+soup.get_text())

    match = []
    for drink in soup.select('{}'.format(tag)):
        print(">>>>>>drink.get_text()="+drink.get_text())        
        title = drink.get_text()
        print(">>>>>>title="+title)
       
        link = 'https://www.cwb.gov.tw' + title
        match.append({'title':title, 'link':link })

    print(">>>>match="+match)
    if len(match) > 0:            
        for article in match:
            print(">>>>>>New Article: {} {}".format(article['title'], article['link']))
            url ="{}".format(article['link'])


    print("Action finRadarUrl_END:"+url)

    return url

def over18(sboard):
    print(">>>>>>>>>board="+sboard)
    rs = requests.session()
    res = rs.get('https://www.ptt.cc/bbs/{}/index.html'.format(sboard), verify=False)
    # 先檢查網址是否包含'over18'字串 ,如有則為18禁網站
    if 'over18' in res.url:
        print("18禁網頁")
        load = {
            'from': '/bbs/{}/index.html'.format(sboard),
            'yes': 'yes'
        }
        res = rs.post('https://www.ptt.cc/ask/over18', verify=False, data=load)
    return BeautifulSoup(res.text, 'html.parser')

def ptt_beauty():
    rs = requests.session()
    res = rs.get('https://www.ptt.cc/bbs/Beauty/index.html', verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    all_page_url = soup.select('.btn.wide')[1]['href']
    start_page = get_page_number(all_page_url)
    page_term = 2  # crawler count
    push_rate = 10  # 推文
    index_list = []
    article_list = []
    for page in range(start_page, start_page - page_term, -1):
        page_url = 'https://www.ptt.cc/bbs/Beauty/index{}.html'.format(page)
        index_list.append(page_url)

    # 抓取 文章標題 網址 推文數
    while index_list:
        index = index_list.pop(0)
        res = rs.get(index, verify=False)
        # 如網頁忙線中,則先將網頁加入 index_list 並休息1秒後再連接
        if res.status_code != 200:
            index_list.append(index)
            # print u'error_URL:',index
            # time.sleep(1)
        else:
            article_list = craw_page(res, push_rate)
            # print u'OK_URL:', index
            # time.sleep(0.05)
    content = ''
    for article in article_list:
        data = '[{} push] {}\n{}\n'.format(article.get('rate', None), article.get('title', None),
                                             article.get('url', None))
        content += data
    return content

def craw_page(res, push_rate):
    soup_ = BeautifulSoup(res.text, 'html.parser')
    article_seq = []
    for r_ent in soup_.find_all(class_="r-ent"):
        try:
            # 先得到每篇文章的篇url
            link = r_ent.find('a')['href']
            if link:
                # 確定得到url再去抓 標題 以及 推文數
                title = r_ent.find(class_="title").text.strip()
                rate = r_ent.find(class_="nrec").text
                url = 'https://www.ptt.cc' + link
                if rate:
                    rate = 100 if rate.startswith('爆') else rate
                    rate = -1 * int(rate[1]) if rate.startswith('X') else rate
                else:
                    rate = 0
                # 比對推文數
                if int(rate) >= push_rate:
                    article_seq.append({
                        'title': title,
                        'url': url,
                        'rate': rate,
                    })
        except Exception as e:
            # print('crawPage function error:',r_ent.find(class_="title").text.strip())
            print('本文已被刪除', e)
    return article_seq

def ptt_gossiping():
    rs = requests.session()
    load = {
        'from': '/bbs/Gossiping/index.html',
        'yes': 'yes'
    }
    res = rs.post('https://www.ptt.cc/ask/over18', verify=False, data=load)
    soup = BeautifulSoup(res.text, 'html.parser')
    all_page_url = soup.select('.btn.wide')[1]['href']
    start_page = get_page_number(all_page_url)
    index_list = []
    article_gossiping = []
    for page in range(start_page, start_page - 2, -1):
        page_url = 'https://www.ptt.cc/bbs/Gossiping/index{}.html'.format(page)
        index_list.append(page_url)

    # 抓取 文章標題 網址 推文數
    while index_list:
        index = index_list.pop(0)
        res = rs.get(index, verify=False)
        # 如網頁忙線中,則先將網頁加入 index_list 並休息1秒後再連接
        if res.status_code != 200:
            index_list.append(index)
            # print u'error_URL:',index
            # time.sleep(1)
        else:
            article_gossiping = crawl_page_gossiping(res)
            # print u'OK_URL:', index
            # time.sleep(0.05)
    content = ''
    for index, article in enumerate(article_gossiping, 0):
        if index == 15:
            return content
        data = '{}\n{}\n'.format(article.get('title', None), article.get('url_link', None))
        content += data
    return content

def ptt_AC_In():
    rs = requests.session()
    load = {
        'from': '/bbs/AC_In/index.html',
        'yes': 'yes'
    }
    res = rs.post('https://www.ptt.cc/ask/over18', verify=False, data=load)
    soup = BeautifulSoup(res.text, 'html.parser')
    all_page_url = soup.select('.btn.wide')[1]['href']
    start_page = get_page_number(all_page_url)
    index_list = []
    article_gossiping = []
    for page in range(start_page, start_page - 2, -1):
        page_url = 'https://www.ptt.cc/bbs/AC_In/index{}.html'.format(page)
        index_list.append(page_url)

    # 抓取 文章標題 網址 推文數
    while index_list:
        index = index_list.pop(0)
        res = rs.get(index, verify=False)
        # 如網頁忙線中,則先將網頁加入 index_list 並休息1秒後再連接
        if res.status_code != 200:
            index_list.append(index)
            # print u'error_URL:',index
            # time.sleep(1)
        else:
            article_gossiping = crawl_page_gossiping(res)
            # print u'OK_URL:', index
            # time.sleep(0.05)
    content = ''
    for index, article in enumerate(article_gossiping, 0):
        if index == 15:
            return content
        data = '{}\n{}\n'.format(article.get('title', None), article.get('url_link', None))
        content += data
    return content

def crawl_page_gossiping(res):
    soup = BeautifulSoup(res.text, 'html.parser')
    article_gossiping_seq = []
    for r_ent in soup.find_all(class_="r-ent"):
        try:
            # 先得到每篇文章的篇url
            link = r_ent.find('a')['href']

            if link:
                # 確定得到url再去抓 標題 以及 推文數
                title = r_ent.find(class_="title").text.strip()
                url_link = 'https://www.ptt.cc' + link
                article_gossiping_seq.append({
                    'url_link': url_link,
                    'title': title
                })

        except Exception as e:
            # print u'crawPage function error:',r_ent.find(class_="title").text.strip()
            # print('本文已被刪除')
            print('delete', e)
    return article_gossiping_seq