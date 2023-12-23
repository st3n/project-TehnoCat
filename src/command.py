import jaro
from prompt_toolkit.completion import Completer, Completion


def bot_commands():
    return [
        {"name": "hello", "args": [], "desc": "greetings message", "func": "hello"},
        {
            "name": "add",
            "args": ["name", "phone"],
            "desc": "add new contact in the phone book",
            "func": "add_contact",
        },
        {
            "name": "change",
            "args": ["name", "old_phone", "new_phone"],
            "desc": "change the saved contact phone",
            "func": "change_contact",
        },
        {
            "name": "change",
            "args": ["name", "old_email", "new_email"],
            "desc": "change the saved contact email",
            "func": "change_contact",
        },
        {
            "name": "change",
            "args": ["name", "old_address", "new_address"],
            "desc": "change the saved contact address",
            "func": "change_contact",
        },
        {
            "name": "remove",
            "args": ["name"],
            "desc": "remove contact",
            "func": "remove_contact",
        },
        {
            "name": "remove",
            "args": ["name", "phone"],
            "desc": "remove contact phone",
            "func": "remove_contact",
        },
        {
            "name": "remove",
            "args": ["name", "email"],
            "desc": "remove contact email",
            "func": "remove_contact",
        },
        {
            "name": "remove",
            "args": ["name", "address"],
            "desc": "remove contact address",
            "func": "remove_contact",
        },
        {
            "name": "phone",
            "args": ["name"],
            "desc": "show the phone of the user with entered name",
            "func": "show_phone",
        },
        {
            "name": "add-birthday",
            "args": ["name", "date"],
            "desc": "add birthday for name 'name' in format 'DD.MM.YYYY'",
            "func": "add_birthday",
        },
        {
            "name": "add-email",
            "args": ["name", "email"],
            "desc": "add email for contact",
            "func": "add_email",
        },
        {
            "name": "add-address",
            "args": ["name", "address"],
            "desc": "add address for contact",
            "func": "add_address",
        },
        {
            "name": "show-email",
            "args": ["name"],
            "desc": "show email for name 'name'",
            "func": "show_email",
        },
        {
            "name": "show-address",
            "args": ["name"],
            "desc": "show email for name 'name'",
            "func": "show_address",
        },
        {
            "name": "show-birthday",
            "args": ["name"],
            "desc": "show birthday for name 'name'",
            "func": "show_birthday",
        },
        {
            "name": "birthdays-next-week",
            "args": [],
            "desc": "show all birthdays from the phone book on the next week",
            "func": "show_birthdays_next_week",
        },
        {
            "name": "birthdays-in-days",
            "args": ["days"],
            "desc": "show all birthdays in a particular amount of days",
            "func": "show_birthdays_in_days",
        },
        {
            "name": "search-by-name",
            "args": ["name"],
            "desc": "shows all contacts with this name",
            "func": "search_by_name",
        },
        {
            "name": "search-by-birthday",
            "args": ["date"],
            "desc": "shows all contacts with the specific birthday",
            "func": "search_by_birthday",
        },
        {
            "name": "search-by-emails",
            "args": ["email1", "email2"],
            "desc": "shows all contacts with the specific emails",
            "func": "search_by_emails",
        },
        {
            "name": "search-by-phones",
            "args": ["phone1", "phone2", "phoneN"],
            "desc": "shows all contacts with the specific phone numbers",
            "func": "search_by_phones",
        },
        {
            "name": "all",
            "args": [],
            "desc": "print the contacts phone book",
            "func": "show_all",
        },
        {"name": "close", "args": [], "desc": "quit from the program", "func": "exit"},
        {"name": "exit", "args": [], "desc": "quit from the program", "func": "exit"},
        {"name": "help", "args": [], "desc": "print help message", "func": "show_help"},
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
