import readline
from src.phone_book import *
from src.utils.cli_parse_decorator import *
from src.command import bot_commands, find_closest_command, CommandCompleter, command_exists, find_command_by_name
from prompt_toolkit import PromptSession

@input_error
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


def exit(history_file):
    readline.write_history_file(history_file)
    print("Good bye!")


def main():
    command_history = "../.command_history"
    contacts = AddressBook()
    session = PromptSession(completer=CommandCompleter())
    print("Welcome to the assistant bot!")

    try:
        readline.read_history_file(command_history)
    except FileNotFoundError:
        pass

    while True:
        try:
            user_input = session.prompt('Enter a command: ').strip()
        except KeyboardInterrupt:
            exit(command_history)
            break

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            exit(command_history)
            break
        elif command == "hello":
            print("How can I help you?")
        elif command_exists(command):
            func_name = find_command_by_name(command)['func']
            func = globals()[func_name]
            print(func(args, contacts))
        elif command == "help":
            show_help()
        else:
            print("Invalid command.")
            print(f"Did you mean '{find_closest_command(command)}'?\n")
            show_help()


if __name__ == "__main__":
    main()
