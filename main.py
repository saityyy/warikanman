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


def get_send_datetime(event: MessageEvent) -> datetime.datetime:
    if event.timestamp is None:
        # 現在の時刻を返す
        return datetime.datetime.now(tz=ZoneInfo("Asia/Tokyo"))
    return datetime.datetime.fromtimestamp(int(event.timestamp/1000),
                                           tz=ZoneInfo("Asia/Tokyo"))


def get_project_id(event: MessageEvent) -> str:
    if event.source.type == "group":
        return str(event.source.group_id)
    else:
        return str(event.source.user_id)


def get_user_name(user_id: str) -> str:
    user_name = line_bot_api.get_profile(user_id).display_name
    if user_name is None:
        return "名無しさん_"+str(user_id)
    else:
        return user_name


def print_log(time: datetime.datetime, project_id: str, command: str) -> None:
    print("[{} , {} , {}]".format(time, project_id, command))


def send_reply(_token, _textmessage):
    line_bot_api.reply_message(
        _token,
        TextSendMessage(text=_textmessage)
    )


@ handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    if not conn.is_connected():
        conn.ping(reconnect=True, attempts=3, delay=3)
    date_time = get_send_datetime(event)
    project_id = get_project_id(event)
    user_id: str = event.source.user_id
    user_name = get_user_name(user_id)
    message_result = functions.extract_message(str(event.message.text))
    print_log(date_time, project_id, message_result["type"])
    if message_result["type"] == "pass":
        pass
    elif not message_result["isValid"]:
        send_reply(event.reply_token, message_result["error_message"])
    # !project <参加人数>
    elif message_result["type"] == "project":
        participant_number, = message_result["args"]
        res = functions.create_projects(
            conn, date_time, project_id, participant_number)
        send_reply(event.reply_token, res)
    # !log
    elif message_result["type"] == "log":
        res = functions.check_payments_log(conn, project_id)
        send_reply(event.reply_token, res)
    # !pay <金額> <メッセージ>
    elif message_result["type"] == "pay":
        amount, message = message_result["args"]
        res = functions.add_payment(
            conn, project_id, user_id, user_name, date_time, amount, message)
        send_reply(event.reply_token, res)
    # !check
    elif message_result["type"] == "check":
        res = functions.warikan(conn, project_id)
        send_reply(event.reply_token, res)
    # !delete <削除したい記録の通し番号>
    elif message_result["type"] == "delete":
        del_index, = message_result["args"]
        res = functions.delete_payment(conn, project_id, int(del_index))
        send_reply(event.reply_token, res)
    # !help
    elif message_result["type"] == "help":
        f = open("./help.txt")
        send_reply(event.reply_token, f.read())
        f.close()


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
