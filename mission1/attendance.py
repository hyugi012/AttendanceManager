from collections import defaultdict


def load_attendance_file(file_name: str):
    records = defaultdict(list)

    try:
        with open(file_name, encoding='utf-8') as f:
            for line in f:
                data = line.strip().split()
                if len(data) == 2:
                    name, day = data
                    records[name].append(day)
                else:
                    raise ValueError("NOT expected input data.")

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")

    return records


def calculate_daily_point(day: str) -> int:
    if day == "wednesday":
        return 3
    elif day in ("saturday", "sunday"):
        return 2
    return 1


def apply_bonus_point(records: dict, points: dict) -> None:
    for name, days in records.items():
        if days.count("wednesday") >= 10:
            points[name] += 10
        if sum(1 for d in days if d in ("saturday", "sunday")) >= 10:
            points[name] += 10


def assign_grade(point: int) -> str:
    if point >= 50:
        return "GOLD"
    elif point >= 30:
        return "SILVER"
    return "NORMAL"


def get_removed_players(records: dict, points: dict) -> list:
    removed = []
    for name, days in records.items():
        grade = assign_grade(points[name])
        if grade == "NORMAL":
            if "wednesday" not in days and not any(d in ("saturday", "sunday") for d in days):
                removed.append(name)
    return removed


def get_evaluate_result(points) -> dict:
    results = {}
    for name, point in points.items():
        results[name] = {
            "point": point,
            "grade": assign_grade(point)
        }

    return results


def calculate_attendance_point(records: dict) -> dict:
    points = defaultdict(int)
    for name in records.keys():
        for day in records[name]:
            points[name] += calculate_daily_point(day)

    apply_bonus_point(records, points)

    return points


if __name__ == "__main__":
    records = load_attendance_file("attendance_weekday_500.txt")
    points = calculate_attendance_point(records)
    results = get_evaluate_result(points)
    removed = get_removed_players(records, points)

    for name, info in results.items():
        print(f"NAME : {name}, POINT : {info['point']}, GRADE : {info['grade']}")

    print("\nRemoved player")
    print("==============")
    for name in removed:
        print(name)
