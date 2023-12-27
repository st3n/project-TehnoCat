from rich import print

error_msg = "[bold yellow]Invalid command format.[/bold yellow] \U0001F914"

class NoNameProvided(Exception):
    def __init__(self, msg):
        self.message = msg


class InvalidArgPropertyCmd(Exception):
    def __init__(self, msg):
        self.message = msg


class InvalidArgument(Exception):
    def __init__(self, cmd):
        self.message = f"cmd: {cmd}\n{error_msg} Try help."


class BirthdayValueError(Exception):
    message = "\U0001F914[bold green]Data format is not correct for birthday. Expected format is DD.MM.YYYY.[/bold green]\n"


class RecordAlreadyExistsError(Exception):
    message = "[bold yellow]Record already exists[/bold yellow] \U0001F917.\n [bold green]Use change_contact [name] instead[/bold green]\n"


class RecordDoesNotExistError(Exception):
    message = "[bold yellow]Record does not exist[/bold yellow] \U0001F917.\n[bold green]Use add_contact [name] instead[/bold green]\n"


class PhoneValueError(Exception):
    message = f"{error_msg}\n[bold green]Phone number is not correct. Expected format is 10 digits.[/bold green]\n"


class PhoneValueNotExist(Exception):
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.message = f"[bold yellow]Contact [/bold yellow]{name} [bold yellow]does not have saved phone number:[/bold yellow] \U0001F917.\n {phone}"


class EmailValueNotExist(Exception):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.message = f"[bold yellow]Contact[/bold yellow] {name} [bold yellow]does not have saved email:[/bold yellow] {email}"


class AddressValueNotExist(Exception):
    def __init__(self, name, address):
        self.name = name
        self.phone = address
        self.message = f"[bold yellow]Contact[/bold yellow] {name} [bold yellow]does not have saved address:[/bold yellow] {address}"


class EmailValueError(Exception):
    def __init__(self, email):
        self.email = email
        self.message = f"[bold yellow]Email[/bold yellow] {email} [bold yellow]is not valid[/bold yellow]."


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, KeyError):
            print(
                {
                    "add_contact": f"{error_msg}\n[bold green]Use 'add'. After the command, write your name and phone number.[/bold green]\n",
                    "change_phone": f"{error_msg}\n[bold green]Use 'change'. After the command, write your name and the information you want to change [/bold green].\n",
                    "change_email": f"{error_msg}\n[bold green]Use 'change'. After the command, write your name and the information you want to change [/bold green].\n",
                    "change_address": f"{error_msg}\n[bold green]Use 'change'. After the command, write your name and the information you want to change [/bold green].\n",
                    "remove_contact": f"{error_msg}\n[bold green]Use 'remove'. After the command, write the name you want to delete and the information you want to delet[/bold green]'.\n",
                    "remove_phone": f"{error_msg}\n[bold green]Use 'remove'. After the command, write the name you want to delete[/bold green]'.\n",
                    "remove_email": f"{error_msg}\n[bold green]Use 'remove'. After the command, write the name you want to delete and the information you want to delet[/bold green]'.\n",
                    "remove_address": f"{error_msg}\n[bold green]Use 'remove'. After the command, write the name you want to delete and the information you want to delet[/bold green]'.\n",
                    "show_phone": f"{error_msg}\n[bold green]Use 'phone' After the command, write your name[/bold green].\n",
                    "show_all": f"{error_msg}\n[bold green]Use only 'all' without arguments.[/bold green]\n",
                    "parse_input": f"{error_msg}\n[bold green]Use 'help' for commands list[/bold green]\n",
                    "add_birthday": f"{error_msg}\n[bold green]Use 'add-birthday' After the command, write your name and birthday in format 'DD.MM.YYYY'.[/bold green]\n",
                    "add_email": f"{error_msg} \n[bold green]Use 'add-email'. After the command, write your name and email for contact.[/bold green]\n",
                    "add_address": f"{error_msg}\n[bold green] Use 'add-address'. After the command, write your name and address for contact.[/bold green]\n",
                    "show_email": f"{error_msg} \n[bold green]Use 'show-email. After the command, write your name.[/bold green]\n",
                    "show_address": f"{error_msg}\n[bold green] Use 'show-address. After the command, write your name.[/bold green]\n",
                    "show_birthday": f"{error_msg}\n[bold green]Use 'show-birthday After the command, write your name.[/bold green]\n",
                    "add_note": f"{error_msg}\n[bold green]Use 'add-note [name]'.[/bold green]\n",
                    "edit_note": f"{error_msg}\n[bold green]Use 'edit-note [name]'.[/bold green]\n",
                    "search_by_note": f"{error_msg}\n[bold green]Use 'search_by_note [search string]' and note editor will open[/bold green]\n",
                    "search_by_tag": f"{error_msg}\n[bold green]Use 'search_by_tag [search string]' and note editor will open.[/bold green]\n",
                    "show_all": "[bold yellow]The contacts list is empty.[/bold yellow]\n",
                    "show_birthdays_in_days": "[bold yellow]No argument provided. Try help[/bold yellow]\n",
                }[func.__name__]
            )
            return
        except (
            EmailValueError,
            EmailValueNotExist,
            AddressValueNotExist,
            RecordAlreadyExistsError,
            RecordDoesNotExistError,
            PhoneValueError,
            PhoneValueNotExist,
            BirthdayValueError,
            NoNameProvided,
            InvalidArgument,
            InvalidArgPropertyCmd
        ) as e:
            print(e.message)
            return

    return inner
