class test:
    def __init__(self,a):
        self.a=a

from Project import Project
project={}

if __name__=="__main__":
    project["test"]=Project("test ",1)
    print(project["test"].project_name)