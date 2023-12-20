from phone_book import *


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def show_help():
    print("possible commands:")
    print("'hello' - greetings message")
    print("'add [name] [phone]' - add new contact in the phone book")
    print("'change [name] [phone]' - change the saved contact phone")
    print("'phone [name]' - show the phone of the user with entered name")
    print(
        "'add-birthday [name] [date]' - add birthday for name 'name' in format 'DD.MM.YYYY'"
    )
    print("'show-birthday[name]' - show birthday for name 'name'")
    print("'birthdays' - show all birthdays from the phone book on the next week")
    print("'all' - print the contacnts phone book")
    print("'close' or 'exit' - quit from the program")
    print("'help' - print help message")


def main():
    contacts = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ").strip().lower()
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(args, contacts))
        elif command == "add-birthday":
            print(add_birthday(args, contacts))
        elif command == "show-birthday":
            print(show_birthday(args, contacts))
        elif command == "birthdays":
            print(show_birthdays_next_week(contacts))
        elif command == "help":
            show_help()
        else:
            print("Invalid command.")
            show_help()


if __name__ == "__main__":
    main()
