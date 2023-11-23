from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone number must be a ten digit string of digits")
        super().__init__(value)
    def validate(self, value):
        """return boolean from check"""
        return value.isdigit() and len(value) == 10
    


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone_number: str):
        phone = Phone(phone_number)
        phone.validate(phone_number)
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

        


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: Name):
        if name in self.data:
            return self.data[name]
        else:
            return None

    def delete(self, name: Name):
        if name in self.data:
            del self.data[name]