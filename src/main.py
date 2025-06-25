from services.NotebookServices import AddressBook, Record, Name, Phone
from services.DataServices import DataServices
from helper.color_loger import log_error

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def validate_args(args, required_count, error_message):
    """Перевіряє, чи достатньо аргументів для команди"""
    if len(args) < required_count:
        print(error_message)
        return False
    return True

def find_contact_safe(contacts, name):
    """Безпечно знаходить контакт за іменем"""
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
                if not validate_args(args, 2, "Будь ласка, вкажіть ім'я та номер телефону"):
                    continue
                record = find_contact_safe(contacts, args[0])
                if record:
                    record.add_phone(args[1])
                    print(contacts)
                else:
                    record = Record(args[0])
                    record.add_phone(args[1])
                    contacts.add_record(record)
                    print(contacts)
            case "change":
                if not validate_args(args, 3, "Будь ласка, вкажіть ім'я, старий та новий номер телефону"):
                    continue

                record = find_contact_safe(contacts, args[0])
                if record:
                    record.edit_phone(args[1], args[2])
                else:
                    print("Контакт не знайдено")
                print(contacts)
            case "phone":
                if not validate_args(args, 1, "Будь ласка, вкажіть ім'я"):
                    continue

                record = find_contact_safe(contacts, args[0])
                if record:
                    print(record)
                else:
                    print("Контакт не знайдено")

            case "remove_phone":
                if not validate_args(args, 2, "Будь ласка, вкажіть ім'я та номер телефону"):
                    continue

                record = find_contact_safe(contacts, args[0])
                if record:
                    record.remove_phone(args[1])
                    print(f"Телефон видалено з контакту {args[0]}")
                else:
                    print("Контакт не знайдено")

            case "remove":
                if not validate_args(args, 1, "Будь ласка, вкажіть ім'я"):
                    continue

                contacts.delete(args[0])
                print(f"Контакт {args[0]} видалено")

            case "all":
                print(contacts)
            case "exit" | "close":
                all_contacts = contacts.get_all_contacts()
                data.save_data(all_contacts)
                print("До побачення!")
                break
            case _:
                log_error("Невірна команда.")

if __name__ == "__main__":
    main()
