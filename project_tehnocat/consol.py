import rich.style
from rich.console import Console
from rich.table import Table
from rich.text import Text

from project_tehnocat.command import bot_commands


class ConsolePrinter:
    def __init__(self, contacts):
        self.contacts = contacts
        self.console = Console()

    @staticmethod
    def highlight_substrings(text, substrings, style="bold white on red"):
        """Highlights substrings within a text with the given style."""
        lowered_text = text.lower()
        highlighted_text = Text()
        i = 0
        while i < len(text):
            matched = False
            for substring in substrings:
                if lowered_text.startswith(substring, i):
                    highlighted_text.append(text[i:i + len(substring)], style=style)
                    i += len(substring)
                    matched = True
                    break
            if not matched:
                highlighted_text.append(text[i])
                i += 1
        return highlighted_text

    def display_table(self, records, highlight=None):
        table = Table(show_header=True, header_style="bold magenta", show_lines=True)
        table.add_column("Name", style="cyan", width=20)
        table.add_column("Phones", style="yellow", width=40)
        table.add_column("Address", style="blue", width=30)
        table.add_column("Email", style="magenta", width=30)
        table.add_column("Birthday", style="green", width=20)
        table.add_column("Notes", style="green", width=20)
        table.add_column("Tags", style="green", width=20)

        for name, record in records:
            phones_str = (
                ", ".join(str(p.value) for p in record.phones)
                if hasattr(record, "phones") and record.phones
                else "None"
            )
            addresses_str = (
                ", ".join(str(a.value) for a in record.address)
                if hasattr(record, "address") and record.address
                else "None"
            )
            emails_str = (
                ", ".join(str(e.value) for e in record.emails)
                if hasattr(record, "emails") and record.emails
                else "None"
            )
            birthday_str = (
                str(record.birthday)
                if hasattr(record, "birthday") and record.birthday
                else "None"
            )
            notes_str = str(record.notes) if record.notes else "None"
            tags_str = (
                str("\n".join([tag.value for tag in record.notes_tags]))
                if record.notes_tags
                else "None"
            )

            if highlight:
                [field_name] = highlight.keys()
                [search_values] = highlight.values()

                if field_name == "name":
                    name = self.highlight_substrings(name, search_values)
                elif field_name == "phones":
                    phones_str = self.highlight_substrings(phones_str, search_values)
                elif field_name == "emails":
                    emails_str = self.highlight_substrings(emails_str, search_values)
                elif field_name == "addresses":
                    addresses_str = self.highlight_substrings(addresses_str, search_values)
                elif field_name == "birthday":
                    birthday_str = self.highlight_substrings(birthday_str, search_values)
                elif field_name == "notes":
                    notes_str = self.highlight_substrings(notes_str, search_values)
                elif field_name == "notes_tags":
                    tags_str = self.highlight_substrings(tags_str, search_values)

            table.add_row(
                name,
                phones_str,
                addresses_str,
                emails_str,
                birthday_str,
                notes_str,
                tags_str,
            )

        self.console.print(table)

    def display_table_all(self):
        self.display_table(self.contacts.data.items())

    def display_help(self):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Command", style="blue", width=25)
        table.add_column("Arguments", style="cyan", width=35)
        table.add_column("Description", style="yellow", width=60)

        unique_blocks = []
        for command_data in bot_commands():
            unique_blocks.append(command_data["block"])
        unique_blocks = sorted(list(set(unique_blocks)))
        unique_blocks.remove("general")
        unique_blocks = ["general"] + unique_blocks

        for block_name in unique_blocks:
            table.add_section()
            table.add_row(
                block_name.upper(), style=rich.style.Style(color="magenta", bold=True)
            )
            for command_data in bot_commands():
                if command_data["block"] == block_name:
                    name = f"{command_data['name']}"
                    args = (
                        f"{' '.join(['<' + c + '>' for c in command_data['args']])}"
                        if len(command_data["args"]) > 0
                        else "no arguments"
                    )
                    desc = command_data["desc"]
                    table.add_row(name, args, desc)

        self.console.print(table)

    def display_address(self, address: str):
        if address:
            self.console.print(address + "\n")
        else:
            self.console.print("[bold cyan]None[/bold cyan]\n")

    def display_birthdays_next_week(self, birthdays: dict):
        table = Table(
            title="Birthdays per Day", show_header=True, header_style="bold magenta"
        )
        table.add_column("Day", style="cyan", width=15)
        table.add_column("Names", style="yellow", width=50)

        for day, names in birthdays.items():
            table.add_row(day, ", ".join(names))

        self.console.print(table)

    def display_birthdays_in_days(self, data: tuple):
        day_of_week, birthday_data, users = data

        table = Table(title="Birthdays", show_header=True, header_style="bold magenta")
        table.add_column(
            f"Birthday Celebrant on {day_of_week} {birthday_data}", style="cyan"
        )

        for user in users:
            table.add_row(user["name"])

        self.console.print(table)
