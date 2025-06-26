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
    for i, p in enumerate(self.phones):
      if p.value == old_phone:
        phone_at_list = Phone(new_phone)
        if hasattr(phone_at_list, 'value') and phone_at_list.value != "":
          self.phones[i] = phone_at_list
        return
    raise ValueError(f"Phone {old_phone} not found")

  def find_phone(self, phone):
    for p in self.phones:
      if p.value == phone:
        return p
    return None

  def to_dict(self):
    """Converts Record to dictionary for JSON serialization"""
    return {
      "name": self.name.value,
      "phones": [p.value for p in self.phones]
    }

  @classmethod
  def from_dict(cls, data):
    """Creates Record from dictionary after JSON deserialization"""
    record = cls(data["name"])
    for phone in data.get("phones", []):
      record.add_phone(phone)
    return record

  def __str__(self):
    if len(self.phones) > 0 and self.name.value != "":
      return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    return ""


class AddressBook(UserDict):
  def __init__(self, initial_contacts=None):
    if initial_contacts and isinstance(list(initial_contacts.values())[0] if initial_contacts else None, dict):
      # If data came from JSON (as dictionaries), convert them to Record objects
      self.data = {}
      for name, contact_data in initial_contacts.items():
        self.data[name] = Record.from_dict(contact_data)
    else:
      # If data are already Record objects
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
  def get_contacts_for_json(self):
    """Returns contacts in format suitable for JSON serialization"""
    return {name: record.to_dict() for name, record in self.data.items()}

  def __str__(self):
    return "\n".join(str(record) for record in self.data.values())
