import re
from rich import print
from project_tehnocat.utils.cli_parse_decorator import input_error
from project_tehnocat.command import *


class CommandParser:
    def __init__(self):
        self.add_pattern = re.compile(
            r"add (?:name:([^,]+))?(?:, *phone:([^,]+))?(?:, *email:([^,]+))?(?:, *address:([^,]+))?"
        )
        self.change_pattern = re.compile(
            '^change (.+?) (phone|email|address) "?(.+?)"? on "?(.+?)"?$'
        )
        self.remove_pattern = re.compile("^remove (.+?) (phone|email|address) (.+?)$")
        self.add_phone_pattern = re.compile("^add-phone (.+?) ([^ \t\n\r\f\v]+)$")
        self.add_email_pattern = re.compile("^add-email (.+?) ([^ \t\n\r\f\v]+)$")
        self.add_birthday_pattern = re.compile("^add-birthday (.+?) ([^ \t\n\r\f\v]+)$")
        self.add_address_pattern = re.compile('^add-address (.+?) "(.+?)"$')

    @input_error
    def parse_input(self, user_input: str):
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()

        if not command_exists(cmd):
            print(f"[bold yellow]Invalid command {cmd}.[/bold yellow]\n\U0001F914\n")
            print(f"Did you mean '{find_closest_command(cmd)}'?\n")
            raise ValueError

        if cmd == "add":
            return self.parse_add_cmd(user_input)
        elif cmd == "change":
            return self.parse_change_cmd(user_input)
        elif cmd == "remove":
            if len(args) == 2:
                return ["remove_contact", args[0] + " " + args[1]]
            return self.parse_remove_cmd(user_input)
        elif cmd == "add-phone":
            return self.parse_add_phone_cmd(user_input)
        elif cmd == "add-email":
            return self.parse_add_email_cmd(user_input)
        elif cmd == "add-address":
            return self.parse_add_address_cmd(user_input)
        elif cmd == "add-birthday":
            return self.parse_add_birthday_cmd(user_input)
        else:
            cmd_info = find_command_by_name(cmd)
            if cmd_info["args"]:
                return cmd_info["func"], *args
            else:
                return cmd_info["func"]

    def parse_add_cmd(self, user_input):
        add_match = self.add_pattern.match(user_input)
        if add_match:
            name = add_match.group(1).strip() if add_match.group(1) else ""
            if not name:
                raise ValueError  # name is obligatory
            phone = add_match.group(2).strip() if add_match.group(2) else ""
            email = add_match.group(3).strip() if add_match.group(3) else ""
            address = add_match.group(4).strip() if add_match.group(4) else ""

            return [
                "add_contact",
                {"name": name, "phone": phone, "email": email, "address": address},
            ]

        raise ValueError

    def parse_change_cmd(self, user_input):
        change_match = self.change_pattern.match(user_input)
        if change_match:
            name = change_match.group(1).strip() if change_match.group(1) else ""
            if not name:
                raise ValueError  # name is obligatory
            property = change_match.group(2).strip() if change_match.group(2) else ""
            if property not in ["phone", "email", "address"]:
                raise ValueError
            old_value = change_match.group(3).strip() if change_match.group(3) else ""
            new_value = change_match.group(4).strip() if change_match.group(4) else ""
            if not old_value or not new_value:
                raise ValueError

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

        raise ValueError

    def parse_remove_cmd(self, user_input):
        remove_match = self.remove_pattern.match(user_input)
        if remove_match:
            name = remove_match.group(1).strip() if remove_match.group(1) else ""
            if not name:
                raise ValueError  # name is obligatory
            property = remove_match.group(2).strip() if remove_match.group(2) else ""
            if property not in ["phone", "email", "address"]:
                raise ValueError
            value = remove_match.group(3).strip() if remove_match.group(3) else ""
            if not value:
                raise ValueError

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

        raise ValueError

    def parse_add_phone_cmd(self, user_input):
        add_phone_match = self.add_phone_pattern.match(user_input)
        if add_phone_match:
            name = add_phone_match.group(1).strip() if add_phone_match.group(1) else ""
            if not name:
                raise ValueError  # name is obligatory
            phone = add_phone_match.group(2).strip() if add_phone_match.group(2) else ""
            if phone:
                return ["add_phone", {"name": name, "phone": phone}]

        raise ValueError

    def parse_add_email_cmd(self, user_input):
        add_email_match = self.add_email_pattern.match(user_input)
        if add_email_match:
            name = add_email_match.group(1).strip() if add_email_match.group(1) else ""
            if not name:
                raise ValueError  # name is obligatory
            email = add_email_match.group(2).strip() if add_email_match.group(2) else ""
            if email:
                return ["add_email", {"name": name, "email": email}]
        else:
            raise ValueError

    def parse_add_address_cmd(self, user_input):
        add_address_match = self.add_address_pattern.match(user_input)
        if add_address_match:
            name = (
                add_address_match.group(1).strip() if add_address_match.group(1) else ""
            )
            if not name:
                raise ValueError  # name is obligatory
            address = (
                add_address_match.group(2).strip() if add_address_match.group(2) else ""
            )
            if address:
                return ["add_address", {"name": name, "address": address}]
        else:
            raise ValueError

    def parse_add_birthday_cmd(self, user_input):
        add_birthday_match = self.add_birthday_pattern.match(user_input)
        if add_birthday_match:
            name = (
                add_birthday_match.group(1).strip()
                if add_birthday_match.group(1)
                else ""
            )
            if not name:
                raise ValueError  # name is obligatory
            birthday = (
                add_birthday_match.group(2).strip()
                if add_birthday_match.group(2)
                else ""
            )
            if birthday:
                return ["add_birthday", {"name": name, "birthday": birthday}]
        else:
            raise ValueError
