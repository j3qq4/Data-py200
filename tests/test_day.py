import pytest
from date import TimeDelta, Date

"""Test TimeDelta"""


@pytest.mark.parametrize("value", [0, 1, 100, 1000])
def test_timedelta_dey_month_year_good(value):
    td = TimeDelta(value, value, value)
    assert td.day == value
    assert td.month == value
    assert td.year == value
    assert str(td) == f"{value}.{value}.{value}"


def test_timedelta_dey_month_year_bad():
    with pytest.raises(TypeError):
        TimeDelta("str", 1, 1)
    with pytest.raises(ValueError):
        TimeDelta(-1, 1, 1)


"""Test Date"""


def test_date_init_good():
    assert "1.2.3" == str(Date(2, 3, day=1))
    assert "2.1.3" == str(Date(2, 3, month=1))
    assert "1.3.2" == str(Date(year=2, month=3, day=1))
    assert "2.3.1" == str(Date(2, 3, 1))
    assert "2.3.1" == str(Date("2. 3. 1"))
    assert "2.3.1" == str(Date("2.3.1"))
    assert "2.3.1" == str(Date(date="2. 3. 1"))


@pytest.mark.parametrize("value, err", [
    (("5", 1, 1), TypeError),
    ((1, "5", 1), TypeError),
    ((1, 1, "5"), TypeError),
    ((1, 1), ValueError),
    (("5"), ValueError),
    (("5, 5, 7"), ValueError),
    ((32, 1, 1999), ValueError),
    ((1, 13, 1999), ValueError),
    ((3, 1, -1999), ValueError),
    ((1, 99, 1), ValueError),

])
def test_date_init_bad1(value, err):
    """Проверки на Type и Value error в init"""
    with pytest.raises(err):
        Date(*value)


def test_date_init_bad2():
    """Проверки на Type и Value error в init"""
    with pytest.raises(ValueError):
        Date(stt="5")
    with pytest.raises(ValueError):
        Date(1, 1, stt="5")


@pytest.mark.parametrize("day, month, year", [
    (12, 1, 1600),
    (13, 2, 1600),
    (14, 3, 2021),
])
def test_day_month_year_good(day, month, year):
    date = Date(1, 1, 1)
    date.day = day
    date.month = month
    date.year = year
    assert day == date.day
    assert month == date.month
    assert year == date.year


@pytest.mark.parametrize("day, month, year, err", [
    ("12", 1, 1600, TypeError),
    (13, "2", 1600, TypeError),
    (14, 3, "2021", TypeError),
    (0, 1, 1600, ValueError),
    (29, 2, 1601, ValueError),
    (14, 3, 0, ValueError),
])
def test_day_month_year_bad(day, month, year, err):
    date = Date(1, 1, 1)
    with pytest.raises(err):
        date.day = day
        date.month = month
        date.year = year



@pytest.mark.parametrize("value, bo", [
    (1600, True),
    (12, True),
    (2021, False),
    (1999, False)
])
def test_is_leap_year_good(value, bo):
    """Тестируем проверку: является ли год високосным"""

    assert Date.is_leap_year(value) == bo


@pytest.mark.parametrize("value", ["1600", 0])
def test_is_leap_year_bad(value):
    with pytest.raises(TypeError):
        Date.is_leap_year(value)


@pytest.mark.parametrize("day, month, year", [
    (29, 2, 1600),
    (31, 1, 1600),
    (28, 2, 2021),
])
def test_get_max_day_good(day, month, year):
    """Тестируем метод вычисления максимального дня в месяце"""
    assert Date.get_max_day(month, year) == day


@pytest.mark.parametrize("month, year", [
    (2, "1600"),
    ("2", 1222),
    ("2", "1600")
])
def test_get_max_day_bad(month, year):
    with pytest.raises(TypeError):
        Date.get_max_day(month, year)


@pytest.mark.parametrize("day, month, year, bo", [
    (1, 1, 2021, True),
    (29, 2, 2021, False),
    (29, 2, 1600, True)
])
def test_is_valid_date_good(day, month, year, bo):
    """Тестируем функцию проверки валиднасти даты"""
    assert Date.is_valid_date(day, month, year) == bo


@pytest.mark.parametrize("day, month, year", [
    ("5", 1, 1),
    (1, "5", 1),
    (1, 1, "5")
])
def test_is_valid_date_bad(day, month, year):
    """Тестируем функцию проверки валиднасти даты"""
    with pytest.raises(TypeError):
        Date.is_valid_date(day, month, year)


@pytest.mark.parametrize("rez, day, month, year", [
    (0, 1, 1, 1),
    (31, 1, 2, 1),
    (396, 1, 2, 2),
    (365, 1, 1, 2),
    (730, 1, 1, 3),
    (584337, 11, 11, 1600)
])
def test_day_in_date_good(rez, day, month, year):
    """Тестируем функцию продсчета количества дней в дате, начиная с 1 января 1 года"""
    assert rez == Date.day_in_date(Date(day, month, year))


def test_day_in_date_bad():
    with pytest.raises(TypeError):
        Date.day_in_date(5)


@pytest.mark.parametrize("rez, date1, date2", [
    (-365, Date(1, 2, 1), Date(1, 2, 2)),
    (39, Date(9, 2, 2021), Date(1, 1, 2021))
])
def test_sub_good(rez, date1, date2):
    """Тестируем вычитание дат"""
    assert rez == date1 - date2


def test_sub_bad():
    """Тестируем вычитание дат"""
    with pytest.raises(TypeError):
        Date(1, 2, 1) - 5


def test_dey_month_year_good():
    """Проверяем работу ограничений на дни месяцы и годы"""
    d = Date(1, 2, 3)
    assert 1 == d.day
    assert 2 == d.month
    assert 3 == d.year


@pytest.mark.parametrize("day, month, year, err", [
    ("5", "5", 0.6, TypeError),
    (0, 0, 0, ValueError),
    (32, 13, -1, ValueError),
])
def test_dey_month_year_bad1(day, month, year, err):
    d = Date(1, 2, 3)
    with pytest.raises(err):
        d.day = day
    with pytest.raises(err):
        d.month = month
    with pytest.raises(err):
        d.year = year


def test_dey_month_year_bad2():
    d = Date(29, 2, 1600)
    with pytest.raises(ValueError):
        d.year = 1999


@pytest.mark.parametrize("rez, date, time", [
    ("29.2.1600", Date(1, 2, 1600), TimeDelta(28)),
    ("4.3.6", Date(1, 1, 1), TimeDelta(1888)),
    ("11.1.1601", Date(12, 12, 1600), TimeDelta(30)),
    ("2.1.2", Date(1, 12, 1), TimeDelta(1, 1)),
    ("1.12.1", Date(1, 1, 1), TimeDelta(months=11))
])
def test_add_good(rez, date, time):
    """Проверяем операцию +"""
    assert rez == str(date + time)


def test_add_bad():
    """Проверяем операцию +"""
    with pytest.raises(TypeError):
        Date(1, 2, 1600) + 5


def test_repr():
    assert "Date(1, 1, 1)" == repr(Date(1, 1, 1))


@pytest.mark.parametrize("rez, date, time", [
    ("29.2.1600", Date(1, 2, 1600), TimeDelta(28)),
    ("1.1.2", Date(1, 1, 1), TimeDelta(months=12))
])
def test_iadd_good(rez, date, time):
    """Проверяем операцию +="""
    date += time
    assert rez == str(date)


def test_iadd_bad():
    """Проверяем операцию +="""
    with pytest.raises(TypeError):
        d = Date(1, 1, 1)
        d += 5

# import unittest
# from my_date import Date, TimeDelta
#
#
# class TestClassDate(unittest.TestCase):
#     """Тестируем class Date"""
#
#     def test_init_value_error(self):
#         """Проверки на Type и Value error в init"""
#         with self.assertRaises(TypeError):
#             Date("5", 1, 1)
#         with self.assertRaises(TypeError):
#             Date(1, "5", 1)
#         with self.assertRaises(TypeError):
#             Date(1, 1, "5")
#         with self.assertRaises(ValueError):
#             Date(1, 1)
#         with self.assertRaises(ValueError):
#             Date("5")
#         with self.assertRaises(ValueError):
#             Date(1, 99, 1)
#         with self.assertRaises(ValueError, msg="dd.mm.yyyy"):
#             Date("5, 5, 7")
#         with self.assertRaises(ValueError):
#             Date(stt="5")
#         with self.assertRaises(ValueError):
#             Date(1, 1, stt="5")
#         with self.assertRaises(ValueError):
#             Date(32, 1, 1999)
#         with self.assertRaises(ValueError):
#             Date(1, 13, 1999)
#         with self.assertRaises(ValueError):
#             Date(3, 1, -1999)
#
#     def test_init_args_kwargs(self):
#         """Проверка на комбинирование args и kwargs"""
#         self.assertEqual("1.2.3", str(Date(2, 3, day=1)))
#         self.assertEqual("2.1.3", str(Date(2, 3, month=1)))
#         self.assertEqual("1.3.2", str(Date(year=2, month=3, day=1)))
#         self.assertEqual("2.3.1", str(Date(2, 3, 1)))
#         self.assertEqual("2.3.1", str(Date("2. 3. 1")))
#         self.assertEqual("2.3.1", str(Date("2.3.1")))
#         self.assertEqual("2.3.1", str(Date(date="2. 3. 1")))
#
#     def test_is_leap_year(self):
#         """Тестируем проверку: является ли год високосным"""
#         self.assertTrue(Date.is_leap_year(1600))
#         self.assertTrue(Date.is_leap_year(12))
#         self.assertFalse(Date.is_leap_year(2021))
#         self.assertFalse(Date.is_leap_year(1999))
#         with self.assertRaises(TypeError):
#             Date.is_leap_year("1600")
#         with self.assertRaises(TypeError):
#             Date.is_leap_year(0)
#
#     def test_get_max_day(self):
#         """Тестируем метод вычисления максимального дня в месяце"""
#         with self.assertRaises(TypeError):
#             Date.get_max_day(2, "1600")
#         with self.assertRaises(TypeError):
#             Date.get_max_day("2", 1222)
#         with self.assertRaises(TypeError):
#             Date.get_max_day("2", "1600")
#         self.assertEqual(29, Date.get_max_day(2, 1600))
#         self.assertEqual(31, Date.get_max_day(1, 1600))
#         self.assertEqual(28, Date.get_max_day(2, 2021))
#
#     def test_is_valid_date(self):
#         """Тестируем функцию проверки валиднасти даты"""
#
#         with self.assertRaises(TypeError):
#             Date.is_valid_date("5", 1, 1)
#         with self.assertRaises(TypeError):
#             Date.is_valid_date(1, "5", 1)
#         with self.assertRaises(TypeError):
#             Date.is_valid_date(1, 1, "5")
#
#         self.assertTrue(Date.is_valid_date(1, 1, 2021))
#         self.assertFalse(Date.is_valid_date(29, 2, 2021))
#         self.assertTrue(Date.is_valid_date(29, 2, 1600))
#
#     def test_day_in_date(self):
#         """Тестируем функцию продсчета количества дней в дате, начиная с 1 января 1 года"""
#
#         self.assertEqual(1, Date.day_in_date(Date(1, 1, 1)))
#         with self.assertRaises(TypeError):
#             Date.day_in_date(5)
#         self.assertEqual(32, Date.day_in_date(Date(1, 2, 1)))
#         self.assertEqual(397, Date.day_in_date(Date(1, 2, 2)))
#
#     def test_sub(self):
#         """Тестируем вычитание дат"""
#         self.assertEqual(-365, Date(1, 2, 1) - Date(1, 2, 2))
#         self.assertEqual(39, Date(9, 2, 2021) - Date(1, 1, 2021))
#
#     def test_dey_month_year(self):
#         """Проверяем работу ограничений на дни месяцы и годы"""
#
#         d = Date(1, 2, 3)
#         self.assertEqual(1, d.day)
#         self.assertEqual(2, d.month)
#         self.assertEqual(3, d.year)
#
#         with self.assertRaises(TypeError):
#             d.day = "5"
#         with self.assertRaises(ValueError):
#             d.day = 0
#         with self.assertRaises(ValueError):
#             d.day = 32
#
#         with self.assertRaises(TypeError):
#             d.month = "5"
#         with self.assertRaises(ValueError):
#             d.month = 0
#         with self.assertRaises(ValueError):
#             d.month = 13
#
#         with self.assertRaises(TypeError):
#             d.year = "5"
#         with self.assertRaises(TypeError):
#             d.year = 0.6
#         with self.assertRaises(ValueError):
#             d.year = 0
#
#         d.year = 12
#         d.month = 11
#         d.day = 10
#         self.assertEqual(10, d.day)
#         self.assertEqual(11, d.month)
#         self.assertEqual(12, d.year)
#         d.year = 1600
#         d.month = 2
#         with self.assertRaises(ValueError):
#             d.day = 31
#
#     def test_add(self):
#         """Проверяем операцию +"""
#
#         d = Date(1, 1, 1)
#         id_d1 = id(d)
#         d_t = d + TimeDelta(62, 24, 5)
#         id_d2 = id(d)
#         self.assertTrue(id_d2 == id_d1)
#         self.assertEqual("4.3.8", str(d_t))
#         self.assertTrue(id(d_t) != id(d))
#         self.assertEqual("29.2.1600", str(Date(1, 2, 1600) + TimeDelta(28)))
#         with self.assertRaises(TypeError):
#             Date(1, 2, 1600) + 5
#
#     def test_iadd(self):
#         """Проверяем операцию +="""
#
#         d = Date(1, 1, 1)
#         d_t = d
#         d += TimeDelta(62, 24, 5)
#         self.assertEqual("4.3.8", str(d))
#         self.assertTrue(id(d_t) == id(d))
#         with self.assertRaises(TypeError):
#             d += 5
#
#     def test_repr_str(self):
#         """Тестируем repr и str"""
#         t = Date(1, 2, 3)
#         self.assertEqual("1.2.3", str(t))
#         self.assertEqual("Date(1, 2, 3)", repr(t))
#
#
# class TestClassTimeDelta(unittest.TestCase):
#     """Тестируем class TimeDelta"""
#
#     def test_dey_month_year(self):
#         """Тестируем создание, запрос и выдачу дней, месяцев, и годов"""
#
#         t = TimeDelta(1, 2, 3)
#         self.assertEqual(1, t.day)
#         self.assertEqual(2, t.month)
#         self.assertEqual(3, t.year)
#
#         with self.assertRaises(TypeError):
#             t.day = "5"
#         with self.assertRaises(ValueError):
#             t.day = -1
#
#         with self.assertRaises(TypeError):
#             t.month = "5"
#         with self.assertRaises(ValueError):
#             t.month = -1
#
#         with self.assertRaises(TypeError):
#             t.year = "5"
#         with self.assertRaises(TypeError):
#             t.year = 0.6
#         with self.assertRaises(ValueError):
#             t.year = -1
#
#         t.year = 12
#         t.month = 11
#         t.day = 10
#         self.assertEqual(10, t.day)
#         self.assertEqual(11, t.month)
#         self.assertEqual(12, t.year)
#
#     def test_str(self):
#         """Тестируем repr и str"""
#         t = TimeDelta(1, 2, 3)
#         self.assertEqual("1.2.3", str(t))
#
#
# if __name__ == '__main__':
#     unittest.main()
