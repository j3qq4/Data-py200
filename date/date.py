from typing import overload


class TimeDelta:
    """Класс для работы со временем"""
    def __init__(self, days: int = 0, months: int = 0, years: int = 0):
        """Создание времянной задержки"""
        self.day = days
        self.month = months
        self.year = years


    @staticmethod
    def __correct_value(value):
        if isinstance(value, int):
            if 0 > value:
                raise ValueError
            return value
        else:
            raise TypeError

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, value: int):
        """Проверять значение и корректность дней"""
        self._day = self.__correct_value(value)

    @property
    def month(self):
        return self._month

    @month.setter
    def month(self, value: int):
        """Проверять значение и корректность месяцев"""
        self._month = self.__correct_value(value)

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value: int):
        """Проверять значение и корректность года"""
        self._year = self.__correct_value(value)

    def __str__(self) -> str:
        """Возвращает дату в формате dd.mm.yyyy"""
        return f"{self._day}.{self._month}.{self._year}"


class Date:
    """Класс для работы с датами"""

    MAX_DAY_ON_MONTH = (31, 15, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)#29

    @overload
    def __init__(self, day: int, month: int, year: int):
        """Создание даты из трех чисел"""

    @overload
    def __init__(self, date: str):
        """Создание даты из строки формата dd.mm.yyyy"""

    def __init__(self, *args, **kwargs):
        """Создание даты"""

        len_args = len(args)
        len_kwargs = len(kwargs)
        d_arg = [None, None, None]

        if len_args + len_kwargs == 3:
            for i in kwargs:
                if i == "day" and d_arg[0] is None:
                    d_arg[0] = kwargs[i]
                elif i == "month" and d_arg[1] is None:
                    d_arg[1] = kwargs[i]
                elif i == "year" and d_arg[2] is None:
                    d_arg[2] = kwargs[i]
                else:
                    raise ValueError("Arguments Error, ('day', 'month', 'year')")

            for i in args:
                for j in range(3):
                    if d_arg[j] is None:
                        d_arg[j] = i
                        break

        elif len_args == 1 and len_kwargs == 0 or len_args == 0 and len_kwargs == 1:
            if len_args and isinstance(args[0], str):
                date_str = args[0].replace(' ', '').split(".")
            elif "date" in kwargs:
                date_str = kwargs["date"].replace(' ', '').split(".")
            else:
                raise ValueError("Arguments Error (date=)")

            if len(date_str) == 3 and all(date.isdigit() for date in date_str):
                d_arg[0] = int(date_str[0])
                d_arg[1] = int(date_str[1])
                d_arg[2] = int(date_str[2])
            else:
                raise ValueError("Arguments Error, (dd.mm.yyyy)")

        else:
            raise ValueError("Arguments error")

        if not self.is_valid_date(d_arg[0], d_arg[1], d_arg[2]):
            raise ValueError

        self._day, self._month, self._year = d_arg

    @staticmethod
    def is_leap_year(year: int) -> bool:
        """Проверяет, является ли год високосным"""

        if not isinstance(year, int) or 0 >= year:
            raise TypeError
        if year % 4 != 0 or year % 100 == 0 and year % 400 != 0:
            return False
        return True

    @classmethod
    def get_max_day(cls, month: int, year: int) -> int:
        """Возвращает максимальное количество дней в месяце для указанного года"""
        if not isinstance(month, int) or not isinstance(year, int):
            raise TypeError

        if 1 > month or month > 12 or year < 1:
            raise ValueError

        if month != 2:
            return cls.MAX_DAY_ON_MONTH[month - 1]

        if cls.is_leap_year(year):
            return cls.MAX_DAY_ON_MONTH[1]
        else:
            return cls.MAX_DAY_ON_MONTH[1] - 1

    @classmethod
    def is_valid_date(cls, day: int, month: int, year: int) -> bool:
        """Проверяет, является ли дата корректной"""
        if not isinstance(month, int) or not isinstance(year, int) or not isinstance(day, int):
            raise TypeError

        if cls._range_month(day, month, year) and \
                cls._range_day(day, month, year) and \
                cls._range_year(day, month, year):
            return True
        return False

    @staticmethod
    def day_in_date(date: "Date") -> int:
        """Считаем количество дней, начиная с 1 января 1 года до указанной даты"""
        if not isinstance(date, Date):
            raise TypeError

        day = 0
        for i in range(1, date.year):
            day += 366 if date.is_leap_year(i) else 365

        for j in range(1, date.month):
            day += date.get_max_day(j, date.year)

        day += date.day - 1

        return day

    @classmethod
    def _range_day(cls, day, month, year) -> bool:
        """Допустимые значения для дней"""
        return 0 < day <= cls.get_max_day(month, year)

    @classmethod
    def _range_month(cls, day, month, year) -> bool:
        """Допустимые значения для месяцев"""
        if not cls._range_day(day, month, year):
            return False
        return 0 < month < 13

    @classmethod
    def _range_year(cls, day, month, year) -> bool:
        if not cls._range_day(day, month, year):
            return False
        return 0 < year

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, value: int):
        """Проверять значение и корректность дней"""
        if isinstance(value, int):
            if not self._range_day(value, self._month, self._year):
                raise ValueError
            self._day = value
        else:
            raise TypeError

    @property
    def month(self):
        return self._month

    @month.setter
    def month(self, value: int):
        """Проверять значение и корректность месяцев"""
        if isinstance(value, int):
            if not self._range_month(self._day, value, self._year):
                raise ValueError
            self._month = value
        else:
            raise TypeError

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value: int):
        """Проверять значение и корректность года"""
        if isinstance(value, int):
            if not self._range_year(self._day, self._month, value):
                raise ValueError
            self._year = value
        else:
            raise TypeError

    def __str__(self) -> str:
        """Возвращает дату в формате dd.mm.yyyy"""
        return f"{self._day}.{self._month}.{self._year}"

    def __sub__(self, other: "Date") -> int:
        """Разница между датой self и other (-)"""
        if not isinstance(other, Date):
            return NotImplemented
        return self.day_in_date(self) - self.day_in_date(other)

    def __add__(self, other: TimeDelta) -> "Date":
        """Складывает self и некий timedeltа. Возвращает НОВЫЙ инстанс Date, self не меняет (+)"""
        if isinstance(other, TimeDelta):
            new_date = Date(self._day, self._month, self._year)
            new_date += other
            return new_date
        else:
            return NotImplemented

    def __repr__(self) -> str:
        """Возвращает дату в формате Date(day, month, year)"""
        return f"Date({self._day}, {self._month}, {self._year})"

    def __iadd__(self, other: TimeDelta) -> "Date":
        """Добавляет к self некий timedelta, меняя сам self (+=)"""
        if isinstance(other, TimeDelta):
            self._month += other.month
            self._year += other.year + (self._month - 1) // 12
            self._month = (self._month - 1) % 12 + 1
            self._day += other.day
            mx = self.get_max_day(self._month, self._year)
            while self._day > mx:
                self._day -= mx
                if self._month < 12:
                    self._month += 1
                else:
                    self._month = 1
                    self._year += 1
                mx = self.get_max_day(self._month, self._year)

            return self
        else:
            return NotImplemented
