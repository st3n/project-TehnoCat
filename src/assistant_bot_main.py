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

from utils.console_history import HistoryConsole

console = Console()

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

# Я не знаю, как загнать в таблицу аргументы, возвращаю мой старый вариант
def show_help():

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Command", style="cyan", width=15)
    table.add_column("Description", style="yellow", width=110)

    commands = [
        ("hello", "Greetings message"),
        ("add", "Add new contact in the phone book. After the command, write your name and phone number"),
        ("change", "Change the saved contact phone. After the command, write your name, old phone number and new phone number"),
        ("change", "Change the saved contact email. After the command, write your name, old email and new email"),
        ("change", "Change the saved contact address. After the command, write your name, old adress and new adress"),
        ("remove", "Remove contact. After the command, write the name you want to delete"),
        ("remove", "Remove phone. After the command, write the name and contact phone number you want to delete"),
        ("remove", "Remove email. After the command, write the name and contact email you want to delete"),
        ("remove", "Remove adress. After the command, write the name and contact adress you want to delete"),
        ("phone", "Show the phone of the user with entered name. After the command, write your name"),
        ("add-birthday", "Add birthday for contact. After the command, write your name and birthday in format 'DD.MM.YYYY'"),
        ("add-email", "Add email for contact. After the command, write your name and email for contact"),
        ("add-address", "Add address for contact. After the command, write your name and address for contact"),
        ("show-birthday", "Show birthday for contact. After the command, write your name"),
        ("show-email", "Show email for contact. After the command, write your name"),
        ("show-address", "Show address for contact. After the command, write your name"),
        ("birthdays", "Show all birthdays from the phone book on the next week"),
        ("all", "Print the contacts phone book"),
        ("close or exit", "Quit from the program"),
        ("help", "Print help message")
    ]

    for command, description in commands:
        table.add_row(command, description)

    console.print(table)


def exit():
    print("[bold magenta]Goodbye![/bold magenta]\n\U0001FAE1")


def main():
    console = Console()
    contacts = AddressBook()
    session = PromptSession(completer=CommandCompleter())
    print(
        "[bold blue]Welcome to the assistant bot![/bold blue]\n\U0001F929  \U0001F929  \U0001F929\n"
    )

 #   console_history = HistoryConsole()

    while True:
        try:
            user_input = session.prompt("Enter a command: ").strip()

        except (KeyboardInterrupt, EOFError):
            exit()
            break

    #    console_history.add_history(user_input)
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            exit()
            break
        elif command == "hello":
            print("[bold blue]How can I help you?[/bold blue]\U0001F600\n")
        elif command == "help":
            show_help()
        elif command == "all":
            show_all(args, contacts, console)    
        elif command_exists(command):
            func_name = find_command_by_name(command)["func"]
            func = globals()[func_name]
            print(func(args, contacts))
        
        else:
            print("[bold yellow]Invalid command.[/bold yellow]\n\U0001F914\n")
            print(f"Did you mean '{find_closest_command(command)}'?\n")
            show_help()


if __name__ == "__main__":
    main()
