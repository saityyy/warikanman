import datetime
import re
import pytz


class Project:
    def __init__(self, user, participants):
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

    def check_payment(self):
        return
