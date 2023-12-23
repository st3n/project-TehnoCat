from rich.console import Console
from rich.table import Table
from src.command import bot_commands


class ConsolePrinter:
    def __init__(self, contacts):
        self.contacts = contacts
        self.console = Console()

    def display_table_all(self):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Name", style="cyan", width=20)
        table.add_column("Phones", style="yellow", width=40)
        table.add_column("Address", style="blue", width=30)
        table.add_column("Email", style="magenta", width=30)
        table.add_column("Birthday", style="green", width=20)

        for name, record in self.contacts.data.items():
            phones_str = ", ".join(str(p.value) for p in record.phones)
            address_str = (
                str(record.address[0].value)
                if hasattr(record, "address") and record.address
                else "None"
            )
            email_str = str(record.emails[0].value) if record.emails else "None"
            birthday_str = str(record.birthday) if record.birthday else "None"
            table.add_row(name, phones_str, address_str, email_str, birthday_str)

            self.console.print(table)

    def display_help(self):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Command", style="cyan", width=15)
        table.add_column("Args", style="cyan", width=15)
        table.add_column("Description", style="yellow", width=110)

        for command_data in bot_commands():
            name = f"{command_data['name']}"
            args = (
                f"[{', '.join(command_data['args'])}]"
                if len(command_data["args"]) > 0
                else ""
            )
            desc = command_data["desc"]
            table.add_row(name, args, desc)

        self.console.print(table)
