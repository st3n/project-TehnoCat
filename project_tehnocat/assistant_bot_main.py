from prompt_toolkit import PromptSession
from project_tehnocat.phone_book import *
from project_tehnocat.utils.cli_parse_decorator import *
from project_tehnocat.utils.console_history import HistoryConsole
from project_tehnocat.command import *
from project_tehnocat.command_parser import CommandParser


def main():
    contacts = PhoneBook()
    cmd_parser = CommandParser()
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
        args = cmd_parser.parse_input(user_input)
        try:
            if type(args) is list:
                func_name, args = args
                func = getattr(contacts, func_name)
                func(args)
            elif type(args) is str:
                func = getattr(contacts, args)
                func()
        except AttributeError as e:
            print(str(e))


if __name__ == "__main__":
    main()
