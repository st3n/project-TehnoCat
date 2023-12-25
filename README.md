# Phone book assistant
## Installation
1. Clone repository and move to the root:
```shell
git clone https://github.com/st3n/project-TehnoCat.git
cd project-TehnoCat
```
2. Create and activate venv
```shell
conda create -n <name_of_venv>
conda activate <name_of_venv>
```
3. Install package
```shell
pip install -e .
```
4. Now the assistant is available by typing `tehnocat`:
```shell
foo@bar:~$ tehnocat
Welcome to the assistant bot!
Enter a command: 
```

## Possible commands
```
'hello' - greetings message
'add [name] [phone]' - add new contact in the phone book
'change [name] [phone]' - change the saved contact phone
'phone [name]' - show the phone of the user with entered name
'add-birthday [name] [date]' - add birthday for name 'name' in format 'DD.MM.YYYY'
'show-birthday[name]' - show birthday for name 'name'
'show-birthday [name]' - show birthday for name 'name'
'birthdays' - show all birthdays from the phone book on the next week
'birthdays-in-days [days]' - show all birthdays in a particular amount of days
'search-by-name [name]' - shows all contacts with this name
'search-by-birthday [date]' - shows all contacts with the specific birthday
'search-by-emails [email]' - shows all contacts with the specific email
'search-by-phones [phone1] [phone2] ...' - shows all contacts with the specific phone number
'all' - print the contacnts phone book
'close' or 'exit' - quit from the program
'help' - print help message

```
