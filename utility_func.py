import copy
import pickle
from classes import AddressBook, Name, Phone, Record, Birthday

CONTACTS = AddressBook()

def input_error(func):
    def inner(*args):
        try:
            result = func(*args)
            return result
        except KeyError:
            return "No user"
        except ValueError:
            return 'Give me name and phone please'
        except IndexError:
            return 'Enter user name'
        except TypeError:
            return 'Missed arguments'
    return inner

def hello_user():
    print('How can I help you?')
    return 

@input_error
def unknown_command(command):
    return f'Unknown command: {command}'

def goodbye():
    print('Good bye!')
    return

@input_error
def add_user(name: str, phone: str = None) -> str:
    name_rec = Name(name)
    phone_rec = Phone(phone)
    phone_rec.value = phone
    record = Record(name_rec, phone_rec)
    if name not in CONTACTS.data:
        result = f'New user {name} is added!'
    else:
        return add_phone(name, phone_rec)
    CONTACTS.add_record(record)
    return result

def add_phone(name: str, phone: str) -> str:
    record = CONTACTS.get_records(name)
    record.add_phone(phone)
    CONTACTS.add_record(record)
    return f'For user {name} is added a new phone {phone}!'

@input_error
def add_birthday(name: str, birthday: Birthday) -> str:
    record = CONTACTS.data.get(name)
    if not record:
        return "Contact not found"
    try: 
        bd_date_str = Birthday(birthday)
        bd_date_str.value = birthday
        record.set_birthday(bd_date_str)
        CONTACTS.add_record(record)
        return f"Added birthday: {bd_date_str.value}"
    except ValueError:
        return f"Invalid date format. Please use the format: DD-MM-YYYY. Birthday: {bd_date_str.value}"

@input_error
def change_phone(name, old_phone, new_phone):
    record = CONTACTS.get_records(name)
    if not record:
        return "Contact not found"
    result = record.change_phone(old_phone, new_phone)  
    return f'{name}`s {result}'

def remove_phone(name, phone): 
    record = CONTACTS.get_records(name)
    if not record:
        return "Contact not found"
    result = record.remove_phone(phone)
    return f'For {name} {result}'

def show_phone(name):
    if name == 'all':
        return show_all()
    else:
        result = ''
        record = CONTACTS.data.get(name)
        birthday = record.show_birthday()
        if record:
            result = f'{name} phone number is: {record.show_phone()}, {birthday} , next birthday in: {days_to_birthday(name)} days'
        else:
            result = f'We dont have {name} in our list'
    return result

def show_all():
    record = CONTACTS.data
    if not record:
        return "No contacts found" 
    result = ''
    for name, phone in record.items():
        birthday = phone.show_birthday()
        result += f'{name} phone number is: {phone.show_phone()}, {birthday}, next birthday in: {days_to_birthday(name)} days\n'
    return result

def days_to_birthday(name: str):
    record = CONTACTS.data.get(name)
    result = record.days_to_birthday()
    return result

@input_error
def paginate(page_size: int) -> str:
    result = ''
    page_size_int = int(page_size)
    for page in CONTACTS.paginate(page_size_int):
        for name, record in page:
            result += f"{name}: {record.show_phone()}, {record.show_birthday()}\n"
        result += "---\n" 
    return result

def search_contact_book(query: str) -> str:
    result = ''
    try:
        int(query)
        for name, record in CONTACTS.data.items():
            if query in CONTACTS.data.get(name):
                result += f'User: {name}, {record}\n'
    except ValueError:
        get_user = list(filter(lambda x: query.lower() in x.lower(), CONTACTS.data.keys()))
        for name in get_user:
            user_info = CONTACTS.data.get(name)
            result += f'User: {name}, {user_info.show_phone()}, {user_info.show_birthday()}\n'
    return result

def save():
    with open('Contacts.bin', 'wb') as file:
        pickle.dump(CONTACTS.data, file)
    return 'Contacts list saved!'

def load():
    with open('Contacts.bin', 'rb') as file:
        CONTACTS.data = pickle.load(file)
    return 'Contacts list loaded!'
        