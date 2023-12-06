from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self._value = None  # використовуємо _value для внутрішнього представлення атрибута value
        self.value = value  # використовуємо setter для валідації значення

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not self.validate(new_value):
            raise ValueError(f"Invalid value for {self.__class__.__name__}")
        self._value = new_value

    def validate(self, value):
        """return boolean from check"""
        return True  # реалізуємо валідацію у підкласах


class Name(Field):
    pass


class Phone(Field):
    def validate(self, value):
        """return boolean from check"""
        return value.isdigit() and len(value) == 10


class Birthday(Field):
    def validate(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, " \
               f"birthday: {self.birthday.value}" if self.birthday else ""

    def add_phone(self, phone_number: str):
        phone = Phone(phone_number)
        if phone not in self.phones:
            self.phones.append(phone)

    def find_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def edit_phone(self, old_phone, new_phone):
        phone_exists = False
        for index, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[index] = Phone(new_phone)
                phone_exists = True
        if not phone_exists:
            raise ValueError(f"The phone number {old_phone} does not exist.")

    def remove_phone(self, phone):
        for item in self.phones:
            if item.value == phone:
                self.phones.remove(item)
                break

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = datetime.now()
        next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day)
        if today > next_birthday:
            next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day)
        days_remaining = (next_birthday - today).days
        return days_remaining


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: Name):
        return self.data.get(name)

    def delete(self, name: Name):
        if name in self.data:
            del self.data[name]

    def iterator(self, batch_size=10):
        for i in range(0, len(self.data), batch_size):
            yield list(self.data.values())[i:i + batch_size]
