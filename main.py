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

from Project import Project

app = Flask(__name__)
# jsonで読み込むようにする.
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@ app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


project = {}


@ handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mes = str(event.message.text)
    if not mes[:3] in ["pro", "pay", "log", "che"]:
        return
    source_type = event.source.type
    user_id = event.source.user_id
    if source_type == "group":
        project_id = str(event.source.group_id)
    elif source_type == "room":
        project_id = str(event.source.room_id)
    else:
        project_id = str(user_id)
    user = line_bot_api.get_profile(user_id).display_name
    if "project" in mes:
        participants = re.sub(r"\D", "", mes)
        if len(participants) == 0:
            send(event.reply_token, "参加人数を入力してください")
        else:
            project[project_id] = Project(user_id, user, int(participants))
            res = "{}が参加人数{}人の割り勘プロジェクトを作成しました".format(user, int(participants))
            send(event.reply_token, res)
    elif "log" in mes:
        log_data = project[project_id].log_data()
        send(event.reply_token, log_data)
    elif "pay" in mes:
        result = project[project_id].pay_money(user_id, user, mes)
        send(event.reply_token, result)
    elif "check" in mes:
        result = project[project_id].check_payment()
        send(event.reply_token, result)
    elif "delete" in mes:
        del_index = re.sub(r"\D", "", mes)
        result = project[project_id].delete_record(del_index)
        send(event.reply_token, result)


def send(_token, _textmessage):
    line_bot_api.reply_message(
        _token,
        TextSendMessage(text=_textmessage)
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
