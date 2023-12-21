from src.phone_book import *


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def show_help():
    print("possible commands:")
    print("'hello' - greetings message")
    print("'add [name] [phone]' - add new contact in the phone book")
    print("'change [name] [phone]' - change the saved contact phone")
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
}


def main():
    contacts = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ").strip()
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
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
