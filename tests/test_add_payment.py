import random
import unittest
import mysql.connector
import datetime

from functions.functions import create_projects, add_payment

TEMP_DATETIME = datetime.datetime(2020, 1, 1, 0, 0, 0)


def random_group_id():
    return str(random.randint(1, 100000))


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
        result = add_payment(self.conn, gid, "0", "user0",
                             TEMP_DATETIME, 1000, "メッセージ")
        f = open("./tests/txt/test_add_payment")
        self.assertEqual(result, f.read())
        f.close()

    def test_add_payment_newuser(self):
        gid = random_group_id()
        _ = create_projects(self.conn, TEMP_DATETIME, gid, 3)
        result = add_payment(self.conn, gid, "1", "user1",
                             TEMP_DATETIME, 1000, "メッセージ")
        f = open("./tests/txt/test_add_payment_newuser")
        self.assertEqual(result, f.read())
        f.close()

    def test_add_payment_rename(self):
        gid = random_group_id()
        _ = create_projects(self.conn, TEMP_DATETIME, gid, 3)
        result = add_payment(self.conn, gid, "1", "user1_rename",
                             TEMP_DATETIME, 1000, "メッセージ")
        f = open("./tests/txt/test_add_payment_rename")
        self.assertEqual(result, f.read())
        f.close()

    # プロジェクトが存在しない場合
    def test_add_payment_noproject(self):
        gid = random_group_id()
        result = add_payment(self.conn, gid, "0", "user0",
                             TEMP_DATETIME, 1000, "メッセージ")
        self.assertEqual(result, "プロジェクトが存在しません")

    def test_add_payment_user_exceeded(self):
        gid = random_group_id()
        _ = create_projects(self.conn, TEMP_DATETIME, gid, 3)
        _ = add_payment(self.conn, gid, "0", "user0",
                        TEMP_DATETIME, 1000, "メッセージ")
        _ = add_payment(self.conn, gid, "1", "user1",
                        TEMP_DATETIME, 1000, "メッセージ")
        _ = add_payment(self.conn, gid, "2", "user2",
                        TEMP_DATETIME, 1000, "メッセージ")
        result = add_payment(self.conn, gid, "3", "user3",
                             TEMP_DATETIME, 1000, "メッセージ")
        self.assertEqual(result, "設定した参加人数を超えています")

    def tearDown(self):
        cur = self.conn.cursor(dictionary=True)
        cur.execute("DELETE FROM projects;")
        cur.execute("DELETE FROM users;")
        cur.execute("DELETE FROM payments;")
        self.conn.commit()
        self.conn.close()
