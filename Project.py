import datetime
import re
import pytz


class Project:
    def __init__(self, user_id, user, participants):
        self.participants = participants
        self.sum = 0
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
            "pay_money": -1,
            "message": "",
        }]

    def log_data(self):
        log = ""
        for data in self.commit_data:
            d = data["commit_time"]
            log += "{}年{}月{}日 {}:{}\n".format(
                d["year"],
                d["month"],
                d["day"],
                d["hour"],
                d["minute"],
            )
            if data["pay_money"] == -1:
                log += "{}がプロジェクトを作成しました\n".format(data["user"])
                log += "参加人数：{}人\n\n".format(self.participants)
            else:
                log += "{}\n".format(data["user"])
                log += "{}円\n".format(int(data["pay_money"]))
                log += "{}\n\n".format(data["message"])
        log += "合計 : {}".format(int(self.sum))
        return log

    def pay_money(self, user_id, user, message):
        if len(message.split()) == 2:
            _, price = message.split()
        else:
            _, price = message.split()[:2]
            message = message.split()[2]

        price = float(re.sub(r"\D", "", price))
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
            "pay_money": price,
            "message": message
        })
        self.sum += price

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
        result = "集計結果\n\n"
        money_per_member = _sum/self.participants
        for v in members.values():
            result += "{} : +{}\n".format(v["pay_user_name"],
                                          abs(v["pay_money"]-money_per_member))
        other_num = self.participants-len(members)
        if other_num > 0:
            for other in range(other_num):
                result += "{} : -{}\n".format("その他の参加者", money_per_member)
        return result
