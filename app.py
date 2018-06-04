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

app = Flask(__name__)

# 填入你的 message api 資訊
# Channel access token
line_bot_api = LineBotApi('mTwL/HAGwWalJsXrpKZpbCFNWJBDOm6pt1ib7v/rXqdT/8dfw3J9fgqOffmVax7QAxHfOlpdEIRAj2ePUtD9X4S2FG0bapg1jWvFRQ9GzFzFkrs0sU3yhX/+rhTgnAypsze6TKJgumTLM25AHRByjAdB04t89/1O/w1cDnyilFU=')
# Channel secret
handler = WebhookHandler('393db2f764c38a5f9d4634af4f671c48')

#User ID
to_myuserid='b4c358d6453b4d7c9131b9486a9da70b'

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
        print("123")
        handler.handle(body, signature)
        print("END")
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("handle_message11")
    print("Handle: reply_token: " + event.reply_token + ", message: " + event.message.text)
    content = "你肚子的回聲蟲: {}".format(event.message.text)

    print("testConfirm11")
    # contentrd = "ID:{}傳給LINE Bot:{}".format(event.reply_token,event.message.text)

    #push message to one user
    line_bot_api.reply_message(
        to_myuserid,
        TextSendMessage(text=content))

    print("testConfirm22")

  
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=content))

    print("handle_message22")



import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
