import datetime
import re
import pytz


class Project:
    def __init__(self, user, participants):
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
        log += "合計 : {}".format(self.sum)
        return log

    def pay_money(self, user, message):
        _, price, message = message.split()
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
            "user": user,
            "commit_time": date,
            "pay_money": price,
            "message": message
        })
        self.sum += price

    def check_payment(self):
        members = {}
        sum = 0
        for data in self.commit_data:
            pay_user = data["user"]
            pay_money = data["pay_money"]
            if pay_user in members.keys():
                members[pay_user] = 0
            members[pay_user] += pay_money
            sum += pay_money
        result = "集計結果\n\n"
        for member, money in members.items():
            result += "{} : +{}\n".format(member, money)
        other_num = self.participants-len(members)
        money_per_member = sum/other_num
        for other in range(self.participants-len(members)):
            result += "{} : -{}\n".format(member, money_per_member)

        return result
