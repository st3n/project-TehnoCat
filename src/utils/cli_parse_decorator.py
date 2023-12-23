error_msg = "[bold yellow]Invalid command format.[/bold yellow] \U0001F914"


class BirthdayValueError(Exception):
    message = "[bold yellow]Invalid command format for birthday[/bold yellow] \U0001F914.\n[bold green]Expected format is DD.MM.YYYY.[/bold green]\n"


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
                "add_contact": f"{error_msg} Use 'add [name] [phone number]'.",
                "change_contact": f"{error_msg} Use 'change [name] [old [phone,email,address]] [new [phone,email,address]]'.",
                "remove_contact": f"{error_msg} Use 'remove [name]'.",
                "show_phone": f"{error_msg} Use 'phone [name]'.",
                "show_all": f"{error_msg} Use 'all' without arguments.",
                "parse_input": f"{error_msg} Use 'help' for commands list",
                "add_birthday": f"{error_msg} Use 'add-birthday [name] [birtday]' birtday in format DD.MM.YYYY.",
                "add_email": f"{error_msg} Use 'add-eamil [name] [email]'.",
                "add_address": f"{error_msg} Use 'add-address [name] [address]'.",
                "show_email": f"{error_msg} Use 'show-email [name]'.",
                "show_address": f"{error_msg} Use 'show-address [name]'.",
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
                return "The contacts list is empty."

    return inner


