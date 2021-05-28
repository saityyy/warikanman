import datetime
import re

class Project:
    def __init__(self,project_name,user):
        self.project_name=project_name
        dt_now=datetime.datetime.now()
        date={
            "year":dt_now.year,
            "month":dt_now.month,
            "day":dt_now.day,
            "hour":dt_now.hour,
            "minute":dt_now.minute,
        }
        self.commit_data=[{
            "user":user,
            "commit_time":date,
            "pay_money":-1,
            "message":"",
        }]
    
    def log_data(self):
        log=""
        for data in self.commit_data:
            d=data["commit_time"]
            log+="{}年{}月{}日 {}:{}\n".format(
                d["year"],
                d["month"],
                d["day"],
                d["hour"],
                d["minute"],
            )
            if data["pay_money"]==-1:
                log+="{}がプロジェクトを作成しました\n\n".format(data["user"])
            else:
                log+="{}\n".format(data["user"])
                log+="{}円\n".format(int(data["pay_money"]))
                log+="{}\n\n".format(data["message"])
        return log

    
    def pay_money(self,user,message):
        _,price,message=[mes for mes in message.split(" ") if len(mes)>0 ]
        price=float(re.sub(r"\D","",price))
        dt_now=datetime.datetime.now()
        date={
            "year":dt_now.year,
            "month":dt_now.month,
            "day":dt_now.day,
            "hour":dt_now.hour,
            "minute":dt_now.minute,
        }
        self.commit_data.append({
            "user":user,
            "commit_time":date,
            "pay_money":price,
            "message":message
        })
    
