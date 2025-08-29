import unittest
from idlelib.run import manage_socket
from unittest.mock import patch, mock_open
from mission2.attendance_manager import AttendanceManager


class TestAttendanceManager(unittest.TestCase):
    def test_file_loading_and_get_result(self):
        file_path = "mission2/attendance_weekday_500.txt"
        manager = AttendanceManager()
        manager.load_attendance_file(file_path)
        result = manager.get_result()
        self.assertEqual(result["Alice"]["point"], 61)
        self.assertEqual(result["Alice"]["grade"], "GOLD")

    def test_file_loading_wrong_file_name(self):
        file_path = "mission2/attendance_weekday_500_wrong.txt"
        manager = AttendanceManager()
        with self.assertRaises(FileNotFoundError) as e:
            manager.load_attendance_file(file_path)

        self.assertEqual(str(e.exception), "파일을 찾을 수 없습니다.")

    def test_file_loading_wrong_data(self):
        m = mock_open(read_data="Alice monday sunday\n")
        with patch('mission2.attendance_manager.open', m) as mock_file:
            manager = AttendanceManager()
            filepath = 'dummy_file.txt'
            with self.assertRaises(ValueError) as e:
                manager.load_attendance_file(filepath)

            self.assertEqual(str(e.exception), "잘못된 데이터가 입력되었습니다.")
            mock_file.assert_called_once_with(filepath, encoding='utf-8')
            m.return_value.__exit__.assert_called_once()

    def test_add_record_and_points(self):
        manager = AttendanceManager()
        manager.add_record("Alice", "monday")
        manager.add_record("Alice", "wednesday")
        manager.add_record("Alice", "sunday")
        self.assertEqual(manager.points["Alice"], 6)  # 1 + 3 + 2

    def test_bonus_policy_for_wednesday(self):
        manager = AttendanceManager()
        for _ in range(10):
            manager.add_record("Bob", "wednesday")
        manager.finalize()
        self.assertEqual(manager.points["Bob"], 40)  # 30 + 10 bonus

    def test_bonus_policy_for_saturday_and_sunday(self):
        manager = AttendanceManager()
        for _ in range(5):
            manager.add_record("Bob", "saturday")
            manager.add_record("Bob", "sunday")
        manager.finalize()
        self.assertEqual(manager.points["Bob"], 30)  # 20 + 10 bonus

    def test_bonus_policy_for_wednesday_saturday_sunday(self):
        manager = AttendanceManager()
        for _ in range(10):
            manager.add_record("Bob", "wednesday")
        for _ in range(5):
            manager.add_record("Bob", "saturday")
            manager.add_record("Bob", "sunday")
        manager.finalize()
        self.assertEqual(manager.points["Bob"], 70)  # 30 + 20 + 10 + 10 bonus

    def test_bonus_policy_for_no_wednesday_saturday_sunday(self):
        manager = AttendanceManager()
        for _ in range(10):
            manager.add_record("Bob", "monday")
        for _ in range(5):
            manager.add_record("Bob", "friday")
            manager.add_record("Bob", "tuesday")
        manager.finalize()
        self.assertEqual(manager.points["Bob"], 20)  # 10 + 5 + 5  bonus

    def test_removed_player(self):
        manager = AttendanceManager()
        manager.add_record("Chris", "monday")
        manager.finalize()
        removed = manager.get_removed_players()
        self.assertIn("Chris", removed)


if __name__ == '__main__':
    unittest.main()
