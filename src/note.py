import os

class RecordDoesNotExistError(Exception):
    pass

class Contact:
    def __init__(self, name):
        self.name = name
        self.notes = []
        self.tags = []

    def add_note_with_tag(self, note, tag):
        self.notes.append(note)
        self.tags.append(tag)

    def add_tag(self, tag):
        self.tags.append(tag)

    def change_note(self, new_note):
        if self.notes:
            self.notes[-1] = new_note

class Notes:
    def __init__(self, file_name='notes.txt'):
        self.file_name = file_name
        self.contacts = {}

    def add_note(self, contact_name, note, tag=None):
        if contact_name not in self.contacts:
            raise RecordDoesNotExistError(contact_name)

        if tag:
            self.contacts[contact_name].add_note_with_tag(note, tag)
            return f"Note '{note}' with tag '#{tag}' for contact {contact_name} added."
        else:
            self.contacts[contact_name].add_note(note)
            return f"Note '{note}' for contact {contact_name} added."

    def add_tag(self, contact_name, tag):
        if contact_name not in self.contacts:
            raise RecordDoesNotExistError(contact_name)

        self.contacts[contact_name].add_tag(tag)
        return f"Tag '#{tag}' added for contact {contact_name}."

    def show_all_notes(self):
        if not self.contacts:
            raise KeyError("No contacts found.")

        all_notes = []
        for contact in self.contacts.values():
            for note, tag in zip(contact.notes, contact.tags):
                all_notes.append((contact.name, note, tag))
        return all_notes

    def search_by_name(self, args):
        value = args[0]
        search_result = []
        for contact in self.contacts.values():
            if value.lower() in contact.name.lower():
                search_result.append(contact)
        return search_result

    def search_tag(self, args):
        value = args[0]
        search_result = []
        for contact in self.contacts.values():
            if value.lower() in map(str.lower, contact.tags):
                search_result.append(contact)
        return search_result

    def search_note(self, args):
        contact_name = args[0]
        search_result = []
        for contact in self.contacts.values():
            if contact_name.lower() == contact.name.lower():
                for note, tag in zip(contact.notes, contact.tags):
                    search_result.append((contact.name, note, tag))
        return search_result

    def change_note(self, contact_name, new_note):
        if contact_name not in self.contacts:
            raise RecordDoesNotExistError(contact_name)

        self.contacts[contact_name].change_note(new_note)
        return f"{contact_name}'s note changed to '{new_note}'."

    def delete_note_by_contact(self, contact_name):
        if contact_name in self.contacts:
            del self.contacts[contact_name]
        else:
            raise RecordDoesNotExistError(contact_name)

if __name__ == "__main__":
    notes = Notes()

    while True:
        user_input = input("Enter a command (add note, show all notes, search note, add tag, search tag, change note, delete note, back): ").strip()

        if user_input == 'add note':
            contact_name = input("Enter contact's name: ")
            note = input("Enter the note: ")
            notes.add_note(contact_name, note)
            print("Note added!")

        elif user_input == 'add tag':
            contact_name = input("Enter contact's name for adding tag: ")
            tag = input("Enter the tag: ")
            notes.add_tag(contact_name, tag)
            print("Tag added!")

        elif user_input == 'show all notes':
            all_notes = notes.show_all_notes()
            print("All Notes:")
            for contact, rest, tag in all_notes:
                print(f"{contact}: {rest} {'#' + tag if tag else ''}")

        elif user_input == 'search note':
            search_query = input("Enter the note to search for: ")
            matching_notes = notes.search_note([search_query])
            if matching_notes:
                print("Matching Notes:")
                for contact_name, note, tag in matching_notes:
                    print(f"{contact_name}: {note} {'#' + tag if tag else ''}")
            else:
                print("No notes found with this note.")

        elif user_input == 'search tag':
            tag_query = input("Enter the tag to search for: ")
            matching_notes = notes.search_tag([tag_query])
            if matching_notes:
                print("Matching Notes:")
                for contact in matching_notes:
                    for note, tag in zip(contact.notes, contact.tags):
                        print(f"{contact.name}: {note} {'#' + tag if tag else ''}")
            else:
                print("No notes found with this tag.")

        elif user_input == 'change note':
            contact_name = input("Enter contact's name for changing: ")
            new_note = input("Enter the new note: ")
            notes.change_note(contact_name, new_note)
            print("Note changed!")

        elif user_input == 'delete note':
            contact_name = input("Enter contact's name for deletion: ")
            notes.delete_note_by_contact(contact_name)
            print("Note deleted!")

        elif user_input == 'back':
            print("Going back to the previous menu.")
            break

        else:
            print("Unknown command. Please try again.")
