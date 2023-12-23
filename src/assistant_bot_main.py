from prompt_toolkit import PromptSession
from src.phone_book import *
from src.utils.cli_parse_decorator import *
from src.utils.console_history import HistoryConsole
from src.command import *


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    contacts = PhoneBook()
    session = PromptSession(completer=CommandCompleter())
    print(
        "[bold blue]Welcome to the assistant bot![/bold blue]\n\U0001F929  \U0001F929  \U0001F929\n"
    )

    console_history = HistoryConsole()

    while True:
        try:
            user_input = session.prompt("Enter a command: ").strip()

        except (KeyboardInterrupt, EOFError):
            contacts.exit()
            break

        console_history.add_history(user_input)
        command, *args = parse_input(user_input)

        if command_exists(command):
            command_info = find_command_by_name(command)
            func_name = command_info["func"]
            func = getattr(contacts, func_name)
            if len(command_info["args"]):
                func(args)
            else:
                func()
        else:
            print("[bold yellow]Invalid command.[/bold yellow]\n\U0001F914\n")
            print(f"Did you mean '{find_closest_command(command)}'?\n")


if __name__ == "__main__":
    main()
