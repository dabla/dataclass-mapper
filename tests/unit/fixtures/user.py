from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from datamapper.converters import converters
from datamapper.decorators import datamap


@dataclass
class User:
    id: UUID
    age: int
    username: str
    name: str
    surname: str
    active: bool


def parse_uuid(value: Optional[str]) -> Optional[UUID]:
    if value:
        return UUID(value)
    return None


def parse_str_to_int(value: Optional[str]) -> Optional[int]:
    if value:
        return int(value)
    return 0


@datamap(data_class=User)
def get_user() -> User:
    return {
        "id": "b0aa940d-61d9-4b83-94dc-1fd8f2b88dbb",
        "age": "",
        "username": "BKD7702",
        "name": "David",
        "surname": "Blain",
        "active": True,
    }


converters["str_uuid"] = parse_uuid
converters["str_int"] = parse_str_to_int
