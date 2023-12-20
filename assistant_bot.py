from phone_book import *
from command import bot_commands, find_closest_command
import pickle
import os


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def show_help():
    print("possible commands:")
    for command_data in bot_commands():
        name = f"{command_data['name']}"
        args = f" [{', '.join(command_data['args'])}]" if command_data['args'] else ''
        print(f"'{name}{args}' - {command_data['desc']}")


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
        elif command == "birthdays-in-days":
            print(show_birthdays_in_days(args, contacts))
        elif command == "help":
            show_help()
        else:
            print("Invalid command.")
            print(f"Did you mean '{find_closest_command(command)}'?\n")
            show_help()


if __name__ == "__main__":
    main()
