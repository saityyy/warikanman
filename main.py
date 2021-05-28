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

from Project import Project
 
app = Flask(__name__)
 
#環境変数取得
# LINE Developersで設定されているアクセストークンとChannel Secretをを取得し、設定します。
YOUR_CHANNEL_ACCESS_TOKEN =("XLE95iVshxjGrMfiOHZqscHfN+ArdNOZV5ZkJSsxMewKlurJ2cORgcBqpeK9nnmNjT748hYdxbDrOHVRDyvWtsexhy3vTC+QLBPM5VcQSxikq7wkhAPlYNqCqGZZq+vKvB5IFvSoD8D2AKG0Fb2C0wdB04t89/1O/w1cDnyilFU=")
YOUR_CHANNEL_SECRET = ("29c927a9604c6430ae09d4e2d7d256a1")
 
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)
 
 
## 1 ##
#Webhookからのリクエストをチェックします。
@app.route("/callback", methods=['POST'])
def callback():
    # リクエストヘッダーから署名検証のための値を取得します。
    signature = request.headers['X-Line-Signature']
 
    # リクエストボディを取得します。
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
 
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
 
#LINEでMessageEvent（普通のメッセージを送信された場合）が起こった場合に、
#def以下の関数を実行します。
#reply_messageの第一引数のevent.reply_tokenは、イベントの応答に用いるトークンです。 
#第二引数には、linebot.modelsに定義されている返信用のTextSendMessageオブジェクトを渡しています。

project={}
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mes=str(event.message.text)
    if not mes[:3] in ["pro","add","log","acc"]:
        return 
    source_type=event.source.type
    if source_type=="group":
        project_id=event.source.groupId
    elif source_type=="room":
        project_id=event.source.roomId
    user_id=event.source.user_id
    user=line_bot_api.get_profile(user_id).display_name
    # 本番ではelseの中に入れる
    project_id=user_id
    if mes=="project":
        print(mes)
        project[project_id]=Project("test",user)
        res="{}がプロジェクトを作成しました".format(user)
        send(event.reply_token,res)
    elif "log" in mes:
        log_data=project[project_id].log_data()
        send(event.reply_token,log_data)
    elif "add" in mes:
        project[project_id].pay_money(user,mes)
    elif "accounting" in mes:
        pass

def send(_token,_textmessage):
    line_bot_api.reply_message(
        _token,
        TextSendMessage(text=_textmessage)
    ) 
# ポート番号の設定
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
