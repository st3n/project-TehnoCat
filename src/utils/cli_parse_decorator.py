error_msg = "[bold yellow]Invalid command format.[/bold yellow] \U0001F914"


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
        except ValueError:
            return {
                "add_contact": f"{error_msg}\n[bold green]Use 'add'. After the command, write your name and phone number.[/bold green]\n",
                "change_contact": f"{error_msg}\n[bold green]Use 'change'. After the command, write your name and the information you want to change [/bold green].\n",
                "remove_contact": f"{error_msg}\n[bold green]Use 'remove'. After the command, write the name you want to delete and the information you want to delet[/bold green]'.\n",
                "show_phone": f"{error_msg}\n[bold green]Use 'phone' After the command, write your name[/bold green].\n",
                "show_all": f"{error_msg}\n[bold green]Use only 'all' without arguments.[/bold green]\n",
                "parse_input": f"{error_msg}\n[bold green]Use only 'help' for commands list[/bold green]\n",
                "add_birthday": f"{error_msg}\n[bold green]Use 'add-birthday' After the command, write your name and birthday in format 'DD.MM.YYYY'.[/bold green]\n",
                "add_email": f"{error_msg} \n[bold green]Use 'add-email'. After the command, write your name and email for contact.[/bold green]\n",
                "add_address": f"{error_msg}\n[bold green] Use 'add-address'. After the command, write your name and address for contact.[/bold green]\n",
                "show_email": f"{error_msg} \n[bold green]Use 'show-email. After the command, write your name.[/bold green]\n",
                "show_address": f"{error_msg}\n[bold green] Use 'show-address. After the command, write your name.[/bold green]\n",
                "show_birthday": f"{error_msg}\n[bold green]Use 'show-birthday After the command, write your name.[/bold green]\n",

            }[func.__name__]
        except (
            EmailValueError,
            EmailValueNotExist,
            AddressValueNotExist,
            RecordAlreadyExistsError,
            RecordDoesNotExistError,
            PhoneValueError,
            PhoneValueNotExist,
            BirthdayValueError,
        ) as e:
            return e.message
        except KeyError:
            if func.__name__ == "show_all":
                return "[/bold yellow]The contacts list is empty.[/bold yellow]\n"

    return inner
