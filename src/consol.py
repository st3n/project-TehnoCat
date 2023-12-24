from rich.console import Console
from rich.table import Table



def display_table_all(contacts):
    console = Console()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Name", style="cyan", width=20)
    table.add_column("Phones", style="yellow", width=40)
    table.add_column("Address", style="blue", width=30)
    table.add_column("Email", style="magenta", width=30)
    table.add_column("Birthday", style="green", width=20)

    for name, record in contacts.data.items():
        phones_str = ", ".join(str(p.value) for p in record.phones) if hasattr(record, "phones") and record.phones else "None"
        
        addresses_str = ", ".join(str(a.value) for a in record.address) if hasattr(record, "address") and record.address else "None"
        
        emails_str = ", ".join(str(e.value) for e in record.emails) if hasattr(record, "emails") and record.emails else "None"
        
        birthday_str = str(record.birthday) if hasattr(record, "birthday") and record.birthday else "None"
        
        table.add_row(name, phones_str, addresses_str, emails_str, birthday_str)

    console.print(table)


