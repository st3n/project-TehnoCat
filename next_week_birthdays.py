from datetime import datetime, timedelta
from collections import defaultdict


def get_birthdays_per_week(users):
    birthdays = defaultdict(list)
    today = datetime.today().date()
    next_saturday = today + timedelta(days=-today.weekday() + 5)
    next_friday = next_saturday + timedelta(days=6)

    for user in users:
      birthday = user["birthday"].date().replace(year=today.year)
      # Since we move weekend birthdays to Monday let's start our "week" from saturday
      if next_saturday <= birthday <= next_friday:
        birthday_day_of_week = birthday.strftime("%A")
        birthday_str = birthday.strftime("%d.%m.%Y")
        if birthday.weekday() > 4: # Saturday & Sunday check
          birthdays[f"Monday ({birthday_str})"].append(user["name"])
        else:
          birthdays[f"{birthday_day_of_week} ({birthday_str})"].append(user["name"])

    for day, names in birthdays.items():
      print(f"{day}: {', '.join(names)}")


def get_birthdays_in_days(users, days_from_now = 0):
    date = datetime.today().date() + timedelta(days=days_from_now)
    birthday_day_of_week = date.strftime("%A")
    birthday_str = date.strftime("%d.%m.%Y")

    birthday_users = list(filter(lambda user: (user['birthday'].date().replace(year=date.year) == date), users))
    user_names = ', '.join(map(lambda user: user['name'], birthday_users))
    print(f"{birthday_day_of_week} ({birthday_str}): {user_names}")


# users = [
#     {"name": "Bill Gates", "birthday": datetime(1955, 10, 28)},
#     {"name": "Jill Valentine", "birthday": datetime(1974, 11, 30)},
#     {"name": "Kate Spade", "birthday": datetime(1962, 12, 23)},
#     {"name": "Yosyp Lozynskyi", "birthday": datetime(1807, 12, 27)},
#     {"name": "Kim Kardashian", "birthday": datetime(1980, 10, 21)},
#     {"name": "Ilon Mask", "birthday": datetime(1971, 6, 28)},
# ]

# get_birthdays_per_week(users)

# get_birthdays_in_days(users, 4)
