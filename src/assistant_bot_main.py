import sys

if sys.platform in ["macOSX", "darwin"]:
    import gnureadline as readline
else:
    import readline


from prompt_toolkit import PromptSession
from rich.console import Console
from rich.table import Table

from phone_book import *
from utils.cli_parse_decorator import *
from command import (
    bot_commands,
    find_closest_command,
    CommandCompleter,
    command_exists,
    find_command_by_name,
)


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def show_help(_, __):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Command", style="cyan", width=15)
    table.add_column("Args", style="cyan", width=15)
    table.add_column("Description", style="yellow", width=110)

    for command_data in bot_commands():
        name = f"{command_data['name']}"
        args = (
            f" [{', '.join(command_data['args'])}]"
            if len(command_data["args"]) > 0
            else ""
        )
        desc = command_data["desc"]
        table.add_row(name, args, desc)

    return table


def exit(history_file):
    readline.write_history_file(history_file)
    print("[bold magenta]Goodbye![/bold magenta]\n\U0001FAE1")


def main():
    command_history = "../.command_history"
    console = Console()
    contacts = AddressBook()
    session = PromptSession(completer=CommandCompleter())
    print(
        "[bold blue]Welcome to the assistant bot![/bold blue]\n\U0001F929  \U0001F929  \U0001F929\n"
    )

    try:
        readline.read_history_file(command_history)
    except FileNotFoundError:
        pass

    while True:
        try:
            user_input = session.prompt("Enter a command: ").strip()
        except KeyboardInterrupt:
            exit(command_history)
            break

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            exit(command_history)
            break
        elif command == "hello":
            print("[bold blue]How can I help you?[/bold blue]\U0001F600\n")
        elif command_exists(command):
            func_name = find_command_by_name(command)["func"]
            func = globals()[func_name]
            print(func(args, contacts))
        elif command == "all":
            show_all(args, contacts, console)
        else:
            print("[bold yellow]Invalid command.[/bold yellow]\n\U0001F914\n")
            print(f"Did you mean '{find_closest_command(command)}'?\n")
            show_help()


if __name__ == "__main__":
    main()
