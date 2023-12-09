from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.__value = None  
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if not self.validate(new_value):
            raise ValueError(f"Invalid value")
        self.__value = new_value

    def validate(self, value):
        return True


class Name(Field):
    pass


class Phone(Field):
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if not self.validate(new_value):
            raise ValueError(f"Invalid phone value")
        self.__value = new_value 
    
    def validate(self, value):
        return value.isdigit() and len(value) == 10


class Birthday(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if not self.validate(new_value):
            raise ValueError(f"Invalid Birthday format")
        self.__value = new_value
    
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
# ДЗ_11. Оператор, що повертає кількість днів до дня народження
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
            
# ДЗ_11. ітератор для посторінкового виводу данних телефонної книги

    def iterator(self, n):
        for i in range(0, len(self.data), n):
            yield list(self.data.values())[i:i + n]
