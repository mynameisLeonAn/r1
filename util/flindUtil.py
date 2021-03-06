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
from util.stringUtil import formatNum

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
        # try:
        driver.get('https://www.ptt.cc/bbs/{}/index.html'.format(slfindList[0]))
        soup = BeautifulSoup(driver.page_source, "html.parser")
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
            driver.get(index)
            soup2 = BeautifulSoup(driver.page_source, "html.parser")

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
        # except :
        #     sMessgge = "{},查無結果:{}".format(sfind,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    print("Action findPTT_END")

    return sMessgge

def findPTT2Page(driver,slfindList,sfind):
    print("Action findPTT2Page")
    print("slfindList[0]="+slfindList[0])
    sNotificationMulticast = ""
    match = []

    # try:
    # re_gs_title = re.compile(r'\['+slfindList[1]+'\s*\]\s*', re.I)
    re_gs_id = re.compile(r'.*\/'+slfindList[0]+'\/M\.(\S+)\.html')
    driver.get('https://www.ptt.cc/bbs/{}/index.html'.format(slfindList[0]))
    soup = BeautifulSoup(driver.page_source, "html.parser")

    all_page_url = soup.select('.btn.wide')[1]['href']
    start_page = get_page_number(all_page_url)
    page_term = 2  # crawler count
    
    index_list = []
    for page in range(start_page, start_page - page_term, -1):
        page_url = 'https://www.ptt.cc/bbs/{}/index{}.html'.format(slfindList[0], page)
        index_list.append(page_url)

    while index_list:
        index = index_list.pop(0)
        driver.get(index)
        soup2 = BeautifulSoup(driver.page_source, "html.parser")

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
    # except :
    #     sMessgge = "{},查無結果:{}".format(sfind,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

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

    quote_page = 'https://www.cwb.gov.tw/V7/js/HDRadar_TW_3600_n_val.js'
    res = requests.get(quote_page)
    soup = BeautifulSoup(res.text, 'html.parser')

    slfindList = soup.get_text().replace(";","").replace(":","").replace("\"","").replace("(","").replace(")","").split(",")

    # for i in range(1,len(slfindList),2): 第2筆為最新 
    # for i in range(0,len(slfindList),1):
    #     print(i)
    #     print("slfindList="+slfindList[i])

    url = 'https://www.cwb.gov.tw' +slfindList[1]

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

def ptt_find(sfind):
    rs = requests.session()
    load = {
        'from': '/bbs/{}/index.html'.format(sfind),
        'yes': 'yes'
    }
    res = rs.post('https://www.ptt.cc/ask/over18', verify=False, data=load)
    soup = BeautifulSoup(res.text, 'html.parser')
    all_page_url = soup.select('.btn.wide')[1]['href']
    start_page = get_page_number(all_page_url)
    index_list = []
    article_gossiping = []
    for page in range(start_page, start_page - 2, -1):
        page_url = 'https://www.ptt.cc/bbs/{}/index{}.html'.format(sfind,page)
        index_list.append(page_url)

    # 抓取 文章標題 網址 推文數
    while index_list:
        index = index_list.pop(0)
        res = rs.get(index, verify=False)
        # 如網頁忙線中,則先將網頁加入 index_list 並休息1秒後再連接
        if res.status_code != 200:
            index_list.append(index)

        else:
            article_gossiping = crawl_page_gossiping(res)

    content = ''

    if len(article_gossiping) > 0:
        with open('data/history/jobUniqueHistory.json', 'r+') as file:
            history = json.load(file)

            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')       
            new_flag = False
            for index, article in enumerate(article_gossiping, 0):
                key = "{}".format(article['url_link'])
                if key in history:
                    continue

                if index == 15:
                    return content

                new_flag = True
                history.append(key)

                data = '{}\n{}\n'.format(article.get('title', None), article.get('url_link', None))
                content += data
                print("{}: New Article: {} {}".format(now, article['title'], article['url_link']))

                print("{}: New_flag:{} ".format(now,new_flag))
                if new_flag == True:
                    file.seek(0)
                    file.truncate()
                    file.write(json.dumps(history))
                    
                else:
                    print("{}: Nothing".format(now))


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


def getGoldCorridor():
    # 盤後交易限於網路銀行買賣黃金存摺。
    # 本表資料僅供參考，網路銀行實際交易價格以交易確認時顯示之價格為準。
    # 盤後交易時間為營業日(不含週六補上班日)下午4時至夜間8時。
    # 當國際黃金價格、外匯走勢或全球金融市場劇烈波動時，本行將隨之機動調整黃金牌價買賣價差。
    # 坊間以本行名義流傳招攬之黃金買賣交易，均與本行無涉，敬請民眾注意，切勿受騙。
    content = ""

    # 以 BeautifulSoup 解析 HTML 程式碼
    rs = requests.session()
    res = rs.get('https://rate.bot.com.tw/gold?Lang=zh-TW', verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')

    # 以 CSS 的 class 抓出掛牌時間
    stories = soup.find_all('div', class_='pull-left trailer text-info')
    for s in stories:
        # 掛牌時間
        print(s.text)
        content='臺灣銀行Gold{}\n'.format(s.text.lstrip().rstrip())

    stories = soup.find_all('td', class_='text-right')
    i=0
    for s in stories:
        # 本行賣出1克/本行賣進1克
        # print('({}) :{}'.format(i,s.text))

        if(i==0):
            content += '{}\n'.format('黃金存摺:賣出1克:'+formatNum(s.text))
        elif(i==1):
            content += '{}\n'.format('黃金存摺:賣進1克:'+formatNum(s.text))
        else:
            pass

        i=i+1

    return content


def getRateSwitch(sRateList,bChange):

    if bChange :
        sRateList=sRateList.replace('USD','美金')
        sRateList=sRateList.replace('HKD','港幣')
        sRateList=sRateList.replace('GBP','英鎊')
        sRateList=sRateList.replace('AUD','澳幣')
        sRateList=sRateList.replace('CAD','加拿大幣')
        sRateList=sRateList.replace('SGD','新加坡幣')
        sRateList=sRateList.replace('CHF','瑞士法郎')
        sRateList=sRateList.replace('JPY','日圓')
        sRateList=sRateList.replace('ZAR','南非幣')
        sRateList=sRateList.replace('SEK','瑞典幣')
        sRateList=sRateList.replace('NZD','紐元')
        sRateList=sRateList.replace('THB','泰幣')
        sRateList=sRateList.replace('PHP','菲國比索')
        sRateList=sRateList.replace('IDR','印尼幣')
        sRateList=sRateList.replace('EUR','歐元')
        sRateList=sRateList.replace('KRW','韓元')
        sRateList=sRateList.replace('VND','越南盾')
        sRateList=sRateList.replace('MYR','馬來幣')
        sRateList=sRateList.replace('CNY','人民幣')
    else :
        sRateList=sRateList.replace('美金','USD')
        sRateList=sRateList.replace('港幣','HKD')
        sRateList=sRateList.replace('英鎊','GBP')
        sRateList=sRateList.replace('澳幣','AUD')
        sRateList=sRateList.replace('加拿大幣','CAD')
        sRateList=sRateList.replace('新加坡幣','SGD')
        sRateList=sRateList.replace('瑞士法郎','CHF')
        sRateList=sRateList.replace('日圓','JPY')
        sRateList=sRateList.replace('南非幣','ZAR')
        sRateList=sRateList.replace('瑞典幣','SEK')
        sRateList=sRateList.replace('紐元','NZD')
        sRateList=sRateList.replace('泰幣','THB')
        sRateList=sRateList.replace('菲國比索','PHP')
        sRateList=sRateList.replace('印尼幣','IDR')
        sRateList=sRateList.replace('歐元','EUR')
        sRateList=sRateList.replace('韓元','KRW')
        sRateList=sRateList.replace('越南盾','VND')
        sRateList=sRateList.replace('馬來幣','MYR')
        sRateList=sRateList.replace('人民幣','CNY')

    return sRateList

def getRateCorridor(sfind):
    content = ""
    sfind = getRateSwitch(sfind.lstrip().rstrip().replace(' ','').replace('getRateCorridor:',''),False)
    slfindList = sfind.split("#@#")

    if len(slfindList) < 1 :
        content = "{},查詢格式有誤，請參閱Rich_help:{}".format(sfind,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    else:
        # 以 BeautifulSoup 解析 HTML 程式碼
        rs = requests.session()
        res = rs.get('https://rate.bot.com.tw/xrt?Lang=zh-TW', verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')

        # 以 CSS 的 class 抓出掛牌時間
        stories = soup.find_all('span', class_='time')
        for s in stories:
            # 掛牌時間
            print(s.text)
            content = '匯率最新掛牌時間:{}\n'.format(s.text.lstrip().rstrip())
            content += '============\n'

        stories = soup.findChildren('tr')
        i=0
        for s in stories:
            # 即期匯率 elif  sConfirmText.find("找推圖") >= 0
            sRateText = s.text.lstrip().rstrip().replace(" ","")

            for sRateFind in slfindList:
                if sRateText.find(sRateFind) >= 0 :
                    inum=0
                    for slist in s.findChildren('td'):
                        if(inum==1):
                            content += '{}{}'.format(sRateFind,'-現金匯率\n  買入/賣出:'+formatNum(slist.text))
                        elif(inum==2):
                            content += '{}\n'.format('/'+formatNum(slist.text))
                        elif(inum==3):
                            content += '{}{}'.format(sRateFind,'-即期匯率\n  買入/賣出:'+formatNum(slist.text))
                        elif(inum==4):
                            content += '{}\n'.format('/'+formatNum(slist.text))
                        
                        inum=inum+1

                    content += '============\n'

                else:
                    pass

                
                i=i+1

    return getRateSwitch(content,True)


def getRateArrivalNotice(sfind,sfindRate,sSwitch):
    content = ""
    sfind = getRateSwitch(sfind.lstrip().rstrip().replace(' ','').replace('getRateCorridor:',''),False)
    slfindList = sfind.split("#@#")
    slfindRate = sfindRate.split("#@#")
    slSwitch = sSwitch.split("#@#")

    if len(slfindList) < 1 or len(slfindRate) < 1 or len(slSwitch)< 1:
        content = "{},查詢格式有誤，請參閱Rich_help:{}".format(sfind,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    else:
        # 以 BeautifulSoup 解析 HTML 程式碼
        rs = requests.session()
        res = rs.get('https://rate.bot.com.tw/xrt?Lang=zh-TW', verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')

        # 以 CSS 的 class 抓出掛牌時間
        stories = soup.find_all('span', class_='time')
        for s in stories:
            # 掛牌時間
            print(s.text)
            content='匯率最新掛牌時間:{}\n'.format(s.text.lstrip().rstrip())
            content += '============\n'

        ifindRate=0
        stories = soup.findChildren('tr')
        for sRateFind in slfindList:
            for s in stories:
                # 即期匯率 elif  sConfirmText.find("XX") >= 0
                sRateText = s.text.lstrip().rstrip().replace(" ","")
                #暫存買入iBuy 賣出iSend
                iBuy=0
                iSend=0
                if sRateText.find(sRateFind) >= 0 :
                    inum=0
                    print(str(ifindRate))
                    for slist in s.findChildren('td'):
                        #紀錄 比較價格
                        iRate=float(slfindRate[ifindRate])
                        if slSwitch[ifindRate] == '現金':
                            if(inum==1):
                                content += '{}{}'.format(sRateFind,'-現金匯率\n  買入/賣出:'+formatNum(slist.text))
                                #紀錄 比較價格-現在價格
                                iBuy = float(slist.text)-float(slfindRate[ifindRate])
                            elif(inum==2):
                                content += '{}\n'.format('/'+formatNum(slist.text))
                                iSend = float(slist.text)-float(slfindRate[ifindRate]) 
                                ifindRate +=1    
                                break
                                                      
                        
                        elif slSwitch[ifindRate] == '即期':
                            if(inum==3):
                                content += '{}{}'.format(sRateFind,'-即期匯率\n  買入/賣出:'+formatNum(slist.text))
                                iBuy = float(slist.text)-float(slfindRate[ifindRate])
                            elif(inum==4):
                                content += '{}\n'.format('/'+formatNum(slist.text))
                                iSend = float(slist.text)-float(slfindRate[ifindRate])
                                ifindRate +=1  
                                break
                                
                        
                        inum=inum+1
                    content += '{}，價差買入:{} /賣出:{}\n'.format(str(iRate),formatNum(str(iBuy)[:6]),formatNum(str(iSend))[:6] )
                    content += '============\n'
                    
                else:
                    pass

                

    return getRateSwitch(content,True)
       
