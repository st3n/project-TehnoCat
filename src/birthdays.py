from datetime import datetime, timedelta
from collections import defaultdict


def get_birthdays_per_week(users):
    # 1. data preparation
    birthdays_per_day = defaultdict(list)

    # 2. obtaining the current date
    today = datetime.today().date()

    # 3. users sorting
    for user in users:
        # date conversion
        name = user["name"]
        birthday = user["birthday"].date()
        # 4. evaluation of dates for this year
        birthday_this_year = birthday.replace(year=today.year)

        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        delta_days = (birthday_this_year - today).days

        # evaluation for the next week
        if delta_days < 7:
            today_day_of_week = today.strftime("%A")
            birthday_day_of_week = (today + timedelta(days=delta_days)).strftime("%A")

            # corner case: skip birthdays of collegues with delta == 6 on the next Monday if today is Sunday
            # (NOTE: this is not mentioned in task description, recomandation)
            if today_day_of_week == "Sunday" and birthday_day_of_week == "Saturday":
                continue

            # if it's a weekend, postpone to Monday
            if birthday_day_of_week in ["Saturday", "Sunday"]:
                birthday_day_of_week = "Monday"
            birthdays_per_day[birthday_day_of_week].append(name)

    return birthdays_per_day


def get_birthdays_in_days(users, days_from_now=0):
    date = datetime.today().date() + timedelta(days=days_from_now)
    birthday_day_of_week = date.strftime("%A")
    birthday_str = date.strftime("%d.%m.%Y")

    birthday_users = list(
        filter(
            lambda user: (user["birthday"].date().replace(year=date.year) == date),
            users,
        )
    )
    return (birthday_day_of_week, birthday_str, birthday_users)


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
