import jaro
from prompt_toolkit.completion import Completer, Completion


def bot_commands():
    return [
        {
            "name": "hello",
            "args": [],
            "desc": "greetings message",
            "func": "hello",
            "block": "general",
        },
        {
            "name": "add",
            "args": ["name: [email:,|phone:,|address:]..."],
            "desc": "add new contact with optional provided phone, email, address",
            "func": "add_contact",
            "block": "general",
        },
        {
            "name": "change",
            "args": ["name", "phone", "old_phone_value", "on", "new_phone_value"],
            "desc": "change the saved contact phone",
            "func": "change_phone",
            "block": "phone numbers",
        },
        {
            "name": "change",
            "args": ["name", "email", "old_email_value", "on", "new_email_value"],
            "desc": "change the saved contact email",
            "func": "change_email",
            "block": "emails",
        },
        {
            "name": "change",
            "args": [
                "name",
                "address",
                '"old_address_value"',
                "on",
                '"new_address_value"',
            ],
            "desc": "change the saved contact address",
            "func": "change_address",
            "block": "addresses",
        },
        {
            "name": "remove",
            "args": ["name"],
            "desc": "remove contact",
            "func": "remove_contact",
            "block": "general",
        },
        {
            "name": "remove",
            "args": ["name", "phone [number...]"],
            "desc": "remove contact phone",
            "func": "remove_phone",
            "block": "phone numbers",
        },
        {
            "name": "remove",
            "args": ["name", "email [address...]"],
            "desc": "remove contact email",
            "func": "remove_email",
            "block": "emails",
        },
        {
            "name": "remove",
            "args": ["name", "address [address_str...]"],
            "desc": "remove contact address",
            "func": "remove_address",
            "block": "addresses",
        },
        {
            "name": "show-contact",
            "args": ["name"],
            "desc": "show the contact info",
            "func": "show_contact",
            "block": "general",
        },
        {
            "name": "add-phone",
            "args": ["name", "phone"],
            "desc": "add phone for contact",
            "func": "add_phone",
            "block": "phone numbers",
        },
        {
            "name": "show-phone",
            "args": ["name"],
            "desc": "show the contact phones",
            "func": "show_contact",
            "block": "phone numbers",
        },
        {
            "name": "add-birthday",
            "args": ["name", "date"],
            "desc": "add birthday for name 'name' in format 'DD.MM.YYYY'",
            "func": "add_birthday",
            "block": "birthdays",
        },
        {
            "name": "add-email",
            "args": ["name", "email"],
            "desc": "add email for contact",
            "func": "add_email",
            "block": "emails",
        },
        {
            "name": "add-address",
            "args": ["name", "address"],
            "desc": "add address for contact",
            "func": "add_address",
            "block": "addresses",
        },
        {
            "name": "show-email",
            "args": ["name"],
            "desc": "show emails for name 'name'",
            "func": "show_email",
            "block": "emails",
        },
        {
            "name": "show-address",
            "args": ["name"],
            "desc": "show addresses for name 'name'",
            "func": "show_address",
            "block": "addresses",
        },
        {
            "name": "show-birthday",
            "args": ["name"],
            "desc": "show birthday for name 'name'",
            "func": "show_birthday",
            "block": "birthdays",
        },
        {
            "name": "birthdays",
            "args": [],
            "desc": "show all birthdays from the phone book on the next week",
            "func": "show_birthdays_next_week",
            "block": "birthdays",
        },
        {
            "name": "birthdays-in-days",
            "args": ["days"],
            "desc": "show all birthdays in a particular amount of days",
            "func": "show_birthdays_in_days",
            "block": "birthdays",
        },
        {
            "name": "search-by-name",
            "args": ["name"],
            "desc": "shows all contacts with this name",
            "func": "search_by_name",
            "block": "search",
        },
        {
            "name": "search-by-birthday",
            "args": ["date"],
            "desc": "shows all contacts with the specific birthday",
            "func": "search_by_birthday",
            "block": "search",
        },
        {
            "name": "search-by-emails",
            "args": ["email1", "email2"],
            "desc": "shows all contacts with the specific emails",
            "func": "search_by_emails",
            "block": "search",
        },
        {
            "name": "search-by-phones",
            "args": ["phone1", "phone2", "phoneN"],
            "desc": "shows all contacts with the specific phone numbers",
            "func": "search_by_phones",
            "block": "search",
        },
        {
            "name": "all",
            "args": [],
            "desc": "print the contacts phone book",
            "func": "show_all",
            "block": "general",
        },
        {
            "name": "close",
            "args": [],
            "desc": "quit from the program",
            "block": "general",
            "func" : "exit"
        },
        {
            "name": "exit",
            "args": [],
            "desc": "quit from the program",
            "block": "general",
            "func" : "exit"
        },
        {
            "name": "help",
            "args": [],
            "desc": "print help message",
            "func": "show_help",
            "block": "general",
        },
        {
            "name": "add-note",
            "args": ["name"],
            "desc": "add note to a contact",
            "func": "add_note",
            "block": "notes",
        },
        {
            "name": "edit-note",
            "args": ["name"],
            "desc": "edit note for a contact",
            "func": "edit_note",
            "block": "notes",
        },
        {
            "name": "search-by-note",
            "args": ["name", "note"],
            "desc": "search records by notes",
            "func": "search_by_note",
            "block": "search",
        },
        {
            "name": "search-by-tag",
            "args": ["name", "tag"],
            "desc": "search records by tag",
            "func": "search_by_tag",
            "block": "search",
        },
        {
            "name": "import-demo",
            "args": [],
            "desc": "imports demo data",
            "func": "import_demo",
            "block": "general",
        },
    ]


def command_exists(command_name):
    return any(
        command_info.get("name") == command_name for command_info in bot_commands()
    )


def find_command_by_name(command_name):
    return next(
        (
            command_info
            for command_info in bot_commands()
            if command_info.get("name") == command_name
        ),
        None,
    )


def find_closest_command(command_name):
    names = list(map(lambda bot_command: bot_command["name"], bot_commands()))
    distances = list(
        map(
            lambda name: {
                "name": name,
                "dist": jaro.jaro_winkler_metric(name, command_name),
            },
            names,
        )
    )
    return sorted(distances, key=lambda x: x["dist"])[-1]["name"]


class CommandCompleter(Completer):
    commands = list(map(lambda bot_command: bot_command["name"], bot_commands()))

    def get_completions(self, document, complete_event):
        # Get the entire text up to the cursor position
        text_before_cursor = document.text_before_cursor

        # Check if there's a space after the first word
        if " " in text_before_cursor:
            return  # Do not offer completions if there's a space after the first word

        # If we're still at the first word, continue with completion
        word = document.get_word_before_cursor()
        for cmd in self.commands:
            if cmd.startswith(word):
                yield Completion(cmd, start_position=-len(word))
