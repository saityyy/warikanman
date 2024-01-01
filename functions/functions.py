from pprint import pprint


def create_projects(conn, date_time, group_id, participant_number):
    cur = conn.cursor(dictionary=True)
    # すでにプロジェクトが存在する場合は削除
    cur.execute("SELECT * FROM projects WHERE group_id=%s;", (group_id,))
    if len(cur.fetchall()) > 0:
        cur.execute("DELETE FROM projects WHERE group_id=%s;", (group_id,))
    cur.execute("INSERT INTO projects (group_id,datetime,participant_number) VALUES(%s,%s,%s);",
                (group_id, date_time, participant_number))
    conn.commit()
    res = "参加人数{}人の割り勘プロジェクトを作成しました".format(participant_number)
    return res


def add_payment(conn, group_id, user_id, name, date_time, amount, message):
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM projects WHERE group_id=%s;", (group_id,))
    project_id = cur.fetchall()[0]["id"]
    cur.execute("SELECT name FROM users WHERE user_id=%s;", (user_id,))
    result = cur.fetchall()
    # ユーザーが存在しない場合は追加
    if len(result) == 0:
        cur.execute(
            "INSERT INTO users (user_id,name) VALUES(%s,%s);", (user_id, name))
    # ユーザー名が変更されている場合は更新
    elif result[0]["name"] != name:
        cur.execute("UPDATE users SET name=%s WHERE user_id=%s;",
                    (name, user_id))
    cur.execute("INSERT INTO payments (project_id,user_id,datetime,amount,message) VALUES(%s,%s,%s,%s,%s);",
                (project_id, user_id, date_time, amount, message))
    conn.commit()
    res = "記録しました\n"
    res += "{} : {}円\n".format(name, amount)
    if message != "":
        res += "メッセージ : {}".format(message)
    return res


def check_payments_log(conn, group_id):
    cur = conn.cursor(dictionary=True)
    query = """
        SELECT id,datetime,(SELECT name from users WHERE user_id=p.user_id) user_name,
        amount,message FROM payments p WHERE project_id=
        (SELECT project_id FROM projects WHERE group_id=%s)
        ORDER BY datetime ASC;
    """
    cur.execute(query, (group_id,))
    res = ""
    result = cur.fetchall()
    for idx, row in enumerate(result, start=1):
        datetime_str = row["datetime"].strftime("%-m/%-d %-H:%M")
        res += "{}) {}\n".format(idx, datetime_str)
        res += "{}\n{}円\n{}\n\n".format(row["user_name"],
                                        row["amount"], row["message"])
    res += "合計 : {}円".format(sum([row["amount"] for row in result]))
    conn.commit()
    return res


def warikan(conn, group_id):
    cur = conn.cursor(dictionary=True)
    # paymentsテーブルからプロジェクトIDが一致するものを取得
    query = """
        SELECT (SELECT name from users WHERE user_id=p.user_id) user_name,
        amount,message FROM payments p WHERE project_id=
        (SELECT project_id FROM projects WHERE group_id=%s);
    """
    cur.execute(query, (group_id,))
    result = cur.fetchall()
    # project's participants number
    cur.execute(
        "SELECT participant_number FROM projects WHERE group_id=%s;", (group_id,))
    participant_number = cur.fetchall()[0]["participant_number"]
    user2amount = {}
    # 合計金額を計算
    total_amount = 0
    for row in result:
        total_amount += row["amount"]
        if row["user_name"] not in user2amount.keys():
            user2amount[row["user_name"]] = 0
        user2amount[row["user_name"]] += row["amount"]
    fraction = total_amount % participant_number
    amount_per_user = int(total_amount/participant_number)
    res = "合計金額 : {}円\n".format(total_amount)
    res += "参加人数 : {}人\n".format(participant_number)
    res += "一人あたりの金額 : {}円\n\n".format(amount_per_user)
    res += "端数 : {}円\n\n".format(fraction)
    for name, amount in user2amount.items():
        res += "{} : {}円".format(name, amount)
        if amount > amount_per_user:
            res += "（{}円もらう）\n".format(amount-amount_per_user)
        else:
            res += "（{}円はらう）\n".format(amount_per_user-amount)
    other_num = participant_number-len(user2amount)
    if other_num > 0:
        for _ in range(other_num):
            res += "{} : {}円\n".format("その他の参加者", -amount_per_user)
    res = res[:-1]
    return res


def delete_payment(conn, group_id, delete_number):
    # project_idが一致するものをdatetimeでソートして、古い方からindex番目のものを削除
    query = """
        SELECT id FROM payments WHERE project_id=
        (SELECT project_id FROM projects WHERE group_id=%s)
        ORDER BY datetime ASC;
    """
    cur = conn.cursor(dictionary=True)
    cur.execute(query, (group_id,))
    result = cur.fetchall()
    if not (0 <= delete_number-1 < len(result)):
        return "その番号の記録は存在しません"
    cur.execute("DELETE FROM payments WHERE id=%s;",
                (result[delete_number-1]["id"],))
    conn.commit()
    return "{}番の記録を削除しました".format(delete_number)


def extract_message(message):
    messages = message.split()
    res = {
        "type": "",
        "args": (),
        "isValid": True,
        "error_message": ""
    }
    if messages[0] == "!help":
        res["type"] = "help"
    elif messages[0] == "!check":
        res["type"] = "check"
    elif messages[0] == "!log":
        res["type"] = "log"
    elif messages[0] == "!project":
        participant_number = message.split()[1]
        res["type"] = "project"
        res["args"] = (participant_number)
        if not (participant_number.isdigit() and int(participant_number) > 0):
            res["isValid"] = False
            res["error_message"] = "参加人数は1以上の半角数字で入力してください"
        return res
    elif messages[0] == "!delete":
        index = message.split()[1]
        res["type"] = "delete"
        res["args"] = (index)
    elif messages[0] == "!pay":
        amount = messages[1]
        message = " ".join(messages[2:])
        res["type"] = "pay"
        res["args"] = (amount, message)
    else:
        res["type"] = "pass"
    return res
