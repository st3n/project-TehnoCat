import re
from rich import print
from project_tehnocat.utils.cli_parse_decorator import *
from project_tehnocat.command import *


class CommandParser:
    def __init__(self):
        self.add_pattern = re.compile(
            r"add (?:name:([^,]+))?(?:, *phone:([^,]+))?(?:, *email:([^,]+))?(?:, *address:([^,]+))?"
        )
        self.change_pattern = re.compile(
            '^change (.+?) (phone|email|address) "?(.+?)"? on "?(.+?)"?$'
        )
        self.remove_pattern = re.compile("^remove (.+?)(?: (phone|email|address) (.+?))?$")
        self.add_phone_pattern = re.compile("^add-phone (.+?) ([^ \t\n\r\f\v]+)$")
        self.add_email_pattern = re.compile("^add-email (.+?) ([^ \t\n\r\f\v]+)$")
        self.add_birthday_pattern = re.compile("^add-birthday (.+?) ([^ \t\n\r\f\v]+)$")
        self.add_address_pattern = re.compile('^add-address (.+?) "(.+?)"$')
        self.add_notes_pattern = re.compile("^add-note (.+?)$")

    @input_error
    def parse_input(self, user_input: str):
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()

        if not command_exists(cmd):
            print(f"[bold yellow]Invalid command {cmd}.[/bold yellow]\n\U0001F914\n")
            print(f"Did you mean '{find_closest_command(cmd)}'?\n")
            raise InvalidArgument(user_input)

        if cmd == "add":
            return self.parse_add_cmd(user_input)
        elif cmd == "change":
            return self.parse_change_cmd(user_input)
        elif cmd == "remove":
            return self.parse_remove_cmd(user_input)
        elif cmd == "add-phone":
            return self.parse_add_phone_cmd(user_input)
        elif cmd == "add-email":
            return self.parse_add_email_cmd(user_input)
        elif cmd == "add-address":
            return self.parse_add_address_cmd(user_input)
        elif cmd == "add-birthday":
            return self.parse_add_birthday_cmd(user_input)
        elif cmd == "add-note":
            return self.parse_add_notes_cmd(user_input)
        elif "search-by" in cmd:
            return self.parse_search_by_cmd(user_input)
        else:
            cmd_info = find_command_by_name(cmd)
            if cmd_info["args"]:
                return [cmd_info["func"], args]
            else:
                return cmd_info["func"]

    @input_error
    def parse_add_cmd(self, user_input):

        add_match = self.add_pattern.match(user_input)
        if add_match:
            name = add_match.group(1).strip() if add_match.group(1) else ""
            if not name:
                err_msg = """Use 'add name: 'name', email:,|phone:,|address:'...
- phone, email, address are optional args, address value in quotes."""
                raise NoNameProvided("No name provided.\n" + err_msg)
            phone = add_match.group(2).strip() if add_match.group(2) else ""
            email = add_match.group(3).strip() if add_match.group(3) else ""
            address = add_match.group(4).strip() if add_match.group(4) else ""

            return [
                "add_contact",
                {"name": name, "phone": phone, "email": email, "address": address},
            ]

        raise InvalidArgument(user_input)

    @input_error
    def parse_change_cmd(self, user_input):
        err_msg = "Use 'change '[name]' [email|phone|address] [old_value] on [new_value]\n'"

        change_match = self.change_pattern.match(user_input)
        if change_match:
            name = change_match.group(1).strip() if change_match.group(1) else ""
            if not name:
                raise NoNameProvided("No name provided.\n" + err_msg)

            property = change_match.group(2).strip() if change_match.group(2) else ""
            if property not in ["phone", "email", "address"]:
                raise InvalidArgPropertyCmd("property should be in [phone, email, address]\n" + err_msg)
            old_value = change_match.group(3).strip() if change_match.group(3) else ""
            new_value = change_match.group(4).strip() if change_match.group(4) else ""
            if not old_value or not new_value:
                raise InvalidArgPropertyCmd("no 'old_value' or 'new_value' provided\n" + err_msg)

            if property == "phone":
                return [
                    "change_phone",
                    {
                        "name": name,
                        "old_value": old_value,
                        "new_value": new_value,
                    },
                ]
            if property == "email":
                return [
                    "change_email",
                    {
                        "name": name,
                        "old_value": old_value,
                        "new_value": new_value,
                    },
                ]
            if property == "address":
                return [
                    "change_address",
                    {
                        "name": name,
                        "old_value": old_value,
                        "new_value": new_value,
                    },
                ]

        raise InvalidArgument(user_input)

    @input_error
    def parse_remove_cmd(self, user_input):
        err_msg = "Use 'remove '{name}' [email|phone|address] [value]\n'"
        remove_match = self.remove_pattern.match(user_input)
        if remove_match:
            name = remove_match.group(1).strip() if remove_match.group(1) else ""
            if not name:
                raise NoNameProvided("No name provided.\n" + err_msg)
            property = remove_match.group(2).strip() if remove_match.group(2) else ""

            if not property:
                return ["remove_contact", {"name" : name}] # remove Foo Viktorovych Bar

            if property not in ["phone", "email", "address"]: # if property provided, it must be in
                raise InvalidArgPropertyCmd("property should be in [phone, email, address]\n" + err_msg)

            value = remove_match.group(3).strip() if remove_match.group(3) else ""
            if not value:
                raise InvalidArgPropertyCmd("couldn't parse [value] to remove\n" + err_msg)

            if property == "phone":
                return [
                    "remove_phone",
                    {
                        "name": name,
                        "phone": value,
                    },
                ]
            if property == "email":
                return [
                    "remove_email",
                    {
                        "name": name,
                        "email": value,
                    },
                ]
            if property == "address":
                return [
                    "remove_address",
                    {
                        "name": name,
                        "address": value,
                    },
                ]

        raise InvalidArgument(user_input)

    @input_error
    def parse_add_phone_cmd(self, user_input):
        add_phone_match = self.add_phone_pattern.match(user_input)
        if add_phone_match:
            name = add_phone_match.group(1).strip() if add_phone_match.group(1) else ""
            if not name:
                err_msg = "Use 'add-phone 'name' [value]\n'"
                raise NoNameProvided("No name provided.\n" + err_msg )
            phone = add_phone_match.group(2).strip() if add_phone_match.group(2) else ""
            if phone:
                return ["add_phone", {"name": name, "phone": phone}]

        raise InvalidArgument(user_input)

    @input_error
    def parse_add_email_cmd(self, user_input):
        add_email_match = self.add_email_pattern.match(user_input)
        if add_email_match:
            name = add_email_match.group(1).strip() if add_email_match.group(1) else ""
            if not name:
                err_msg = "Use 'add-email 'name' [value]\n'"
                raise NoNameProvided("No name provided.\n" + err_msg )
            email = add_email_match.group(2).strip() if add_email_match.group(2) else ""
            if email:
                return ["add_email", {"name": name, "email": email}]

        raise InvalidArgument(user_input)

    @input_error
    def parse_add_address_cmd(self, user_input):
        add_address_match = self.add_address_pattern.match(user_input)
        if add_address_match:
            name = (
                add_address_match.group(1).strip() if add_address_match.group(1) else ""
            )
            if not name:
                err_msg = "Use 'add-address 'name' 'multi word in quotes'\n'"
                raise NoNameProvided("No name provided.\n" + err_msg )
            address = (
                add_address_match.group(2).strip() if add_address_match.group(2) else ""
            )
            if address:
                return ["add_address", {"name": name, "address": address}]

        raise InvalidArgument(user_input)

    @input_error
    def parse_add_birthday_cmd(self, user_input):
        add_birthday_match = self.add_birthday_pattern.match(user_input)
        if add_birthday_match:
            name = (
                add_birthday_match.group(1).strip()
                if add_birthday_match.group(1)
                else ""
            )
            if not name:
                err_msg = "Use 'add-birthday [name] [date]' - date in format 'dd.mm.yyyy'...\n'"
                raise NoNameProvided("No name provided.\n" + err_msg )
            birthday = (
                add_birthday_match.group(2).strip()
                if add_birthday_match.group(2)
                else ""
            )
            if birthday:
                return ["add_birthday", {"name": name, "birthday": birthday}]

        raise InvalidArgument(user_input)

    @input_error
    def parse_add_notes_cmd(self, user_input):
        add_notes_match = self.add_notes_pattern.match(user_input)
        if add_notes_match:
            name = add_notes_match.group(1).strip() if add_notes_match.group(1) else ""
            if not name:
                err_msg = "Use 'add-note [name]' - vim redactor will open for note write...\n'"
                raise NoNameProvided("No name provided.\n" + err_msg )
            return ["add_note", {"name": name}]

        raise InvalidArgument(user_input)

    @input_error
    def parse_search_by_cmd(self, user_input):
        method, *value = user_input.split(' ')
        if method and value:
            method = method.replace('-', '_')
            return [method, {"value": value}]

        raise InvalidArgument(user_input)

