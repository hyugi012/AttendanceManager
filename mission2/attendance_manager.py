from collections import defaultdict
from mission2.grade import StandardGradePolicy, GradePolicy
from mission2.point import AttendancePoint, StandardAttendancePoint, BonusPoint, StandardBonusPoint


class AttendanceManager:
    def __init__(self,
                 attendance_policy: AttendancePoint = None,
                 bonus_policy: BonusPoint = None,
                 grade_policy: GradePolicy = None):
        self.records = defaultdict(list)
        self.points = defaultdict(int)
        self.attendance_policy = attendance_policy or StandardAttendancePoint()
        self.bonus_policy = bonus_policy or StandardBonusPoint()
        self.grade_policy = grade_policy or StandardGradePolicy()

    def load_attendance_file(self, file_name: str) -> None:
        try:
            with open(file_name, encoding="utf-8") as f:
                for line in f:
                    data = line.strip().split()
                    if len(data) == 2:
                        name, day = data
                        self.add_record(name, day)
                    else:
                        raise ValueError("잘못된 데이터가 입력되었습니다.")

        except FileNotFoundError:
            raise FileNotFoundError("파일을 찾을 수 없습니다.")

    def add_record(self, name: str, day: str):
        self.records[name].append(day)
        self.points[name] += self.attendance_policy.get_point(day)

    def finalize(self):
        self.bonus_policy.apply(self.records, self.points)

    def get_result(self):
        self.finalize()
        results = {}
        for name, point in self.points.items():
            results[name] = {
                "point": point,
                "grade": self.grade_policy.grade(point)
            }
        return results

    def get_removed_players(self):
        removed = []
        for name, days in self.records.items():
            is_normal = self.grade_policy.grade(self.points[name]) == "NORMAL"
            remove_condition = "wednesday" not in days and not any(d in ("saturday", "sunday") for d in days)
            if is_normal and remove_condition:
                removed.append(name)
        return removed
