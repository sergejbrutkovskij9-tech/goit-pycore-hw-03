import sys

# ────────────────────────────────────────────
# Декоратор обробки помилок
# ────────────────────────────────────────────

def input_error(func):
    """Декоратор для обробки типових помилок введення користувача."""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter the argument for the command."
    return inner


# ────────────────────────────────────────────
# Обробники команд
# ────────────────────────────────────────────

@input_error
def add_contact(args: list, contacts: dict) -> str:
    """Додає новий контакт або оновлює існуючий."""
    name, phone = args          # ValueError якщо args має менше 2 елементів
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args: list, contacts: dict) -> str:
    """Змінює номер телефону існуючого контакту."""
    name, phone = args          # ValueError якщо args має менше 2 елементів
    if name not in contacts:
        raise KeyError
    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args: list, contacts: dict) -> str:
    """Показує номер телефону за ім'ям контакту."""
    name = args[0]              # IndexError якщо args порожній
    return f"{name}: {contacts[name]}"   # KeyError якщо контакт не знайдено


@input_error
def show_all(contacts: dict) -> str:
    """Повертає список усіх збережених контактів."""
    if not contacts:
        return "No contacts saved."
    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())


# ────────────────────────────────────────────
# Парсинг введення
# ────────────────────────────────────────────

def parse_input(user_input: str) -> tuple:
    """Розбиває рядок на команду та аргументи."""
    parts = user_input.strip().split()
    command = parts[0].lower() if parts else ""
    args = parts[1:]
    return command, args


# ────────────────────────────────────────────
# Головний цикл
# ────────────────────────────────────────────

def main():
    contacts = {}
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ").strip()

        if not user_input:
            continue

        command, args = parse_input(user_input)

        match command:
            case "hello":
                print("How can I help you?")

            case "add":
                print(add_contact(args, contacts))

            case "change":
                print(change_contact(args, contacts))

            case "phone":
                print(show_phone(args, contacts))

            case "all":
                print(show_all(contacts))

            case "close" | "exit":
                print("Good bye!")
                sys.exit(0)

            case _:
                print("Invalid command.")


if __name__ == "__main__":
    main()