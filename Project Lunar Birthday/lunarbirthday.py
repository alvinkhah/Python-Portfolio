import datetime
from lunarcalendar import Converter, Solar


# Request for user's input and output user's element and Chinese zodiac
def main():
    print("This program only accepts birth dates from year 1900 to current year or year 2100, whichever earlier.")
    date_of_birth = input("Please enter your Date of Birth in the format (DD/MM/YYYY)? ")   # No need for zero padding if day or month is single digit

    current_date = datetime.date.today()
    current_year = current_date.year                        # Current year is required for the validation of birth year and determining zodiac later on.

    if check_format(date_of_birth):                         # Only go ahead if input format is valid.
        day, month, year = map(int, date_of_birth.split("/"))

        if date_validation(day, month, year, current_year): # Only go ahead if birth date is valid.
            solar = Solar(year, month, day)                 # These 2 lines of code are to convert Gregorian calendar dates to Lunar calendar dates.
            lunar = Converter.Solar2Lunar(solar)
            print(f"Your lunar birth date was day {lunar.day} of month {lunar.month} in year {lunar.year}.")

            lunar_year = lunar.year                         # Get lunar birth year
            chi_zodiac = zodiac(lunar_year, current_year)   # Determine Chinese Zodiac
            chi_element = element(lunar_year)               # Determine Chinese Element
            print(f"Your Chinese element and zodiac was the {chi_element} {chi_zodiac}.\n")
    else:
        print("Please check date format, should be DD/MM/YYYY.")


# Function to check whether date format was input correctly
def check_format(date_of_birth):
    date_format = "%d/%m/%Y"    # No need for zero padding if day or month is single digit

    try:
        dateObject = datetime.datetime.strptime(date_of_birth, date_format)
        return True
    except ValueError:
        return False


# Function to check whether date is valid
def date_validation(day, month, year, current_year):

    day = int(day)                          # Did these 4 lines of code as pytest mentioned "TypeError: not all arguments converted during string formatting"
    month = int(month)
    year = int(year)
    current_year = int(current_year)

    if month in [1, 3, 5, 7, 8, 10, 12]:
        max_days = 31
    elif month in [4, 6, 9, 11]:
        max_days = 30
    elif year % 4 == 0 and year % 100 != 0 or year % 4 == 0 and year % 400 == 0:    # Conditions for month of February
        max_days = 29
    else:
        max_days = 28

    leap_year = False                       # To note whether that year was a leap year for the first output statement to user
    if year % 4 == 0 and year % 100 != 0 or year % 4 == 0 and year % 400 == 0:
        leap_year = True

    if day < 1 or max_days < day:
        print(f"\n{day} is out of valid range. Please check the day.")
        return False
    elif month < 1 or 12 < month:
        print(f"\n{month} is out of valid range. Please check the month.")
        return False
    elif year < 1900 or current_year < year:
        print(f"\n{year} is out of range. Please check the year.")
        return False
    else:
        num_date_of_birth = datetime.datetime(year, month, day)
        dob_statement = num_date_of_birth.strftime("%A, %d %B %Y")                  # No need for zero padding if day or month is single digit
        if leap_year == False:
            print(f"\nYou were born on {dob_statement}. It was not a leap year.")    # First output statement to user
        else:
            print(f"\nYou were born on {dob_statement}. It was a leap year.")        # First output statement to user
        return True


# Function to provide Chinese zodiac
def zodiac(lunar_year, current_year):

    current_year = int(current_year)

    for r in range(1900, current_year + 1, 12):     # Chinese zodiac in 12-year cycle
        if lunar_year == r:
            return f"Rat"
    for o in range(1901, current_year + 1, 12):
        if lunar_year == o:
            return f"Ox"
    for t in range(1902, current_year + 1, 12):
        if lunar_year == t:
            return f"Tiger"
    for ra in range(1903, current_year + 1, 12):
        if lunar_year == ra:
            return f"Rabbit"
    for d in range(1904, current_year + 1, 12):
        if lunar_year == d:
            return f"Dragon"
    for s in range(1905, current_year + 1, 12):
        if lunar_year == s:
            return f"Snake"
    for h in range(1906, current_year + 1, 12):
        if lunar_year == h:
            return f"Horse"
    for g in range(1907, current_year + 1, 12):
        if lunar_year == g:
            return f"Goat"
    for m in range(1908, current_year + 1, 12):
        if lunar_year == m:
            return f"Monkey"
    for ro in range(1909, current_year + 1, 12):
        if lunar_year == ro:
            return f"Rooster"
    for do in range(1910, current_year + 1, 12):
        if lunar_year == do:
            return f"Dog"
    for p in range(1911, current_year + 1, 12):
        if lunar_year == p:
            return f"Pig"


# Function to provide element (fire, water, gold, wood and earth)
def element(lunar_year):

    lunar_year = str(lunar_year)                            # Convert lunar birth year

    if lunar_year[-1] == "0" or lunar_year[-1] == "1":      # Chinese elements are repeated in 10-year cycle
        return f"Metal"
    elif lunar_year[-1] == "2" or lunar_year[-1] == "3":
        return f"Water"
    elif lunar_year[-1] == "4" or lunar_year[-1] == "5":
        return f"Wood"
    elif lunar_year[-1] == "6" or lunar_year[-1] == "7":
        return f"Fire"
    else:
        return f"Earth"


if __name__ == "__main__":
    main()
