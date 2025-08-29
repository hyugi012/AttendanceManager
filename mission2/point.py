from abc import ABC, abstractmethod
from typing import Dict, List


class AttendancePoint(ABC):
    @abstractmethod
    def get_point(self, day: str) -> int:
        raise NotImplementedError


class StandardAttendancePoint(AttendancePoint):
    def get_point(self, day: str) -> int:
        if day == "wednesday":
            return 3
        elif day in ("saturday", "sunday"):
            return 2
        return 1


class BonusPoint(ABC):
    @abstractmethod
    def apply(self, records: Dict[str, List[str]], points: Dict[str, int]):
        raise NotImplementedError


class StandardBonusPoint(BonusPoint):
    def apply(self, records: Dict[str, List[str]], points: Dict[str, int]):
        for name, days in records.items():
            if days.count("wednesday") >= 10:
                points[name] += 10
            if sum(1 for d in days if d in ("saturday", "sunday")) >= 10:
                points[name] += 10
