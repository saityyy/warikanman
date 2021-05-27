import datetime

class Project:
    def __init__(self,project_name,user):
        self.project_name=project_name
        dt_now=datetime.datetime.now()
        #date={
            #"year":dt_now.year,
            #"month":dt_now.month,
            #"day":dt_now.day,
            #"hour":dt_now.hour,
            #"minute":dt_now.minute,
        #}
        #self.commit_data=[{
            #"user":user,
            #"commit_time":date,
            #"pay_money":0,
            #"message":"",
        #}]
    
    def show_log(self):
        log=[]
        for data in self.commit_data:
            d=data["commit_time"]
            _log="{}年{}月{}日 {}:{}\n".format(
                d.year,
                d.month,
                d.day,
                d.hour,
                d.minute
            )
            _log+="{}\n".format(data["user"])
            _log+="{}払いました\n".format(data["pay_money"])
            log.append(_log)
        return log

    
    def add_accounting_data(self,user,pay_money,message=""):
        self.project_name=project_name
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
            "pay_money":pay_money,
            "message":message
        })
    
