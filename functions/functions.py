import datetime
from typing import Any, TypedDict, Literal

# alias typing


class MessageResult(TypedDict):
    type: Literal["help",
                  "project",
                  "log",
                  "check",
                  "delete",
                  "pay",
                  "pass"]
    args: tuple
    isValid: bool
    error_message: str


def create_projects(conn,
                    date_time: datetime.datetime,
                    project_id: str,
                    participant_number: int
                    ) -> str:
    cur = conn.cursor(dictionary=True)
    # すでにプロジェクトが存在する場合は削除
    cur.execute("SELECT * FROM projects WHERE project_id=%s;", (project_id,))
    if len(cur.fetchall()) > 0:
        cur.execute("DELETE FROM projects WHERE project_id=%s;", (project_id,))
    cur.execute("INSERT INTO projects (project_id,datetime,participant_number) VALUES(%s,%s,%s);",
                (project_id, date_time, participant_number))
    conn.commit()
    reply_message = "参加人数{}人の割り勘プロジェクトを作成しました".format(participant_number)
    return reply_message


def add_payment(conn,
                project_id: str,
                user_id: str,
                name: str,
                date_time: datetime.datetime,
                amount: int,
                message: str
                ) -> str:
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM projects WHERE project_id=%s;", (project_id,))
    project = cur.fetchall()
    if len(project) == 0:
        return "プロジェクトが存在しません"
    participant_number: int = project[0]["participant_number"]
    cur.execute(
        "SELECT DISTINCT user_id FROM payments WHERE project_id=%s;", (project_id,))
    # すでに支払い記録があるユーザーのuser_idを取得
    pay_user_ids = [row["user_id"] for row in cur.fetchall()]
    if len(pay_user_ids) == participant_number and (user_id not in pay_user_ids):
        return "設定した参加人数を超えています"
    cur.execute("SELECT name FROM users WHERE user_id=%s;", (user_id,))
    user = cur.fetchall()
    # ユーザーが存在しない場合は追加
    if len(user) == 0:
        cur.execute(
            "INSERT INTO users (user_id,name) VALUES(%s,%s);", (user_id, name))
    # ユーザー名が変更されている場合は更新
    elif user[0]["name"] != name:
        cur.execute("UPDATE users SET name=%s WHERE user_id=%s;",
                    (name, user_id))
    cur.execute("INSERT INTO payments (project_id,user_id,datetime,amount,message) VALUES(%s,%s,%s,%s,%s);",
                (project_id, user_id, date_time, amount, message))
    conn.commit()
    reply_message = "記録しました\n"
    reply_message += "{} : {}円\n".format(name, amount)
    if message != "":
        reply_message += "メッセージ : {}".format(message)
    return reply_message


def check_payments_log(conn, project_id: str) -> str:
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT participant_number FROM projects WHERE project_id=%s;", (project_id,))
    project = cur.fetchall()
    if len(project) == 0:
        return "プロジェクトが存在しません"
    participant_number: int = project[0]["participant_number"]
    # あるプロジェクトでの支払い記録をdatetimeでソートして取得
    query = """
        SELECT id,datetime,(SELECT name from users WHERE user_id=p.user_id)
        user_name,amount,message FROM payments p
        WHERE project_id=(SELECT project_id FROM projects WHERE project_id=%s)
        ORDER BY datetime ASC;
    """
    cur.execute(query, (project_id,))
    reply_message = "割り勘参加人数 : {}人\n\n".format(participant_number)
    result = cur.fetchall()
    for idx, row in enumerate(result, start=1):
        datetime_str = row["datetime"].strftime("%-m/%-d %-H:%M")
        reply_message += "{}) {}\n".format(idx, datetime_str)
        reply_message += "{} : {}円\n".format(row["user_name"], row["amount"])
        if row["message"] != "":
            reply_message += "メッセージ : {}\n".format(row["message"])
        reply_message += "\n"
    reply_message += "合計 : {}円".format(sum([row["amount"] for row in result]))
    conn.commit()
    return reply_message


def warikan(conn, project_id: str) -> str:
    cur = conn.cursor(dictionary=True)
    # paymentsテーブルからプロジェクトIDが一致するものを取得
    query = """
        SELECT (SELECT name from users WHERE user_id=p.user_id) user_name,
        amount,message FROM payments p WHERE project_id=%s;
    """
    cur.execute(query, (project_id,))
    result = cur.fetchall()
    # project's participants number
    cur.execute(
        "SELECT participant_number FROM projects WHERE project_id=%s;", (project_id,))
    project: list[dict[str, Any]] = cur.fetchall()
    if len(project) == 0:
        return "プロジェクトが存在しません"
    participant_number: int = project[0]["participant_number"]
    username2amount: dict[str, int] = {}
    # 合計金額を計算
    total_amount: int = 0
    for row in result:
        total_amount += row["amount"]
        if row["user_name"] not in username2amount.keys():
            username2amount[row["user_name"]] = 0
        username2amount[row["user_name"]] += row["amount"]
    fraction = total_amount % participant_number
    amount_per_user = int(total_amount/participant_number)
    if total_amount == 0:
        return "支払い記録がまだひとつもありません"
    reply_message = "合計金額 : {}円\n".format(total_amount)
    reply_message += "参加人数 : {}人\n".format(participant_number)
    reply_message += "一人あたりの金額 : {}円\n\n".format(amount_per_user)
    reply_message += "端数 : {}円\n\n".format(fraction)
    for name, amount in username2amount.items():
        reply_message += "{} : {}円".format(name, amount)
        if amount > amount_per_user:
            reply_message += "（{}円もらう）\n".format(amount-amount_per_user)
        else:
            reply_message += "（{}円はらう）\n".format(amount_per_user-amount)
    other_num = participant_number-len(username2amount)
    if other_num > 0:
        reply_message += "その他の参加者：0円（{}円はらう）\n".format(amount_per_user)
    reply_message = reply_message[:-1]
    return reply_message


# あるプロジェクトでの支払い記録をdatetimeでソートして、古い方からindex番目のものを削除
def delete_payment(conn, project_id: str, delete_number: int) -> str:
    query = """
        SELECT id FROM payments WHERE project_id=
        (SELECT project_id FROM projects WHERE project_id=%s)
        ORDER BY datetime ASC;
    """
    cur = conn.cursor(dictionary=True)
    cur.execute(query, (project_id,))
    result = cur.fetchall()
    if len(result) == 0:
        return "プロジェクトが存在しません"
    if not (0 <= delete_number-1 < len(result)):
        return "その番号の記録は存在しません"
    cur.execute("DELETE FROM payments WHERE id=%s;",
                (result[delete_number-1]["id"],))
    conn.commit()
    return "{}番の記録を削除しました".format(delete_number)


def extract_message(message: str) -> MessageResult:
    messages = message.split()
    message_result: MessageResult = {
        "type": "pass",
        "args": (),
        "isValid": True,
        "error_message": ""
    }
    if messages[0] == "!help":
        message_result["type"] = "help"
        return message_result
    if messages[0] == "!check":
        message_result["type"] = "check"
        return message_result
    if messages[0] == "!log":
        message_result["type"] = "log"
        return message_result
    if messages[0] == "!project":
        message_result["type"] = "project"
        if len(message.split()) == 1:
            message_result["isValid"] = False
            message_result["error_message"] = "プロジェクトの参加人数を半角数字で入力してください"
            return message_result
        participant_number = message.split()[1]
        if not (participant_number.isdigit() and int(participant_number) >= 2):
            message_result["isValid"] = False
            message_result["error_message"] = "参加人数は2以上の半角数字で入力してください"
            return message_result
        message_result["args"] = (int(participant_number),)
        return message_result
    if messages[0] == "!delete":
        message_result["type"] = "delete"
        if len(message.split()) == 1:
            message_result["isValid"] = False
            message_result["error_message"] = "削除する記録の通し番号を半角数字で入力してください"
            return message_result
        index = message.split()[1]
        if not (index.isdigit() and int(index) >= 1):
            message_result["isValid"] = False
            message_result["error_message"] = "通し番号の指定は1以上の半角数字で入力してください"
            return message_result
        message_result["args"] = (int(index),)
        return message_result
    elif messages[0] == "!pay":
        message_result["type"] = "pay"
        if len(message.split()) == 1:
            message_result["isValid"] = False
            message_result["error_message"] = "はらった金額を半角数字で入力してください"
            return message_result
        amount = messages[1]
        pay_message = " ".join(messages[2:])
        if not (amount.isdigit() and int(amount) > 0):
            message_result["isValid"] = False
            message_result["error_message"] = "はらった金額は1以上の半角数字で入力してください"
            return message_result
        if len(pay_message) > 150:
            message_result["isValid"] = False
            message_result["error_message"] = "メッセージが長すぎます"
            return message_result
        message_result["args"] = (int(amount), pay_message)
        return message_result
    return message_result
