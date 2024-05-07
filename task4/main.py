from pathlib import Path


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as err:
            if len(args) > 0:
                return err.args[0]
            else:
                return err.__doc__
        except KeyError:
            return "Contact does not exist."
        except IndexError:
            return "Arguments are required."

    return inner


def get_contact_filepath():
    datapath = Path("./data/contacts.dat")
    if not datapath.exists():
        with open(datapath, "w+"):
            return datapath

    return datapath


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, contacts):
    if len(args) != 2:
        raise ValueError("invalid params. The correct is: add ContactName PhoneNumber")

    name, phone = args

    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts):
    if len(args) != 2:
        raise ValueError(
            "invalid params. The correct is: change ContactName NewPhoneNumber"
        )

    name, phone = args

    contacts[name] = phone
    return "Contact changed."


@input_error
def remove_contact(args, contacts):
    if len(args) != 1:
        raise ValueError("invalid params. The correct is: remove ContactName")

    name = args[0]
    contacts.pop(name)
    return "Contact removed."


@input_error
def show_contacts(contacts):
    maxlen = 10
    for name in contacts.keys():
        if len(name) > maxlen:
            maxlen = len(name)
    maxlen += 2
    print(f"{'Contact Name':{maxlen}} \t Phone number")
    for name in contacts.keys():
        print(f"{name:{maxlen}} \t {contacts[name]}")


def get_allowed_commands():
    return ["close", "exit", "add", "change", "remove", "show", "phone"]


def save_contacts(contacts, path):
    with open(path, "w") as file:
        for name in contacts.keys():
            file.write(f"{name};{contacts[name]}\n")


def load_contacts(path):
    contacts = {}
    with open(path, "r") as file:
        for contactline in file.readlines():
            contacts[contactline.split(";")[0]] = contactline.split(";")[1].strip()
    return contacts


@input_error
def get_phone(args, contacts):
    if len(args) != 1:
        raise ValueError("invalid params. The correct is: remove ContactName")
    name = args[0]

    if contacts.keys().__contains__(name):
        return contacts[name]
    else:
        return f"Contact with name {name} is not found."


def main():
    # contacts = load_contacts(get_contact_filepath())
    print("Welcome to the assistant bot!")
    contacts = {}
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        match command:
            case "close":
                print("Good bye!")
                save_contacts(contacts, get_contact_filepath())
                break
            case "exit":
                print("Good bye!")
                save_contacts(contacts, get_contact_filepath())
                break
            case "add":
                print(add_contact(args, contacts))
            case "change":
                print(change_contact(args, contacts))
            case "remove":
                print(remove_contact(args, contacts))
            case "show":
                show_contacts(contacts)
            case "phone":
                print(get_phone(args, contacts))
            case _:
                print("Invalid command.")


if __name__ == "__main__":
    main()
