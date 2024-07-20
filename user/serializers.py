import json
import uuid
import case_changer
from typing import Any, Optional, Union
from pydantic import BaseModel


class SerializerBase(BaseModel):
    class Config:
        alias_generator = case_changer.camel_case
        populate_by_name = True


class User(SerializerBase):
    id: Optional[uuid.UUID] = None
    email: Union[str, None] = None
    name: Union[str, None]
