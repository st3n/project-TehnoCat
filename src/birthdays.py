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

    return "\n".join(
        [f"{day}: {', '.join(names)}" for day, names in birthdays_per_day.items()]
    )


