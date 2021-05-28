import re

a = "aaa   aaa  aa a  a"
b = a.split(" ")
b = [i for i in b if len(i) > 0]
price = "project3"
price = int(re.sub(r"\D", "", price))
List = [1, 2, 3]
del List[1]
print(List)
