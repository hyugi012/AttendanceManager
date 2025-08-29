from abc import ABC, abstractmethod


class GradeInfo(ABC):
    @classmethod
    @abstractmethod
    def get_grade(cls) -> str:
        raise NotImplementedError


class GoldGrade(GradeInfo):
    GRADE = "GOLD"

    @classmethod
    def get_grade(cls) -> str:
        return cls.GRADE


class SilverGrade(GradeInfo):
    GRADE = "SILVER"

    @classmethod
    def get_grade(cls) -> str:
        return cls.GRADE


class NormalGrade(GradeInfo):
    GRADE = "NORMAL"

    @classmethod
    def get_grade(cls) -> str:
        return cls.GRADE


class GradePolicy(ABC):
    @abstractmethod
    def grade(self, point: int) -> str:
        raise NotImplementedError


class StandardGradePolicy(GradePolicy):
    def grade(self, point: int) -> str:
        if point >= 50:
            return GoldGrade.get_grade()
        elif point >= 30:
            return SilverGrade.get_grade()
        return NormalGrade.get_grade()
