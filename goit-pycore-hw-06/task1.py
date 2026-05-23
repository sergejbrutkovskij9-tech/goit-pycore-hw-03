from collections import UserDict


# ────────────────────────────────────────────
# Базові класи полів
# ────────────────────────────────────────────

class Field:
    """Базовий клас для полів запису."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Клас для зберігання імені контакту (обов'язкове поле)."""
    pass


class Phone(Field):
    """Клас для зберігання номера телефону з валідацією (рівно 10 цифр)."""
    def __init__(self, value: str):
        if not value.isdigit() or len(value) != 10:
            raise ValueError(f"Invalid phone number '{value}'. Must be exactly 10 digits.")
        super().__init__(value)


# ────────────────────────────────────────────
# Запис контакту
# ────────────────────────────────────────────

class Record:
    """Зберігає ім'я контакту та список його телефонів."""

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []

    def add_phone(self, phone: str) -> None:
        """Додає телефон до запису."""
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        """Видаляє телефон із запису. Піднімає ValueError якщо не знайдено."""
        target = self.find_phone(phone)
        if target is None:
            raise ValueError(f"Phone {phone} not found.")
        self.phones.remove(target)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """Замінює існуючий телефон на новий."""
        target = self.find_phone(old_phone)
        if target is None:
            raise ValueError(f"Phone {old_phone} not found.")
        idx = self.phones.index(target)
        self.phones[idx] = Phone(new_phone)

    def find_phone(self, phone: str) -> Phone | None:
        """Повертає об'єкт Phone або None якщо не знайдено."""
        return next((p for p in self.phones if p.value == phone), None)

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"


# ────────────────────────────────────────────
# Адресна книга
# ────────────────────────────────────────────

class AddressBook(UserDict):
    """Колекція записів Record з пошуком та видаленням за іменем."""

    def add_record(self, record: Record) -> None:
        """Додає запис до книги."""
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        """Знаходить запис за іменем. Повертає None якщо не знайдено."""
        return self.data.get(name)

    def delete(self, name: str) -> None:
        """Видаляє запис за іменем. Піднімає KeyError якщо не знайдено."""
        if name not in self.data:
            raise KeyError(f"Contact '{name}' not found.")
        del self.data[name]


# ────────────────────────────────────────────
# Демонстрація
# ────────────────────────────────────────────

if __name__ == "__main__":
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)

    # Створення та додавання запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів
    for record in book.data.values():
        print(record)

    # Редагування телефону John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    print(john)  # Contact name: John, phones: 1112223333; 5555555555

    # Пошук телефону
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # John: 5555555555

    # Видалення Jane
    book.delete("Jane")
    print("After deleting Jane:", list(book.data.keys()))  # ['John']