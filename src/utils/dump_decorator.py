def dump_contacts(func):
    def wrapper(*args, **kwargs):
        # Call the original function
        result = func(*args, **kwargs)
        # Extract the contacts from the arguments
        # Assuming contacts is always the second argument
        contacts = args[0]
        # Call the dump method
        contacts.dump()
        # Return the original result
        return result

    return wrapper
