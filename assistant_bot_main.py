from phone_book import *
from rich.console import Console
from rich import print
from rich.table import Table

console = Console()

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args



def show_help():
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Command", style="cyan", width=20)
    table.add_column("Description", style="yellow", width=60)

    commands = [
        ("hello", "Greetings message"),
        ("add", "Add new contact in the phone book. After the command, write your name and phone number"),
        ("change", "Change the saved contact phone. After the command, write your name and phone number"),
        ("phone", "Show the phone of the user with entered name. After the command, write your name"),
        ("add-birthday", "Add birthday for name 'name'. After the command, write your name and birthday in format 'DD.MM.YYYY'"),
        ("show-birthday", "Show birthday for name 'name'. After the command, write your name"),
        ("birthdays", "Show all birthdays from the phone book on the next week"),
        ("all", "Print the contacts phone book"),
        ("close or exit", "Quit from the program"),
        ("help", "Print help message")
    ]

    for command, description in commands:
        table.add_row(command, description)

    console.print(table)

def main():
    contacts = AddressBook()
    print("[bold blue]Welcome to the assistant bot![/bold blue]")  
    while True:
        user_input = input("Enter a command: ").strip().lower()
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("[bold magenta]Goodbye![/bold magenta]")  
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
            show_all(args, contacts, console)
        elif command == "add-birthday":
            print(add_birthday(args, contacts))
        elif command == "show-birthday":
            print(show_birthday(args, contacts))
        elif command == "birthdays":
            print(show_birthdays_next_week(contacts))
        elif command == "help":
            show_help()
        else:
            print("[bold yellow]Invalid command.[/bold yellow]")

if __name__ == "__main__":
    main()
