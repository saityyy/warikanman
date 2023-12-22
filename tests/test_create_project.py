import random
import unittest
import mysql.connector

from functions.functions import create_projects

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
    def test_create_project_a(self):
        gid=random_group_id()
        result=create_projects(self.conn,gid,3)
        self.assertEqual(result,"参加人数3人の割り勘プロジェクトを作成しました")
    def test_create_project_b(self):
        gid=random_group_id()
        _=create_projects(self.conn,gid,3)
        result=create_projects(self.conn,gid,10)
        self.assertEqual(result,"参加人数10人の割り勘プロジェクトを作成しました")

    def tearDown(self):
        self.conn.close()