from typing import Union
from pydantic import BaseModel

class UserText(BaseModel):
    text: str