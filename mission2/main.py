from attendance_manager import AttendanceManager

if __name__ == "__main__":  # pragma: no cover
    attendance_file_name = "attendance_weekday_500.txt"
    attendance_manager = AttendanceManager()
    attendance_manager.load_attendance_file(attendance_file_name)
    result = attendance_manager.get_result()

    for name, info in result.items():
        print(f"NAME : {name}, POINT : {info['point']}, GRADE : {info['grade']}")

    print("\nRemoved player")
    print("==============")
    for name in attendance_manager.get_removed_players():
        print(name)
