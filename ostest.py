import re 

a="aaa   aaa  aa a  a"
b=a.split(" ")
b=[i for i in b if len(i)>0]
price="f2020年fjdf"
price=float(re.sub(r"\D","",price))
mes="project"
print(mes[:5])
if mes[:3] in ["pro"]:
    print(mes[:3])