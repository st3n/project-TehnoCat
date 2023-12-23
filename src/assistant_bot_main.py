from src.phone_book import *
from src.utils.cli_parse_decorator import *
from src.command import (
    bot_commands,
    find_closest_command,
    CommandCompleter,
    command_exists,
    find_command_by_name,
)
from prompt_toolkit import PromptSession
from src.utils.console_history import HistoryConsole


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def show_help():
    print("possible commands:")

    for command_data in bot_commands():
        name = f"{command_data['name']}"
        args = f" [{', '.join(command_data['args'])}]" if command_data["args"] else ""
        print(f"'{name}{args}' - {command_data['desc']}")


def exit():
    print("Good bye!")


def main():
    print("Welcome to the assistant bot!")
    contacts = AddressBook()
    session = PromptSession(completer=CommandCompleter())

    console_history = HistoryConsole()

    while True:
        try:
            user_input = session.prompt("Enter a command: ").strip()
        except (KeyboardInterrupt, EOFError):
            exit()
            break

        console_history.add_history(user_input)
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            exit()
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "help":
            show_help()
        elif command_exists(command):
            func_name = find_command_by_name(command)["func"]
            func = globals()[func_name]
            print(func(args, contacts))
        else:
            print("Invalid command.")
            print(f"Did you mean '{find_closest_command(command)}'?\n")
            show_help()


if __name__ == "__main__":
    main()
