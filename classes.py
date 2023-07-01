from collections import UserDict
from re import match
from datetime import datetime, date

class Field:
    def __init__(self, value) -> None:
        self.value = value

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, new_value):
        self.validator(new_value)
        self.__value = new_value
    
    def validator(self, value):
        pass


class Name(Field):
    def __init__(self, value) -> None:
        super().__init__(value)

    def __repr__(self) -> str:
        return f"{self.value}"

class Phone(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
 
    def validator(self, new_value):
        if isinstance(new_value, str):
            if not match(r'^\+38\d{10}$', new_value):
                print("Phone number should be in the format +380XXXXXXXXX")
                raise ValueError("Phone number should be in the format +380XXXXXXXXX")
        else:
            raise ValueError('value must be str not int')
            
    def __repr__(self) -> str:
        return f"{self.value}"

class Birthday(Field):
    def __init__(self, value) -> None:
        super().__init__(value)

    def validator(self, new_value):
        if not isinstance(new_value, str):
            raise ValueError
        try:
            datetime.strptime(new_value, '%d-%m-%Y')
        except ValueError:
            raise ValueError

class Record:
    def __init__(self, name: Name, phone: Phone=None, birthday: Birthday=None) -> None:
        self.name = name
        self.phones = []
        self.birthday = None
        if phone is not None:
            self.add_phone(phone)

        if birthday is not None:
            self.set_birthday(birthday)

    def set_birthday(self, birthday: Birthday):
        self.birthday = birthday.value

    def remove_birthday(self):
        self.birthday = None

    def days_to_birthday(self) -> int:
        if self.birthday is None:
            return 'please enter your date of birth'
        
        today = date.today()
        birthday = datetime.strptime(self.birthday, '%d-%m-%Y').date()
        next_bd = date(today.year, birthday.month, birthday.day)
        
        if today > next_bd:
            next_bd = date(today.year + 1, birthday.month, birthday.day)

        days_to_birthday = (next_bd - today).days
        return days_to_birthday

    def add_phone(self, phone: Phone | str):
        if isinstance(phone, str):
            phone = self.create_phone(phone)
        self.phones.append(phone)
    
    def create_phone(self, phone: str):
        return Phone(phone)

    def remove_phone(self, phone):
        new_phone_list = list(filter(lambda x: str(x) != str(phone), self.phones))
        if len(new_phone_list) != len(self.phones):
            self.phones = list(new_phone_list)
            return f'phone: {phone} deleted'
        return f'phone {phone} not found'

    def change_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return f'{old_phone} has been changed to a new one: {new_phone}'
            else:
                return f'Phone {old_phone} not found'
    
    def show_phone(self):
        res = ''
        for index, phone in enumerate(self.phones):
           res += f'{index + 1}. {phone.value} '
        return res
    
    def show_birthday(self):
        if self.birthday is None:
            return 'date of birth not specified'
        return f'birthday: {self.birthday}'

    def __repr__(self) -> str:
        return f'{self.phones}'
    
class Iterator:
    def __init__(self, records) -> None:
        self.records = records
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.records):
            raise StopIteration
        record = self.records[self.index]
        self.index += 1
        return record

class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def get_records(self, name: str) -> Record:
        return self.data[name]
    
    def __str__(self) -> str:
        print({self.data})

    def __iter__(self):
        return Iterator(list(self.data.values()))

    def paginate(self, page_size: int):
        records = list(self.data.values())
        total_records = len(records)
        num_pages = (total_records + page_size - 1) // page_size

        for page in range(num_pages):
            start_index = page * page_size
            end_index = (page + 1) * page_size
            yield [(record.name.value, record) for record in records[start_index:end_index]]

    
    