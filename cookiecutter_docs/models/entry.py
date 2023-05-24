"""Model."""

from pydantic import BaseModel


class Entry(BaseModel):
    key: str
    value: str
    description: str
