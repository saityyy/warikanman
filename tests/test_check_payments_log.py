import random
import unittest
import mysql.connector
import datetime

from functions.functions import create_projects, add_payment, check_payments_log

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
        cur.execute("ALTER TABLE projects AUTO_INCREMENT = 1;")
        cur.execute("ALTER TABLE users AUTO_INCREMENT = 1;")
        cur.execute("ALTER TABLE payments AUTO_INCREMENT = 1;")

        self.conn.commit()

    def test_check_payments_log(self):
        gid = random_group_id()
        _ = create_projects(self.conn, TEMP_DATETIME, gid, 3)
        result = add_payment(self.conn, gid, 1, "user1",
                             TEMP_DATETIME+datetime.timedelta(minutes=10), 1000, "message1")
        result = add_payment(self.conn, gid, 2, "user2",
                             TEMP_DATETIME+datetime.timedelta(minutes=20), 2000, "message2")
        result = add_payment(self.conn, gid, 3, "user3",
                             TEMP_DATETIME+datetime.timedelta(minutes=30), 3000, "message3")
        result = add_payment(self.conn, gid, 1, "user1",
                             TEMP_DATETIME+datetime.timedelta(minutes=40), 1000, "")
        result = check_payments_log(self.conn, gid)
        f = open("./tests/txt/test_check_payments_log_a")
        self.assertEqual(result, f.read())
        f.close()

    # プロジェクトが存在しない場合
    def test_check_payments_log_noproject(self):
        gid = random_group_id()
        result = check_payments_log(self.conn, gid)
        self.assertEqual(result, "プロジェクトが存在しません")

    def tearDown(self):
        cur = self.conn.cursor(dictionary=True)
        cur.execute("DELETE FROM projects;")
        cur.execute("DELETE FROM users;")
        cur.execute("DELETE FROM payments;")
        self.conn.commit()
        self.conn.close()
