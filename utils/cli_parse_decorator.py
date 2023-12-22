error_msg = "[bold yellow]Invalid command format.[/bold yellow] \U0001F914"


class BirthdayValueError(Exception):
    message = f"{error_msg} [bold yellow] [bold yellow]for birthday[/bold yellow].\n[bold green]Expected format is DD.MM.YYYY.[/bold green]\n"


class RecordAlreadyExistsError(Exception):
    message = "[bold yellow]Record already exists[/bold yellow] \U0001F917.\n [bold green]Use change_contact [name] instead[/bold green]\n"


class RecordDoesNotExistError(Exception):
    message = "[bold yellow]Record does not exist[/bold yellow] \U0001F917.\n[bold green]Use add_contact [name] instead[/bold green]\n"


class PhoneValueError(Exception):
    message = f"{error_msg}\n[bold green]Phone number is not correct. Expected format is 10 digits.[/bold green]\n"


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ValueError:
            return {
                "add_contact": f"{error_msg}\n[bold green]Use 'add [name] [phone number]'.[/bold green]\n",
                "change_contact": f"{error_msg}\n[bold green]Use 'change [name] [new phone number]'.[/bold green]\n",
                "show_phone": f"{error_msg}\n[bold green] Use 'phone [name]'.[/bold green]\n",
             #   "show_all": f"{error_msg} Use 'all' without arguments.",
                "parse_input": f"{error_msg}\n[bold green]Use 'help' for commands list[/bold green]\n",
                "add_birthday": f"{error_msg}\n[bold green]Use 'add-birthday [name] [birtday]' birtday in format DD.MM.YYYY.[/bold green]\n",
                "show_birthday": f"{error_msg}\n[bold green]Use 'show-birthday [name]'.[/bold green]\n",
            }[func.__name__]
        except (
            RecordAlreadyExistsError,
            RecordDoesNotExistError,
            PhoneValueError,
            BirthdayValueError,
        ) as e:
            return e.message
        except KeyError:
            if func.__name__ == "show_all":
                return "[/bold yellow]The contacts list is empty.[/bold yellow]\n"

    return inner
