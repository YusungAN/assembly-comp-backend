from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship


from db import Base


from typing import Union
from pydantic import BaseModel

class UserText(BaseModel):
    text: str