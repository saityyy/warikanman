import datetime
import re
import pytz


class Project:
    def __init__(self, user_id, user, participants):
        self.participants = participants
        dt_now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
        date = {
            "year": dt_now.year,
            "month": dt_now.month,
            "day": dt_now.day,
            "hour": dt_now.hour,
            "minute": dt_now.minute,
        }
        self.commit_data = [{
            "id": user_id,
            "user": user,
            "commit_time": date,
            "pay_money": 0,
            "message": "",
        }]

    def log_data(self):
        log = ""
        _sum = 0
        for i, data in enumerate(self.commit_data):
            d = data["commit_time"]
            if i > 0:
                log += str(i)+")"
            log += "{}年{}月{}日 {}:{}\n".format(
                d["year"],
                d["month"],
                d["day"],
                d["hour"],
                d["minute"],
            )
            if data["pay_money"] == 0:
                log += "{}がプロジェクトを作成しました\n".format(data["user"])
                log += "参加人数：{}人\n\n".format(self.participants)
            else:
                log += "{}\n".format(data["user"])
                log += "{}円\n".format(int(data["pay_money"]))
                log += "{}\n\n".format(data["message"])
                _sum += data["pay_money"]
        log += "合計 : {}円".format(_sum)
        return log

    def pay_money(self, user_id, user, message):
        res_message = "なし"
        if len(message.split()) == 2:
            _, price = message.split()
        else:
            _, price = message.split()[:2]
            res_message = message.split()[2]

        price = re.sub(r"\D", "", price)
        if len(price) == 0 or int(price) == 0:
            return "有効な数字を入力してください"
        dt_now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
        date = {
            "year": dt_now.year,
            "month": dt_now.month,
            "day": dt_now.day,
            "hour": dt_now.hour,
            "minute": dt_now.minute,
        }
        self.commit_data.append({
            "id": user_id,
            "user": user,
            "commit_time": date,
            "pay_money": float(price),
            "message": res_message
        })
        result = "記録しました\n"
        result += "払った人：{}\n".format(user)
        result += "払った金額：{}円\n".format(float(price))
        result += "メッセージ：{}\n".format(res_message)
        return result

    def delete_record(self, index):
        if 0 < index < len(self.commit_data):
            del self.commit_data[index]
            return "削除しました"
        else:
            return "有効な番号を指定してください"

    def check_payment(self):
        members = {}
        _sum = 0
        for data in self.commit_data:
            pay_user_id = data["id"]
            pay_money = data["pay_money"]
            pay_user_name = data["user"]
            if pay_user_id not in members.keys():
                members[pay_user_id] = {}
                members[pay_user_id]["pay_user_name"] = pay_user_name
                members[pay_user_id]["pay_money"] = 0
            members[pay_user_id]["pay_money"] += pay_money
            _sum += pay_money
        money_per_member = _sum/self.participants
        result = "集計結果\n\n"
        result += "合計金額 : {}円\n".format(_sum)
        result += "一人あたりの金額 : {}円\n\n".format(money_per_member)
        for v in members.values():
            result += "{} : {}円\n".format(v["pay_user_name"],
                                          v["pay_money"]-money_per_member)
        other_num = self.participants-len(members)
        if other_num > 0:
            for other in range(other_num):
                result += "{} : {}円\n".format("その他の参加者",
                                              -money_per_member)
        return result
