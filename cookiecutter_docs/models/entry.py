"""Model."""

from pydantic import BaseModel


class Entry(BaseModel):
    """Input in cookiecutter."""

    key: str
    value: str
    description: str
