error_msg = "Invalid command format."


class BirthdayValueError(Exception):
    message = f"{error_msg} for birthday. Expected format is DD.MM.YYYY."


class RecordAlreadyExistsError(Exception):
    message = f"Record already exists. Use change_contact [name] instead"


class RecordDoesNotExistError(Exception):
    message = "Record does not exist. Use add_contact [name] instead"


class PhoneValueError(Exception):
    message = f"{error_msg} Phone number is not correct. Expected format is 10 digits."


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ValueError:
            return {
                "add_contact": f"{error_msg} Use 'add [name] [phone number]'.",
                "change_contact": f"{error_msg} Use 'change [name] [new phone number]'.",
                "show_phone": f"{error_msg} Use 'phone [name]'.",
                "show_all": f"{error_msg} Use 'all' without arguments.",
                "parse_input": f"{error_msg} Use 'help' for commands list",
                "add_birthday": f"{error_msg} Use 'add-birthday [name] [birtday]' birtday in format DD.MM.YYYY.",
                "show_birthday": f"{error_msg} Use 'show-birthday [name]'.",
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
                return "The contacts list is empty."

    return inner
