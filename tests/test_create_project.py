import random
import unittest
import mysql.connector
import datetime

from functions.functions import create_projects

TEMP_TIMESTAMP = datetime.datetime(2020, 1, 1, 0, 0, 0)


def random_group_id() -> str:
    return str(random.randint(1, 1_000_000_000))


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
        self.conn.commit()

    def test_create_project_normal_a(self):
        gid = random_group_id()
        result = create_projects(self.conn, TEMP_TIMESTAMP, gid, 3)
        self.assertEqual(result, "参加人数3人の割り勘プロジェクトを作成しました")

    def test_create_project_normal_b(self):
        gid = random_group_id()
        _ = create_projects(self.conn, TEMP_TIMESTAMP, gid, 3)
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM projects WHERE project_id=%s;", (gid,))
        result_sql = cur.fetchall()[0]["participant_number"]  # type: ignore
        self.assertEqual(result_sql, 3)

    def test_create_project_overwrite(self):
        gid = random_group_id()
        _ = create_projects(self.conn, TEMP_TIMESTAMP, gid, 3)
        _ = create_projects(self.conn, TEMP_TIMESTAMP, gid, 10)
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM projects WHERE project_id=%s;", (gid,))
        result_sql = cur.fetchall()[0]["participant_number"]  # type: ignore
        self.assertEqual(result_sql, 10)

    def tearDown(self):
        cur = self.conn.cursor(dictionary=True)
        cur.execute("DELETE FROM projects;")
        cur.execute("DELETE FROM users;")
        cur.execute("DELETE FROM payments;")
        self.conn.commit()
        self.conn.close()
