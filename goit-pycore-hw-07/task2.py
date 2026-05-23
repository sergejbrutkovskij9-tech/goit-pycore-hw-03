import sys
from collections import UserDict
from datetime import date, datetime, timedelta


# ────────────────────────────────────────────
# Моделі
# ────────────────────────────────────────────

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value: str):
        if not value.isdigit() or len(value) != 10:
            raise ValueError(f"Invalid phone '{value}'. Must be exactly 10 digits.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value: str):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None

    def add_phone(self, phone: str) -> None:
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        target = self.find_phone(phone)
        if target is None:
            raise ValueError(f"Phone {phone} not found.")
        self.phones.remove(target)

    def edit_phone(self, old: str, new: str) -> None:
        target = self.find_phone(old)
        if target is None:
            raise ValueError(f"Phone {old} not found.")
        self.phones[self.phones.index(target)] = Phone(new)

    def find_phone(self, phone: str) -> Phone | None:
        return next((p for p in self.phones if p.value == phone), None)

    def add_birthday(self, value: str) -> None:
        self.birthday = Birthday(value)

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones) or "—"
        bday_str = str(self.birthday) if self.birthday else "—"
        return (f"Contact name: {self.name.value}, "
                f"phones: {phones_str}, birthday: {bday_str}")


class AddressBook(UserDict):

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name not in self.data:
            raise KeyError(f"Contact '{name}' not found.")
        del self.data[name]

    def get_upcoming_birthdays(self, days: int = 7) -> list[dict]:
        today = date.today()
        result = []
        for record in self.data.values():
            if record.birthday is None:
                continue
            bday = record.birthday.value.replace(year=today.year)
            if bday < today:
                bday = bday.replace(year=today.year + 1)
            if (bday - today).days > days:
                continue
            if bday.weekday() == 5:
                bday += timedelta(days=2)
            elif bday.weekday() == 6:
                bday += timedelta(days=1)
            result.append({
                "name": record.name.value,
                "congratulation_date": bday.strftime("%d.%m.%Y"),
            })
        return result


# ────────────────────────────────────────────
# Декоратор
# ────────────────────────────────────────────

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e) if str(e) else "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter the argument for the command."
    return inner


# ────────────────────────────────────────────
# Обробники команд
# ────────────────────────────────────────────

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phone(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    return ", ".join(p.value for p in record.phones) or "No phones."


@input_error
def show_all(book: AddressBook):
    if not book.data:
        return "No contacts saved."
    return "\n".join(str(r) for r in book.data.values())


@input_error
def add_birthday(args, book: AddressBook):
    name, bday, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_birthday(bday)
    return "Birthday added."


@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    return str(record.birthday) if record.birthday else "Birthday not set."


@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays in the next 7 days."
    return "\n".join(
        f"{item['name']}: {item['congratulation_date']}" for item in upcoming
    )


# ────────────────────────────────────────────
# Парсинг та головний цикл
# ────────────────────────────────────────────

def parse_input(user_input: str):
    parts = user_input.strip().split()
    return (parts[0].lower(), *parts[1:]) if parts else ("",)


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()