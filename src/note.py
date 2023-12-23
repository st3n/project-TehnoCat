class Notes:
    def __init__(self, file_name='notes.txt'):
        self.file_name = file_name

    def add_note(self, contact_name, note, tag=None):
        with open(self.file_name, 'a') as file:
            if tag:
                file.write(f"{contact_name}: {note} #{tag}\n")
            else:
                file.write(f"{contact_name}: {note}\n")

    def add_tag(self, contact_name, tag):
        try:
            with open(self.file_name, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print(f"File '{self.file_name}' not found. File will be created.")
            lines = []

        found_contact = False
        for i, line in enumerate(lines):
            if contact_name in line:
                found_contact = True
                if f"#{tag}" not in line:
                    lines[i] = f"{contact_name}: {line.split(':', 1)[1].strip()} #{tag}\n"
                else:
                    print(f"Tag #{tag} already exists for contact {contact_name}")
                break

        if not found_contact:
            with open(self.file_name, 'a') as file:
                file.write(f"{contact_name}: #{tag}\n")

        with open(self.file_name, 'w') as file:
            file.writelines(lines)

    def show_all_notes(self):
        try:
            with open(self.file_name, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print(f"File '{self.file_name}' not found.")
            return []

        all_notes = []
        prev_contact = None

        for line in lines:
            contact, rest = line.split(":", 1)
            contact = contact.strip()
            rest = rest.strip()
            tag = None

            if "#" in rest:
                tag_start = rest.find("#") + 1
                tag = rest[tag_start:].strip()
                rest = rest.replace(f"#{tag}", "").strip()

            if contact == prev_contact:
                all_notes[-1] = (contact, rest, tag)
            else:
                all_notes.append((contact, rest, tag))
                prev_contact = contact

        return all_notes

    def search_note_by_tag_or_contact(self, query):
        query_lower = query.lower()
        with open(self.file_name, 'r') as file:
            lines = file.readlines()
            matching_notes = [line for line in lines if query_lower in line.lower()]
        return ''.join(matching_notes)

    def search_tag(self, tag_query):
        tag_query = f"#{tag_query}"
        with open(self.file_name, 'r') as file:
            lines = file.readlines()
            matching_notes = [line for line in lines if tag_query in line]
        return ''.join(matching_notes)

    def change_note(self, contact_name, new_note):
        with open(self.file_name, 'r') as file:
            lines = file.readlines()
        with open(self.file_name, 'w') as file:
            for line in lines:
                if contact_name in line:
                    file.write(f"{contact_name}: {new_note}\n")
                else:
                    file.write(line)

    def delete_note_by_contact(self, contact_name):
        with open(self.file_name, 'r') as file:
            lines = file.readlines()
        with open(self.file_name, 'w') as file:
            for line in lines:
                if contact_name not in line:
                    file.write(line)

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
            search_query = input("Enter the contact name to search for: ")
            matching_notes = notes.search_note_by_tag_or_contact(search_query)
            if matching_notes:
                print("Matching Notes:\n", matching_notes)
            else:
                print("No notes found with this contact name.")

        elif user_input == 'search tag':
            tag_query = input("Enter the tag to search for: ")
            matching_notes = notes.search_tag(tag_query)
            if matching_notes:
                print("Matching Notes:\n", matching_notes)
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