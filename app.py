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

def index():
    return "<p>Wenli_tset:</p>"+datetime.datetime.now().time()

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
    msg = event.message.text
    msg = msg.encode('utf-8')

    content = "你肚子有回聲蟲: {}".format(event.message.text)
  
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=content))
   
    print("testConfirm11")
    userId = event.source.user_id
    print("userId="+userId)
    contentrd = "ID: {}傳給LINE Bot: {}".format(userId, event.message.text)

    print("push_message="+contentrd)
    #push message to one user
    line_bot_api.push_message(
        userId,
        TextSendMessage(text=contentrd))

    print("push_message_END")



import os
if __name__ == "__main__":
    app.run(debug=True)
    app.run(host='0.0.0.0',port=os.environ['PORT'])
