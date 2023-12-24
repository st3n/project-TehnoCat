from collections import UserDict
import os
import pickle
from rich import print
import datetime
import re

from src.utils.validator import is_valid_phone
from src.utils.cli_parse_decorator import *
from src.utils.demo_data import generate_fake_contacts_data
from src.utils.dump_decorator import dump_contacts
from src.phone_book import *
from src.birthdays import *
from src.contact_record import Record
from src.consol import ConsolePrinter


class PhoneBook(UserDict):
    def __init__(self, load_from_file=True):
        """
        Initialize an AddressBook instance.

        This constructor initializes an empty dictionary in the `data` attribute and
        loads data from a file into it if the file exists.
        """
        super().__init__()
        self.data = {}

        if load_from_file:
            self.load()

        self.console = ConsolePrinter(self)

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise RecordDoesNotExistError

    def dump(self):
        """
        Serialize and save the data dictionary to a binary file using the Pickle format.
        The data is saved to the file "address_book.bin" in binary mode.
        :return: None
        """
        with open("./data/address_book.bin", "wb") as file:
            pickle.dump(self.data, file)

    def load(self):
        """
        Deserialize and load data from a binary file using the Pickle format.
        If the file "address_book.bin" exists, it loads the data from it into the AddressBook instance.
        :return:
        """
        FILENAME = "./data/address_book.bin"
        if os.path.exists(FILENAME):
            with open(FILENAME, "rb") as file:
                self.data = pickle.load(file)

    def import_demo(self):
        for contact_info in generate_fake_contacts_data(10):
            self.add_contact([contact_info["name"], contact_info["phone"]])
            self.add_birthday([contact_info["name"], contact_info["birthday"]])
            self.add_email([contact_info["name"], contact_info["email"]])
            self.add_address([contact_info["name"], contact_info["address"]])

        return "Demo data has been imported successfully"

    @dump_contacts
    @input_error
    def add_contact(self, args):
        name, phone = args

        if name in self.data:
            self.data[name].add_phone(phone)
        else:
            record = Record(name)
            record.add_phone(phone)
            self.add_record(record)

        return f"[bold purple]Phone number[/bold purple] {phone} [bold purple]for contact[/bold purple] [bold cyan]{name}[/bold cyan] [bold purple]added[/bold purple].\n"

    @dump_contacts
    @input_error
    def remove_contact(self, args):
        if len(args) < 1:
            raise ValueError

        name = args[0]

        if len(args) == 1:
            self.delete(name)
            print(
                f"[magenta]Contact[/magenta] [bold cyan]{name}[/bold cyan] [magenta]removed[/magenta].\n"
            )
            return

        if len(args) == 2:
            if "@" in args[1]:
                self.data[name].remove_email(args[1])
                print(
                    f"[bold cyan]{name}'s [/bold cyan][magenta]email[/magenta]'{args[1]}' [magenta]removed[/magenta].\n"
                )
            elif args[1].isdigit():
                self.data[name].remove_phone(args[1])
                print(
                    f"[bold cyan]{name}'s [/bold cyan][magenta]phone[/magenta] '{args[1]}' [magenta]removed[/magenta].\n"
                )
        else:
            full_address = " ".join(args[1:])
            self.data[name].remove_address(full_address)
            print(
                f"[bold cyan]{name}'s [/bold cyan][magenta]address[/magenta] '{full_address}' [magenta]removed[/magenta].\n"
            )

    @dump_contacts
    @input_error
    def change_contact(self, args):
        name = args[0]

        if name not in self.data:
            raise RecordDoesNotExistError(name)

        if len(args) == 3:
            if "@" in args[1] and "@" in args[2]:
                self.data[name].edit_email(args[1], args[2])
                print(
                    f"[bold cyan]{name}'s[/bold cyan] [bold purple]email '{args[1]}' changed to '{args[2]}'.\n"
                )
                return
            elif args[1].isdigit() and args[2].isdigit():
                self.data[name].edit_phone(args[1], args[2])
                print(
                    f"[bold cyan]{name}'s[/bold cyan] [bold purple]phone [/bold purple]'{args[1]}'[bold purple] changed to[/bold purple] '{args[2]}'.\n"
                )
                return

        addresses = [
            x.strip() for x in " ".join(args[1:]).split(sep="|") if x != "" and x != " "
        ]
        if len(addresses) != 2:
            raise ValueError

        self.data[name].edit_address(addresses[0], addresses[1])
        res = f"[bold cyan]{name}'s[/bold cyan] [bold purple]address[/bold purple] '{addresses[0]}' [bold purple]changed to [/bold purple]'{addresses[1]}'.\n"
        print(res)
        return res

    @input_error
    def show_contact(self, args):
        if len(args) < 1:
            raise ValueError

        name = args[0]
        contact = self.find(name)
        if not contact:
            raise RecordDoesNotExistError

        print(str(contact))

    @input_error
    def show_phone(self, args):
        if len(args) == 0:
            raise ValueError
        name = args[0]
        contact = self.find(name)
        if not contact:
            raise RecordDoesNotExistError

        print(
            ", ".join(str(p.value) for p in contact.phones)
            if contact.phones
            else "None"
        )

    @input_error
    def show_all(self):
        if not self.data:
            raise KeyError

        self.console.display_table_all()

    def show_help(self):
        self.console.display_help()

    @dump_contacts
    @input_error
    def add_birthday(self, args):
        name, date = args
        contact = self.find(name)
        if not contact:
            raise RecordDoesNotExistError

        contact.add_birthday(date)
        print("[bold purple]Birthday added[/bold purple].\n")

    @dump_contacts
    @input_error
    def add_email(self, args):
        name, *emails = args
        contact = self.find(name)
        if not contact:
            raise RecordDoesNotExistError

        for email in emails:
            contact.add_email(email)
        print("[bold purple]Emails added[/bold purple].\n")

    @dump_contacts
    @input_error
    def add_address(self, args):
        name = args[0]
        contact = self.find(name)
        if not contact:
            raise RecordDoesNotExistError

        address = " ".join(args[1:])
        contact.add_address(address)
        print(
            f"[bold cyan]{name}'s [/bold cyan][magenta]address[/magenta] '{address}' [magenta]added[/magenta].\n"
        )

    @input_error
    def show_birthday(self, args):
        if len(args) == 0:
            raise ValueError

        name = args[0]
        contact = self.find(name)
        if not contact:
            raise RecordDoesNotExistError

        print(str(contact.birthday) if contact.birthday else "None")

    @input_error
    def show_email(self, args):
        if len(args) == 0:
            raise ValueError
        name = args[0]
        contact = self.find(name)
        if not contact:
            raise RecordDoesNotExistError

        print(
            ", ".join(str(p.value) for p in contact.emails)
            if contact.emails
            else "None"
        )

    @input_error
    def show_address(self, args):
        if len(args) == 0:
            raise ValueError
        name = args[0]
        contact = self.find(name)
        if not contact:
            raise RecordDoesNotExistError

        address_str = "\n".join(
            f"[bold cyan]{address.value}[/bold cyan]" for address in contact.address
        )
        self.console.display_address(address_str)

    def hello(self):
        print("[bold blue]How can I help you?[/bold blue]\U0001F600\n")

    def exit(self):
        print("[bold magenta]Goodbye![/bold magenta]\n\U0001FAE1")
        raise SystemExit(0)

    @input_error
    def show_birthdays_next_week(self):
        contacts_with_birthdays = list(
            filter(lambda name: self.find(name).birthday is not None, self.data)
        )
        birthdays_per_week = birthdays_per_week(
            map(
                lambda name: {
                    "name": name,
                    "birthday": self.find(name).birthday.value,
                },
                contacts_with_birthdays,
            )
        )

        self.console.display_birthdays_next_week(birthdays_per_week)

    @input_error
    def show_birthdays_in_days(self, args):
        days_from_now = args[0]
        contacts_with_birthdays = list(
            filter(lambda name: self.find(name).birthday is not None, self.data)
        )
        data = get_birthdays_in_days(
            map(
                lambda name: {
                    "name": name,
                    "birthday": self.find(name).birthday.value,
                },
                contacts_with_birthdays,
            ),
            int(days_from_now),
        )
        self.console.display_birthdays_in_days(data)

    def search(self, values, field_name):
        if not isinstance(values, datetime):
            values = [v.lower() for v in values]
        else:
            values = [values]
        match_scores, matched_substrings = {}, {}

        for v in values:
            for record, substring in self.search_by_partial(field_name, v):
                self.update_match_info(match_scores, matched_substrings, record, substring)

        sorted_matches = sorted(match_scores, key=match_scores.get, reverse=True)
        res = [(rec.name.value, rec) for rec in sorted_matches]

        print(f"{len(sorted_matches)} records found:")
        highlight_substrings = {field_name: [matched_substrings[rec] for rec in sorted_matches]}
        self.console.display_table(res, highlight=highlight_substrings)

    def update_match_info(self, match_scores, matched_substrings, record, substring):
        match_score = len(substring)
        if match_score > match_scores.get(record, 0):
            match_scores[record] = match_score
            matched_substrings[record] = substring

    def search_by_partial(self, field_name, value, min_substring_length=3):
        partial_matches = {}

        for record in self.data.values():
            substring = self.find_longest_match(record, field_name, value, min_substring_length)
            if substring:
                partial_matches[record] = substring

        return partial_matches.items()

    def find_longest_match(self, record, field_name, value, min_substring_length):
        if len(value) < min_substring_length:
            # If the value is shorter than the minimum substring length, check the value directly
            if record.field_has_value(field_name, value):
                return value
            else:
                return None

        # For longer values, generate and check all substrings
        longest_match = None
        for i in range(len(value)):
            for j in range(len(value), i + min_substring_length - 1, -1):
                substring = value[i:j]
                if record.field_has_value(field_name, substring) and (
                        longest_match is None or len(substring) > len(longest_match)):
                    longest_match = substring

        return longest_match

    def search_by_name(self, args):
        values = args
        return self.search(values, "name")

    def search_by_birthday(self, args):
        values = args
        return self.search(values, "birthday")

    def search_by_emails(self, args):
        values = args
        return self.search(values, "emails")

    def search_by_phones(self, args):
        values = args
        return self.search(values, "phones")

    @dump_contacts
    @input_error
    def add_note(self, args):
        [name] = args
        contact = self.find(name)
        if not contact:
            record = Record(name)
            self.add_record(record)

        contact = self.find(name)
        contact.add_note()
        return "Notes added."

    @dump_contacts
    @input_error
    def edit_note(self, args):
        [name] = args
        contact = self.find(name)
        if not contact:
            raise RecordDoesNotExistError

        contact.edit_note()
        return "Notes edited."

    def search_by_note(self, args):
        values = args
        return self.search(values, "notes")

    def search_by_tag(self, args):
        values = args
        return self.search(values, "notes_tags")
