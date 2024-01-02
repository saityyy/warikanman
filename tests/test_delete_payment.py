import random
import unittest
import mysql.connector
import datetime

from functions.functions import create_projects, add_payment, delete_payment

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

    def test_delete_payment(self):
        gid = random_group_id()
        _ = create_projects(self.conn, TEMP_DATETIME, gid, 3)
        _ = add_payment(self.conn, gid, 1, "user1",
                        TEMP_DATETIME, 1000, "message1")
        _ = add_payment(self.conn, gid, 2, "user2",
                        TEMP_DATETIME, 2000, "message2")
        _ = add_payment(self.conn, gid, 3, "user3",
                        TEMP_DATETIME, 3000, "message3")
        _ = add_payment(self.conn, gid, 1, "user1",
                        TEMP_DATETIME, 1000, "message4")
        result = delete_payment(self.conn, gid, 1)
        self.assertEqual(result, "1番の記録を削除しました")
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM payments WHERE message=%s;", ("message1",))
        self.assertEqual(cur.fetchall(), [])

    # すべての記録を削除した場合
    def test_delete_payment_alldelete(self):
        gid = random_group_id()
        _ = create_projects(self.conn, TEMP_DATETIME, gid, 3)
        _ = add_payment(self.conn, gid, 1, "user1",
                        TEMP_DATETIME, 1000, "message1")
        _ = add_payment(self.conn, gid, 2, "user2",
                        TEMP_DATETIME, 2000, "message2")
        _ = add_payment(self.conn, gid, 3, "user3",
                        TEMP_DATETIME, 3000, "message3")
        _ = delete_payment(self.conn, gid, 1)
        _ = delete_payment(self.conn, gid, 1)
        _ = delete_payment(self.conn, gid, 1)
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM payments")
        self.assertEqual(cur.fetchall(), [])

    # プロジェクトが存在しない場合
    def test_delete_payment_noproject(self):
        gid = random_group_id()
        result = delete_payment(self.conn, gid, 1)
        self.assertEqual(result, "プロジェクトが存在しません")

    # 指定の番号の記録が存在しない場合
    def test_delete_payment_norecord(self):
        gid = random_group_id()
        _ = create_projects(self.conn, TEMP_DATETIME, gid, 3)
        _ = add_payment(self.conn, gid, 1, "user1",
                        TEMP_DATETIME, 1000, "message1")
        result = delete_payment(self.conn, gid, -1)
        self.assertEqual(result, "その番号の記録は存在しません")
        result = delete_payment(self.conn, gid, 2)
        self.assertEqual(result, "その番号の記録は存在しません")

    def tearDown(self):
        cur = self.conn.cursor(dictionary=True)
        cur.execute("DELETE FROM projects;")
        cur.execute("DELETE FROM users;")
        cur.execute("DELETE FROM payments;")
        self.conn.commit()
        self.conn.close()
