# Lunar Birthday
#### Video Demo: https://youtu.be/yo4PPKr2OfY
#### Description:
Lunar Birthday is a program which provides more information about one's Gregorian birth date. Some of that information is Chinese culture related, specifically the lunar birth date, Chinese element and zodiac which a birth date belongs to.


## Requirements

This program utilises the built-in datetime and the lunarcalendar libraries only. Their documentations can be found below:
[Datetime](https://docs.python.org/3/library/datetime.html)
[LunarCalendar 0.0.9](https://pypi.org/project/LunarCalendar/)

Datetime library was used mainly for 2 purposes, to ensure that the input complies to a particular format and to get the current year.
The LunarCalendar library provided this program with the ability to convert birthday from Gregorian calendar to birthday in the lunar calendar. It can convert dates from year 1900 to 2100.


## User Guide

To use this program, the user needs to be ready with his/her birthday according to the Gregorian calendar, in the format DD/MM/YYYY, prior to the activation of the program. This birthday must fall within 1900 to the current year. This program can be used up to year 2100 only. If using VS Code, by running "python project.py" in the terminal, the program will prompt the user for said birthday. After keying it in, three statements will greet the user. First statement is in accordance to the Gregorian calendar and informs about the day of the week, the numerical day, fully spelt month name and numerical year of the birthday. It also informs whether the birth year was a leap year. The second statement provides the user with the lunar birth date that was converted from the birthday that was provided. The last statement informs the user of the Chinese element and zodiac which belongs to the lunar birth date. The following is an example of the three statements where birthday was input as "05/04/1920":

<You were born on Monday, 05 April 1920. It was a leap year.
Your lunar birth date was day 17 of month 2 in year 1920.
Your Chinese element and zodiac was the Metal Monkey.>


## How does the Code Work?

### Functions
There are five functions in this program, namely main, check_format, date_validation, zodiac and element.

### Main Function
The main function will first print out a sentence stating that the program only accepts birth dates from year 1900 to the current year or year 2100, whichever is earlier. Then it asks the user to enter a date of birth in a particular format, DD/MM/YYYY. The following is an example of the sentences which the main function prints out:

<This program only accepts birth dates from year 1900 to current year or year 2100, whichever earlier.
Please enter your Date of Birth in the format (DD/MM/YYYY)? >

The main function gets the current year from the datetime library and calls the check_format function to ensure that the input format is correct. If it is not correct, it will print out "Please check date format, should be DD/MM/YYYY." and exit the program. If it is correct, date_validation function will then be called to ensure that the date do exist in the Gregorian calendar. For example, the 29th of February only exists in leap years. Separate error messages within the date_validation function will address whether the day, month or year was input wrongly and the program will be exited. If the date format is correct and the date is valid in the Gregorian calendar, the Gregorian birth date will be converted to the the lunar birth date using the LunarCalendar library. Both zodiac and element functions will be called to contribute to the three output statements.

The main function is important in ensuring control over the format and validity of the input date of birth. If the input fails to comply with the format, the other functions should not be called. If the format is good but not the date validity, then the conversion to lunar birth date and the subsequent generate of the element and zodiac should not take place. Apart from the control flow, the main function gets us 2 important variables which are current_year and lunar_year. The current_year variable will ensure that the birth date is not a future date in the date_validation function and lunar_year holds the year component of the lunar birth date which is important for the generation of the Chinese element and zodiac.

### Check_format Function
The check_format function takes in the user's input as its only argument. The sole purpose of the check_format function is to ensure that the input complies with the recommended format which is DD/MM/YYYY. It tolerates single digits for day and month but year must be in 4 digits. In other words, there is no need to pad with zero. For example, "1/7/1968", "01/07/1968", "01/7/1968" and "1/07/1968" are all valid but "01/07/68" is regarded as a wrong format. For wrong format input, the main function will print "Please check date format, should be DD/MM/YYYY." and exit the program. The function returns True when the input is compliant and False when the input is not.

### Date_validation Function
The date_validation function takes in the day, month, year components of the input and the current_year variable as arguments. The purpose of the date_validation function is to ensure that the input date of birth is valid. In other words, the date of birth cannot be a future date and it must be a date that is found within the Gregorian calendar. For example, 29/02/2013 is invalid as 2013 was not a leap year. In order to do date validation, the day, month and year components in the string input had to be separated and converted into integers. I used the map() method in the main function to do this but somehow pytest could not detect the conversion. Hence, I individually converted them within the date_validation function too. This was a duplication which the program tolerated.

After getting the numbers for day, month and year, I laid out the maximum number of days which are within each calendar month and made sure that February had the 29th day for leap years. Leap_year variable was then assigned as False by default and only returned as True when the year was calculated to be a leap year.

```
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
```

After the lines of code above, the following were validity checks. If the day component was out of range, an error message saying "*day* is out of valid range. Please check the day." and the program is exited. Similar error messages will be sent if the month component or year component was out of range and the program will be exited.

  **if day < 1 or max_days < day:**
      **print(f"\n{day} is out of valid range. Please check the day.")**
      **return False**
  **elif month < 1 or 12 < month:**
      **print(f"\n{month} is out of valid range. Please check the month.")**
      **return False**
  **elif year < 1900 or current_year < year:**
      **print(f"\n{year} is out of range. Please check the year.")**
      **return False**

If the date was correct, then the last part of date_validation function is to provide the first statement informing about the day of the week, the numerical day, fully spelt month name and numerical year of the birthday. It also informs whether the birth year was a leap year.

  **else:**
      **num_date_of_birth = datetime.datetime(year, month, day)**
      **dob_statement = num_date_of_birth.strftime("%A, %d %B %Y")**                  # No need for zero padding if day or month is single digit
      **if leap_year == False:**
          **print(f"\nYou were born on {dob_statement}. It was not a leap year.")**    # First output statement to user
      **else:**
          **print(f"\nYou were born on {dob_statement}. It was a leap year.")**        # First output statement to user
      **return True**

An example of the first statement:

<You were born on Monday, 05 April 1920. It was a leap year.>

### Zodiac Function
The zodiac function takes in the lunar_year and current_year as its arguments. The zodiac function determines the Chinese zodiac which the lunar birth date falls in. Since we restricted the valid years to be from 1900 to current year and knowing that the zodiacs move in 12-year cycles, I used the range() method and started the zodiac cycles from year 1900 onwards. In order for this method to work, current_year variable had to be in integer form, so it was converted. The function returns the zodiac sign. For example:

  **for r in range(1900, current_year + 1, 12):**     # Chinese zodiac in 12-year cycle
      **if lunar_year == r:**
          **return f"Rat"**

### Element Function
The element function takes in the lunar_year as its only argument. The element function determines the Chinese element which the lunar birth date falls in. Since the elements move in 10-year cycles, the last digit of the lunar birth year is sufficient to determine the Chinese element that the lunar birth date falls in. I decided to use string indexing "[-1]" to achieve this, so the lunar_year was converted to a string. The function returns the element.

  **if lunar_year[-1] == "0" or lunar_year[-1] == "1":**      # Chinese elements are repeated in 10-year cycle
      **return f"Metal"**
  **elif lunar_year[-1] == "2" or lunar_year[-1] == "3":**
      **return f"Water"**
  **elif lunar_year[-1] == "4" or lunar_year[-1] == "5":**
      **return f"Wood"**
  **elif lunar_year[-1] == "6" or lunar_year[-1] == "7":**
      **return f"Fire"**
  **else:**
      **return f"Earth"**
