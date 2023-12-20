import jaro

def bot_commands():
  return [
    {
        'name': 'hello',
        'args': [],
        'desc': 'greetings message'
    },
    {
        'name': 'add',
        'args': ['name', 'phone'],
        'desc': 'add new contact in the phone book'
    },
    {
        'name': 'change',
        'args': ['name', 'phone'],
        'desc': 'change the saved contact phone'
    },
    {
        'name': 'phone',
        'args': ['name'],
        'desc': 'show the phone of the user with entered name'
    },
    {
        'name': 'add-birthday',
        'args': ['name', 'date'],
        'desc': "add birthday for name 'name' in format 'DD.MM.YYYY'"
    },
    {
        'name': 'show-birthday',
        'args': ['name'],
        'desc': "show birthday for name 'name'"
    },
    {
        'name': 'birthdays',
        'args': [],
        'desc': 'show all birthdays from the phone book on the next week'
    },
    {
        'name': 'birthdays-in-days',
        'args': ['days'],
        'desc': 'show all birthdays in a particular amount of days'
    },
    {
        'name': 'search-by-name',
        'args': [],
        'desc': 'shows all contacts with this name'
    },
    {
        'name': 'search-by-birthday',
        'args': [],
        'desc': 'shows all contacts with the specific birthday'
    },
    {
        'name': 'search-by-email',
        'args': [],
        'desc': 'shows all contacts with the specific email'
    },
    {
        'name': 'search-by-phones',
        'args': [],
        'desc': 'shows all contacts with the specific phone number'
    },
    {
        'name': 'all',
        'args': [],
        'desc': 'print the contacts phone book'
    },
    {
        'name': 'close',
        'args': [],
        'desc': 'quit from the program'
    },
    {
        'name': 'exit',
        'args': [],
        'desc': 'quit from the program'
    },
    {
        'name': 'help',
        'args': [],
        'desc': 'print help message'
    }
  ]

def find_closest_command(command_name):
  names = list(map(lambda bot_command: bot_command['name'], bot_commands()))
  distances = list(map(lambda name: {'name': name, 'dist': jaro.jaro_winkler_metric(name, command_name)}, names))
  return sorted(distances, key=lambda x: x['dist'])[-1]['name']