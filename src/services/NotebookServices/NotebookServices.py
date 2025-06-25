from helper.color_loger import  log_warning
from decorators.error_decorators import input_error
from collections import UserDict
from dataclasses import dataclass

class Field:
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return str(self.value)

class Name(Field):
  @input_error
  def __init__(self, value):
    if not value.isalpha():
      raise ValueError("Name must contain only letters")
    self.value = value


class Phone(Field):
  @input_error
  def __init__(self, value):
    if not value.isdigit():
      raise ValueError("Phone number must contain only digits")
    if len(value) != 10:
      raise ValueError("Phone number must be 10 digits")
    self.value = value


@dataclass
class Record:
  name: Name
  phones: list[Phone] | None

class Record(Record):
  def __init__(self, name):
    self.name = Name(name)
    self.phones = []

  def add_phone(self, phone):
    phone_at_list = Phone(phone)
    if hasattr(phone_at_list, 'value') and phone_at_list.value != "":
      self.phones.append(phone_at_list)

  def remove_phone(self, phone):
    self.phones = [p for p in self.phones if p.value != phone]

  @input_error
  def edit_phone(self, old_phone, new_phone):
    for p in self.phones:
      if p.value == old_phone:
        p.value = new_phone
        return
    raise ValueError(f"Phone {old_phone} not found")

  def find_phone(self, phone):
    for p in self.phones:
      if p.value == phone:
        return p
    return None

  def __str__(self):
    if len(self.phones) > 0 and self.name.value != "":
      return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    return ""


class AddressBook(UserDict):
  def __init__(self, initial_contacts=None):
    self.data = initial_contacts if initial_contacts else {}

  def add_record(self, record):
    self.data[record.name.value] = record

  @input_error
  def find(self, name):
    if name == "":
      raise ValueError("Please provide name")
    return self.data.get(name)

  def delete(self, name):
    del self.data[name]


  @input_error
  def get_all_contacts(self):
    return self.data

  def __str__(self):
    return "\n".join(str(record) for record in self.data.values())
