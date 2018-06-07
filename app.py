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
from datetime import datetime

app = Flask(__name__)

# 填入你的 message api 資訊
# Channel access token
line_bot_api = LineBotApi('kKnqWh2H18SIBXfwovAY5ScSfsH9fOOTxVAHkV/IRBkHi+kg+j5lJUKmnbMrcHQKdqnESugkPYahGCUXFOOC9cUWW0uUZgGSifYDeygynCdaZE7ABXgLfJ2kRKLyJeGujLVag6Df61W5pHQsPLYKxwdB04t89/1O/w1cDnyilFU=')
# Channel secret
handler = WebhookHandler('fedfc3d7af2d1fd102ddf854fefd7141')

#User ID
to_myuserid='Ud0d8235b4696d1cab3da6b1e46f39598'

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
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=content))
   
    userId = event.source.user_id
    contentrd = "ID: {}傳給LINE Bot: {} ，系統回傳:{}".format(userId, event.message.text,content)

    print("push_message="+contentrd)
    #push message to one user
    line_bot_api.push_message(
        userId,
        TextSendMessage(text=contentrd))

def confirmMessage(event):
    sReturn = ""
    sConfirmText = event.message.text
    import random
    iRandom = random.sample(range(5), 1)[0]
    
    print("iRandom={}".format(iRandom))

    if sConfirmText.find("想吃"):
        sReturn = switch(iRandom)
    elif  sConfirmText.find("要吃"):
        sReturn = switch(iRandom)
    else:
        sReturn = "你肚子有回聲蟲: {}".format(event.message.text)

    return sReturn

def switch(x):
    print("x={}".format(x))
    return {
        0 :">>>>今天吃麥當當",
        1 :">>>>今天吃KFC"     ,
        2 :">>>>今天吃頂呱呱"  ,
        3 :">>>>今天吃拿坡里"  ,
        4 :">>>>今天吃八方"    ,
    }.get(x,">>>>今天吃XXX")

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
