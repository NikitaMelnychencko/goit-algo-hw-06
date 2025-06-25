from services.NotebookServices import AddressBook, Record, Name, Phone
from services.DataServices import DataServices
from helper.color_loger import log_error

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def validate_args(args, required_count, error_message):
    """Checks if there are enough arguments for the command"""
    if len(args) < required_count:
        print(error_message)
        return False
    return True

def find_contact_safe(contacts, name):
    """Safely finds contact by name"""
    try:
        return contacts.find(name)
    except:
        return None

welcome_bunner = """
 █████╗ ███████╗███████╗██╗███████╗████████╗ █████╗ ███╗   ██╗████████╗    ██████╗  ██████╗ ████████╗
██╔══██╗██╔════╝██╔════╝██║██╔════╝╚══██╔══╝██╔══██╗████╗  ██║╚══██╔══╝    ██╔══██╗██╔═══██╗╚══██╔══╝
███████║███████╗███████╗██║███████╗   ██║   ███████║██╔██╗ ██║   ██║       ██████╔╝██║   ██║   ██║
██╔══██║╚════██║╚════██║██║╚════██║   ██║   ██╔══██║██║╚██╗██║   ██║       ██╔══██╗██║   ██║   ██║
██║  ██║███████║███████║██║███████║   ██║   ██║  ██║██║ ╚████║   ██║       ██████╔╝╚██████╔╝   ██║
╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝       ╚═════╝  ╚═════╝    ╚═╝

"""

commands = """
  Commands:
  ---------
  1. hello
  2. add <username> <phone>
  3. change <username> <old_phone> <new_phone>
  4. remove phone in contact <username> <phone>
  5. remove contact <username>
  6. phone <username>
  7. all
  8. close, exit
  ---------
"""


def main():
    data = DataServices()
    contacts = AddressBook(data.get_init_data())
    print(welcome_bunner)
    print("Welcome to the assistant bot!")
    print(commands)

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        match (command.lower()):
            case "hello":
                print("How can I help you?")
            case "add":
                is_valid = validate_args(args, 2, "Please provide name and phone number")
                if is_valid:
                    record = find_contact_safe(contacts, args[0])
                    if record:
                        record.add_phone(args[1])
                        print(contacts)
                    else:
                        record = Record(args[0])
                        # Check if the name is valid and not empty
                        if hasattr(record.name, 'value') and record.name.value != "":
                            record.add_phone(args[1])
                            if len(record.phones) > 0:
                                contacts.add_record(record)
                                print(contacts)
            case "change":
                if not validate_args(args, 3, "Please provide name, old phone number and new phone number"):
                    continue

                record = find_contact_safe(contacts, args[0])
                if record:
                    record.edit_phone(args[1], args[2])
                    print(contacts)
                else:
                    print("Contact not found")
            case "phone":
                if not validate_args(args, 1, "Please provide name"):
                    continue

                record = find_contact_safe(contacts, args[0])
                if record:
                    print(record)
                else:
                    print("Contact not found")

            case "remove_phone":
                if not validate_args(args, 2, "Please provide name and phone number"):
                    continue

                record = find_contact_safe(contacts, args[0])
                if record:
                    record.remove_phone(args[1])
                    print(contacts)
                else:
                    print("Contact not found")

            case "remove":
                if not validate_args(args, 1, "Please provide name"):
                    continue

                record = find_contact_safe(contacts, args[0])
                if record:
                    contacts.delete(args[0])
                    print(contacts)
                else:
                    print("Contact not found")

            case "all":
                print(contacts)
            case "exit" | "close":
                all_contacts = contacts.get_all_contacts()
                data.save_data(all_contacts)
                print("Goodbye!")
                break
            case _:
                log_error("Invalid command.")

if __name__ == "__main__":
    main()
