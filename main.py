from flask import Flask, request, abort
import mysql.connector
import datetime

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from zoneinfo import ZoneInfo
import os

from functions import functions

app = Flask(__name__)
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

conn = mysql.connector.connect(
    user="warikanman",
    password="warikanman",
    host="127.0.0.1",
    database="warikanman"
)


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


TEMP_TIMESTAMP = "2020-01-01 00:00:00"
project = {}


@ handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    if not conn.is_connected():
        conn.ping(reconnect=True, attempts=3, delay=3)
    mes = str(event.message.text)
    date_time = datetime.datetime.fromtimestamp(int(event.timestamp/1000),
                                                tz=ZoneInfo("Asia/Tokyo"))
    print("送信メッセージ : {}".format(mes))
    source_type = event.source.type
    user_id = event.source.user_id
    if source_type == "group":
        project_id = str(event.source.group_id)
    elif source_type == "room":
        project_id = str(event.source.room_id)
    else:
        project_id = str(user_id)
    user = line_bot_api.get_profile(user_id).display_name
    message_result = functions.extract_message(mes)
    print(message_result)
    if message_result["type"] == "pass":
        pass
    elif not message_result["isValid"]:
        send(event.reply_token, message_result["error_message"])
    elif message_result["type"] == "project":
        participant_number = int(message_result["args"])
        res = functions.create_projects(
            conn, date_time, project_id, participant_number)
        send(event.reply_token, res)
    elif message_result["type"] == "log":
        res = functions.check_payments_log(conn, project_id)
        send(event.reply_token, res)
    elif message_result["type"] == "pay":
        amount, message = message_result["args"]
        res = functions.add_payment(
            conn, project_id, user_id, user, date_time, amount, message)
        send(event.reply_token, res)
    elif message_result["type"] == "check":
        res = functions.warikan(conn, project_id)
        send(event.reply_token, res)
    elif message_result["type"] == "delete":
        del_index = message_result["args"]
        res = functions.delete_payment(conn, project_id, int(del_index))
        send(event.reply_token, res)
    elif message_result["type"] == "help":
        f = open("./help.txt")
        send(event.reply_token, f.read())
        f.close()


def send(_token, _textmessage):
    line_bot_api.reply_message(
        _token,
        TextSendMessage(text=_textmessage)
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
