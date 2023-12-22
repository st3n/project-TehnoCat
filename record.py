from contact_data import *

   
class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def __str__(self):
        return f"[bold purple]Contact name:[/bold purple] {self.name.value}[bold purple], phones: [/bold purple]{', '.join(p.value for p in self.phones)}\n"

    def add_phone(self, phone):
        if Phone.is_valid_phone(phone):
            self.phones.append(Phone(phone))
        else:
            raise ValueError("[bold yellow]Error: the phone number must be 10 digits[/bold yellow]\U0001F914\n")

    def remove_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        if Phone.is_valid_phone(new_phone):
            for item in self.phones:
                if item.value == old_phone:
                    item.value = new_phone
                    return
            raise ValueError(
                f"[bold yellow]Error: the phone number {old_phone} not found in the record.[/bold yellow]\U0001F914\n"
            )
        else:
            raise ValueError("[bold yellow]Error: the phone number must be 10 digits[/bold yellow]\U0001F914\n")

    def find_phone(self, phone):
        for item in self.phones:
            if item.value == phone:
                return item.value
        raise ValueError(f"[bold yellow]Error: the phone number {phone} not found in the record.[/bold yellow]\U0001F914\n")

    def add_birthday(self, date):
        self.birthday = Birthday(date)
