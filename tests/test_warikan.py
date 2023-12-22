import random
import unittest
import mysql.connector

from functions.functions import create_projects,add_payment,warikan

TEMP_TIMESTAMP="2020-01-01 00:00:00"

def random_group_id():
    return random.randint(1,100000)

class Test(unittest.TestCase):
    def setUp(self):
        self.conn=mysql.connector.connect(
            user="warikanman",
            password="warikanman",
            host="127.0.0.1",
            database="warikanman"
        )
        if not self.conn.is_connected():
            raise Exception("failed connect mysql")
        cur=self.conn.cursor(dictionary=True)
        #tableの初期化
        cur.execute("DELETE FROM projects;")
        cur.execute("DELETE FROM users;")
        cur.execute("DELETE FROM payments;")

        self.conn.commit()
    
    def test_warikan(self):
        gid=random_group_id()
        _=create_projects(self.conn,gid,3)
        _=add_payment(self.conn,gid,1,"user1",TEMP_TIMESTAMP,1000,"message1")
        _=add_payment(self.conn,gid,2,"user2",TEMP_TIMESTAMP,2000,"message2")
        _=add_payment(self.conn,gid,3,"user3",TEMP_TIMESTAMP,3000,"message3")
        _=add_payment(self.conn,gid,1,"user1",TEMP_TIMESTAMP,1000,"message4")
        result=warikan(self.conn,gid)
        f=open("./tests/txt/test_warikan_a")
        self.assertEqual(result,f.read())
        f.close()


    
    def tearDown(self):
        self.conn.close()


