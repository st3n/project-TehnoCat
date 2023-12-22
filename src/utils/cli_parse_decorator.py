error_msg = "Invalid command format."


class BirthdayValueError(Exception):
    message = f"{error_msg} for birthday. Expected format is DD.MM.YYYY."


class RecordAlreadyExistsError(Exception):
    message = f"Record already exists. Use change_contact [name] instead"


class RecordDoesNotExistError(Exception):
    message = "Record does not exist. Use add_contact [name] instead"


class PhoneValueError(Exception):
    message = "Phone number is not correct. Expected format is 10 digits."


class PhoneValueNotExist(Exception):
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.message = f"Contact {name} does not have saved phone number: {phone}"


class EmailValueNotExist(Exception):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.message = f"Contact {name} does not have saved email: {email}"


class AddressValueNotExist(Exception):
    def __init__(self, name, address):
        self.name = name
        self.phone = address
        self.message = f"Contact {name} does not have saved address: {address}"


class EmailValueError(Exception):
    def __init__(self, email):
        self.email = email
        self.message = f"Email {email} is not valid."


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
