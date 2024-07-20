import json
import uuid
import case_changer
from typing import Any, Optional, Union
from pydantic import BaseModel


class SerializerBase(BaseModel):
    class Config:
        alias_generator = case_changer.camel_case
        populate_by_name = True


class Login(SerializerBase):
    name: str
    password: str


class Registration(SerializerBase):
    name: Union[str]
    password: str
    phone_number: str
    email: Union[str, None] = None


class User(SerializerBase):
    id: uuid.UUID
    name: str
    email: str
    phone_number: str


class CreateContact(SerializerBase):
    name: str
    is_spam: bool = False
    phone_number: str


class Contact(SerializerBase):
    id: uuid.UUID
    name: str
    is_spam: bool = False
    phone_number: str
