import random
import unittest
import mysql.connector
import datetime

from functions.functions import create_projects, add_payment

TEMP_DATETIME = datetime.datetime(2020, 1, 1, 0, 0, 0)


def random_group_id():
    return random.randint(1, 100000)


class Test(unittest.TestCase):
    def setUp(self):
        self.conn = mysql.connector.connect(
            user="warikanman",
            password="warikanman",
            host="127.0.0.1",
            database="warikanman"
        )
        if not self.conn.is_connected():
            raise Exception("failed connect mysql")
        cur = self.conn.cursor(dictionary=True)
        # tableの初期化
        cur.execute("DELETE FROM projects;")
        cur.execute("DELETE FROM users;")
        cur.execute("DELETE FROM payments;")
        cur.execute("INSERT INTO users (user_id,name) VALUES (%s,%s);",
                    (0, "user0"))
        self.conn.commit()

    def test_add_payment(self):
        gid = random_group_id()
        _ = create_projects(self.conn, TEMP_DATETIME, gid, 3)
        result = add_payment(self.conn, gid, 0, "user0",
                             TEMP_DATETIME, 1000, "メッセージ")
        f = open("./tests/txt/test_add_payment")
        self.assertEqual(result, f.read())
        f.close()

    def test_add_payment_newuser(self):
        gid = random_group_id()
        _ = create_projects(self.conn, TEMP_DATETIME, gid, 3)
        result = add_payment(self.conn, gid, 1, "user1",
                             TEMP_DATETIME, 1000, "メッセージ")
        f = open("./tests/txt/test_add_payment_newuser")
        self.assertEqual(result, f.read())
        f.close()

    def test_add_payment_rename(self):
        gid = random_group_id()
        _ = create_projects(self.conn, TEMP_DATETIME, gid, 3)
        result = add_payment(self.conn, gid, 1, "user1_rename",
                             TEMP_DATETIME, 1000, "メッセージ")
        f = open("./tests/txt/test_add_payment_rename")
        self.assertEqual(result, f.read())
        f.close()

    def tearDown(self):
        cur = self.conn.cursor(dictionary=True)
        cur.execute("DELETE FROM projects;")
        cur.execute("DELETE FROM users;")
        cur.execute("DELETE FROM payments;")
        self.conn.commit()
        self.conn.close()
