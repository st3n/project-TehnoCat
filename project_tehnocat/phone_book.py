from collections import UserDict
import os
import pickle
from rich import print
import datetime
import re

from project_tehnocat.utils.validator import is_valid_phone
from project_tehnocat.utils.cli_parse_decorator import *
from project_tehnocat.utils.demo_data import generate_fake_contacts_data
from project_tehnocat.utils.dump_decorator import dump_contacts
from project_tehnocat.phone_book import *
from project_tehnocat.birthdays import *
from project_tehnocat.contact_record import Record
from project_tehnocat.consol import ConsolePrinter


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
        if os.path.exists(FILENAME) and os.path.getsize(FILENAME) > 0:
            with open(FILENAME, "rb") as file:
                self.data = pickle.load(file)

    def import_demo(self):
        for contact_info in generate_fake_contacts_data(10):
            self.add_contact({"name" : contact_info["name"], "phone" : contact_info["phone"]})
            self.add_birthday({"name" :contact_info["name"], "birthday": contact_info["birthday"]})
            self.add_email({"name" : contact_info["name"], "email": contact_info["email"]})
            self.add_address({"name" :contact_info["name"], "address" : contact_info["address"]})

        return "Demo data has been imported successfully"

    def get_contact(self, args, args_expected_size: int):
        if len(args) < args_expected_size:
            raise ValueError

        contact = self.find(args[0])
        if not contact:
            raise RecordDoesNotExistError

        return contact

    @dump_contacts
    def add_contact(self, args):
        if args.get("name") != None:
            name = args["name"]
        else:
            print("No name provide. Try help")

        if name in self.data:
            print ("Record alreasy exist")

        record = Record(name)
        self.add_record(record)
        phone = args.get("phone")
        email = args.get("email")
        address = args.get("address")
        if phone not in  ["", None]:
            self.add_phone(args)
        if email not in  ["", None]:
            self.add_email(args)
        if address not in  ["", None]:
            self.add_address(args)

        print(f"[bold purple]Contact[/bold purple] [bold cyan]{name}[/bold cyan] [bold purple]added[/bold purple].")

    @dump_contacts
    @input_error
    def remove_contact(self, args):
        self.delete(args['name'])
        print(f"[magenta]Contact[/magenta] [bold cyan]{args['name']}[/bold cyan] [magenta]removed[/magenta].")

    @dump_contacts
    @input_error
    def remove_phone(self, args):
        name = args["name"]
        if name not in self.data:
            raise RecordDoesNotExistError

        self.data[name].remove_phone(args["phone"])
        print(f"[bold cyan]{name}'s [/bold cyan][magenta]phone[/magenta] '{args['phone']}' [magenta]removed[/magenta].")

    @dump_contacts
    @input_error
    def remove_email(self, args):
        name = args["name"]
        if name not in self.data:
            raise RecordDoesNotExistError

        self.data[name].remove_email(args["email"])
        print(f"[bold cyan]{name}'s [/bold cyan][magenta]email[/magenta]'{args['email']}' [magenta]removed[/magenta].")

    @dump_contacts
    @input_error
    def remove_address(self, args):
        name = args["name"]
        if name not in self.data:
            raise RecordDoesNotExistError

        self.data[name].remove_address(args["address"])
        print(f"[bold cyan]{name}'s [/bold cyan][magenta]address[/magenta] '{args['address']}' [magenta]removed[/magenta].")

    @dump_contacts
    @input_error
    def change_phone(self, args):
        name = args["name"]
        if name not in self.data:
            raise RecordDoesNotExistError

        self.data[name].edit_phone(args["old_value"], args["new_value"])
        print(f"[bold cyan]{name}'s[/bold cyan] [bold purple]phone [/bold purple]'{args['old_value']}'[bold purple] changed to[/bold purple] '{args['new_value']}'.")

    @dump_contacts
    @input_error
    def change_email(self, args):
        name = args["name"]
        if name not in self.data:
            raise RecordDoesNotExistError

        self.data[name].edit_email(args["old_value"], args["new_value"])
        print(f"[bold cyan]{name}'s[/bold cyan] [bold purple]email '{args['old_value']}' changed to '{args['new_value']}'.")

    @dump_contacts
    @input_error
    def change_address(self, args):
        name = args["name"]
        if name not in self.data:
            raise RecordDoesNotExistError

        self.data[name].edit_address(args["old_value"], args["new_value"])
        print(f"[bold cyan]{name}'s[/bold cyan] [bold purple]address[/bold purple] '{args['old_value']}' [bold purple]changed to [/bold purple]'{args['new_value']}'.")

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
    def add_phone(self, args):
        name = args["name"]
        if name not in self.data:
            raise RecordDoesNotExistError

        self.data[name].add_phone(args["phone"])
        print("[bold purple]Phone added[/bold purple].")

    @input_error
    def show_phone(self, args):
        if len(args) < 1:
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
        name = args["name"]
        if name not in self.data:
            raise RecordDoesNotExistError

        self.data[name].add_birthday(args["birthday"])
        print("[bold purple]Birthday added[/bold purple].")

    @dump_contacts
    @input_error
    def add_email(self, args):
        name = args["name"]
        if name not in self.data:
            raise RecordDoesNotExistError

        self.data[name].add_email(args["email"])
        print("[bold purple]Email added[/bold purple].")

    @dump_contacts
    @input_error
    def add_address(self, args):
        name = args["name"]
        if name not in self.data:
            raise RecordDoesNotExistError

        self.data[name].add_address(args["address"])
        print(
            f"[bold cyan]{name}'s [/bold cyan][magenta]address[/magenta] '{args['address']}' [magenta]added[/magenta]."
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
        birthdays = get_birthdays_per_week(
            map(
                lambda name: {
                    "name": name,
                    "birthday": self.find(name).birthday.value,
                },
                contacts_with_birthdays,
            )
        )

        self.console.display_birthdays_next_week(birthdays)

    @input_error
    def show_birthdays_in_days(self, args):
        if len(args) != 1:
            raise ValueError

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
        values = [v.replace(" ", "") for v in values]
        if not isinstance(values, datetime):
            values = [v.lower() for v in values]
        # else:
        #     values = [values]
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
        return self.search([' '.join(args['value'])], "name")

    def search_by_birthday(self, args):
        return self.search(args['value'], "birthday")

    def search_by_emails(self, args):
        return self.search(args['value'], "emails")

    def search_by_phones(self, args):
        return self.search(args['value'], "phones")

    @dump_contacts
    @input_error
    def add_note(self, args):
        name = args["name"]
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
        value = args['value']
        return self.search(value, "notes")

    def search_by_tag(self, args):
        value = args['value']
        return self.search(value, "notes_tags")
