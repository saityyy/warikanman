import unittest

from functions.functions import extract_message


def get_response(command_type, error_message, args=()):
    if error_message == "":
        isValid = True
    else:
        isValid = False
    return {
        "type": command_type,
        "args": args,
        "isValid": isValid,
        "error_message": error_message
    }


class Test(unittest.TestCase):
    def setUp(self):
        self.VERY_LONG_STRING = "L" * 200
        pass

    def test_extract_message_pass(self):
        self.assertEqual(extract_message("help"), get_response("pass", ""))
        self.assertEqual(extract_message("!hel"), get_response("pass", ""))
        self.assertEqual(extract_message("!"), get_response("pass", ""))

    def test_extract_message_help(self):
        self.assertEqual(extract_message("!help"), get_response("help", ""))
        self.assertEqual(extract_message("!help "), get_response("help", ""))

    def test_extract_message_project_success(self):
        self.assertEqual(extract_message("!project 3"),
                         get_response("project", "", (3,)))
        self.assertEqual(extract_message("!project 3 aaa"),
                         get_response("project", "", (3,)))

    def test_extract_message_project_fail_a(self):
        self.assertEqual(extract_message("!project"),
                         get_response("project", "プロジェクトの参加人数を半角数字で入力してください", ()))

    def test_extract_message_project_fail_b(self):
        self.assertEqual(extract_message("!project 0"),
                         get_response("project", "参加人数は2以上の半角数字で入力してください", ()))
        self.assertEqual(extract_message("!project ten"),
                         get_response("project", "参加人数は2以上の半角数字で入力してください", ()))

    def test_extract_message_pay_success(self):
        self.assertEqual(extract_message("!pay 1000 メッセージ"),
                         get_response("pay", "", (1000, "メッセージ")))
        self.assertEqual(extract_message("!pay 1000"),
                         get_response("pay", "", (1000, "")))
        self.assertEqual(extract_message("!pay 1000 message message message"),
                         get_response("pay", "", (1000, "message message message")))

    def test_extract_message_pay_fail_a(self):
        self.assertEqual(extract_message("!pay"),
                         get_response("pay", "はらった金額を半角数字で入力してください", ()))

    def test_extract_message_pay_fail_b(self):
        self.assertEqual(extract_message("!pay 100円"),
                         get_response("pay", "はらった金額は1以上の半角数字で入力してください", ()))
        self.assertEqual(extract_message("!pay 0"),
                         get_response("pay", "はらった金額は1以上の半角数字で入力してください", ()))

    def test_extract_message_pay_fail_c(self):
        self.assertEqual(extract_message("!pay 1000 {}".format(self.VERY_LONG_STRING)),
                         get_response("pay", "メッセージが長すぎます", ()))

    def test_extract_message_log_success(self):
        self.assertEqual(extract_message("!log"),
                         get_response("log", ""))

    def test_extract_message_check_success(self):
        self.assertEqual(extract_message("!check"),
                         get_response("check", ""))

    def test_extract_message_delete_success(self):
        self.assertEqual(extract_message("!delete 1"),
                         get_response("delete", "", (1,)))

    def test_extract_message_delete_fail_a(self):
        self.assertEqual(extract_message("!delete"),
                         get_response("delete", "削除する記録の通し番号を半角数字で入力してください", ()))

    def test_extract_message_delete_fail_b(self):
        self.assertEqual(extract_message("!delete aaa"),
                         get_response("delete", "通し番号の指定は1以上の半角数字で入力してください", ()))
        self.assertEqual(extract_message("!delete 0"),
                         get_response("delete", "通し番号の指定は1以上の半角数字で入力してください", ()))
