import readline
from src.phone_book import *
from src.utils.cli_parse_decorator import *


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def show_help():
    print("possible commands:")
    print("'hello' - greetings message")
    print("'add [name] [phone]' - add new contact in the phone book")
    print("'change [name] [old_phone] [new_phone]' - change the saved contact phone")
    print("'change [name] [old_email] [new_email]' - change the saved contact email")
    print(
        "'change [name] [old_address] | [new_address]' - change the saved contact address"
    )
    print("remove [name]' - remove contact")
    print("remove [name] [phone]' - remove contact phone")
    print("remove [name] [email]' - remove contact email")
    print("remove [name] [address]' - remove contact address")
    print("'phone [name]' - show the phone of the user with entered name")
    print(
        "'add-birthday [name] [date]' - add birthday for contact in format 'DD.MM.YYYY'"
    )
    print("add-email [name] [email] - add email for contact")
    print("add-address [name] [address] - add address for contact")
    print("show-email [name]")
    print("show-address [name]")
    print("show-birthday [name]")
    print("'birthdays' - show all birthdays from the phone book on the next week")
    print("'all' - print the contacnts phone book")
    print("'close' or 'exit' - quit from the program")
    print("'help' - print help message")


command_dict = {
    "add": add_contact,
    "change": change_contact,
    "remove": remove_contact,
    "phone": show_phone,
    "all": show_all,
    "add-birthday": add_birthday,
    "add-email": add_email,
    "add-address": add_address,
    "show-email": show_email,
    "show-address": show_address,
    "show-birthday": show_birthday,
    "birthdays": show_birthdays_next_week,
    "birthdays-in-days": show_birthdays_in_days
}


def exit(history_file):
    readline.write_history_file(history_file)
    print("Good bye!")


def main():
    command_history = "../.command_history"
    contacts = AddressBook()
    print("Welcome to the assistant bot!")

    try:
        readline.read_history_file(command_history)
    except FileNotFoundError:
        pass

    while True:
        try:
            user_input = input("Enter a command: ").strip()
        except KeyboardInterrupt:
            exit(command_history)
            break

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            exit(command_history)
            break
        elif command == "hello":
            print("How can I help you?")
        elif command in command_dict:
            print(command_dict[command](args, contacts))
        elif command == "help":
            show_help()
        else:
            print("Invalid command.")
            show_help()


if __name__ == "__main__":
    main()
