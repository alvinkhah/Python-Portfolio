from project import check_format, date_validation, zodiac, element
import pytest


def main():
    test_format()
    test_date_format()
    test_zodiac()
    test_element()


def test_format():
    assert check_format("11/01/1990") == True
    assert check_format("11/01/2050") == True
    assert check_format("1/01/1990") == True
    assert check_format("21/1/1990") == True
    assert check_format("11-01-1990") == False
    assert check_format("11/01/90") == False
    assert check_format("11011990") == False
    assert check_format("") == False
    assert check_format("cat") == False
    assert check_format("do/do/dodo") == False


def test_date_format():
    assert date_validation("11", "01", "2000", "2023") == True
    assert date_validation("11", "01", "1900", "2023") == True
    assert date_validation("1", "1", "1900", "2023") == True
    assert date_validation("1", "1", "19", "2023") == False
    assert date_validation("32", "01", "2000", "2023") == False
    assert date_validation("32", "01", "2000", "2023") == False
    assert date_validation("11", "13", "2000", "2023") == False
    assert date_validation("11", "01", "2100", "2023") == False
    assert date_validation("11", "01", "2", "2023") == False


def test_zodiac():
    assert zodiac(1900, "2023") == "Rat"
    assert zodiac(1965, "2023") == "Snake"
    assert zodiac(1990, "2023") == "Horse"
    assert zodiac(1997, "2023") == "Ox"
    assert zodiac(2015, "2023") == "Goat"
    assert zodiac(2023, "2023") == "Rabbit"


def test_element():
    assert element(1915) == "Wood"
    assert element(2000) == "Metal"
    assert element(2002) == "Water"
    assert element(1998) == "Earth"
    assert element(1986) == "Fire"


if __name__ == "__main__":
    main()
