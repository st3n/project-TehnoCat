from datetime import datetime, timedelta
from collections import defaultdict
from tabulate import tabulate
from rich.console import Console
from rich.table import Table

# хочу вывести в красивую таблицу
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
        if delta_days >= 0 and delta_days < 7:
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
   
    table = Table(title="Birthdays", show_header=True, header_style="bold magenta")
    table.add_column("Day", style="cyan", width=10)
    table.add_column("Birthdays", style="yellow")

    for day, names in birthdays_per_day.items():
        table.add_row(day, ', '.join(names))

    console = Console()
    console.print(table)
   



 
   
    #table_data = []
    #for day, names in birthdays_per_day.items():
    #    table_data.append([day, ', '.join(names)])

   # return tabulate(table_data, headers=["Day", "Birthdays"])
    ##return "\n".join(
    #    [f"{day}: {', '.join(names)}" for day, names in birthdays_per_day.items()]
    

    def get_birthdays_in_days(users, days_from_now = 0):
        date = datetime.today().date() + timedelta(days=days_from_now)
        birthday_day_of_week = date.strftime("%A")
        birthday_str = date.strftime("%d.%m.%Y")

        birthday_users = list(filter(lambda user: (user['birthday'].date().replace(year=date.year) == date), users))
        user_names = ', '.join(map(lambda user: user['name'], birthday_users))
  #  return f"{birthday_day_of_week} ({birthday_str}): {user_names}"


    

def get_birthdays_in_days(users, days_from_now=0):
    date = datetime.today().date() + timedelta(days=days_from_now)
    birthday_day_of_week = date.strftime("%A")
    birthday_str = date.strftime("%d.%m.%Y")

    birthday_users = list(filter(lambda user: (user['birthday'].date().replace(year=date.year) == date), users))

    table = Table(title="Birthdays", show_header=True, header_style="bold magenta")
    table.add_column("Birthday Celebrant", style="cyan")

    for user in birthday_users:
        table.add_row(user['name'])

    console = Console()
    console.print(table)
    



  #  user_names = ', '.join(map(lambda user: user['name'], birthday_users))

   # table_data = []
   # for user in birthday_users:
    #    table_data.append([user['name']])

   # return tabulate(table_data, headers=["Birthday Celebrant"])
    #return f"{birthday_day_of_week} ({birthday_str}): {user_names}"


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

