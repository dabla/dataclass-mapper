# Datamap [0.0.16]
[![Build Status](https://travis-ci.org/dabla/datamap.svg?branch=master)](https://travis-ci.org/dabla/datamap)

Datamap will apply the PEP8 naming convention on the dict keys, flatten nested dicts if required and map those dicts to dataclasses using the [dacite](https://github.com/konradhalas/dacite) module.
If the module encounters dict values which are integers but are mapped to a datetime in the dataclass, it will also try to convert those to datetime. 


## Install

```bash
pip install datamap==0.0.16
```

## Usage

```python
from dataclasses import dataclass
from datetime import datetime

from datamap.decorators import datamap


@dataclass
class DateAttribute:
    id: str
    created_by: str
    created_on: datetime
    asset_id: str
    type_name: str
    system: bool
    value: datetime


@datamap(module="attributes", flatten=True)
def get_date_attribute_with_module() -> DateAttribute:
    return {
        "id": "b0aa940d-61d9-4b83-94dc-1fd8f2b88dbb",
        "createdBy": "00000000-0000-0000-0000-000000900002",
        "createdOn": 1647520829437,
        "lastModifiedBy": "00000000-0000-0000-0000-000000900002",
        "lastModifiedOn": 1647520829438,
        "system": False,
        "resourceType": "DateAttribute",
        "type": {
            "id": "00000000-0000-0000-0000-000000000254",
            "resourceType": "DateAttributeType",
            "name": "Effective End Date",
        },
        "asset": {
            "id": "794d2c0b-efd2-446d-9c18-0be336fd61d9",
            "resourceType": "Asset",
            "name": "2022-03-17 #1",
        },
        "value": 1647648000000,
    }


@datamap(data_class=DateAttribute, flatten=True)
def get_date_attribute_with_dataclass() -> DateAttribute:
    return {
        "id": "b0aa940d-61d9-4b83-94dc-1fd8f2b88dbb",
        "createdBy": "00000000-0000-0000-0000-000000900002",
        "createdOn": 1647520829437,
        "lastModifiedBy": "00000000-0000-0000-0000-000000900002",
        "lastModifiedOn": 1647520829438,
        "system": False,
        "resourceType": "DateAttribute",
        "type": {
            "id": "00000000-0000-0000-0000-000000000254",
            "resourceType": "DateAttributeType",
            "name": "Effective End Date",
        },
        "asset": {
            "id": "794d2c0b-efd2-446d-9c18-0be336fd61d9",
            "resourceType": "Asset",
            "name": "2022-03-17 #1",
        },
        "value": 1647648000000,
    }
```

## Registering custom data type converter

By default, datamap comes with an int to datetime converter, but you can add custom data types converter if needed to the global converters dictionary in the datamap converters module.
Below you will find an example of a custom string to UUID converter, as for the id attribute of the User dataclass a UUID is required, we need the string from the json response to be converted to a UUID.

```python
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from datamap.converters import converters
from datamap.decorators import datamap


@dataclass
class User:
    id: UUID
    username: str
    name: str
    surname: str
    active: bool
    
    
def parse_uuid(value: Optional[str]) -> Optional[UUID]:
    if value:
        return UUID(value)
    return None


# as a key we concatenate the input with the output type joined by an underscore in lower case
# if the input type could be any value, then we just define the output type as a key
converters["str_uuid"] = parse_uuid


@datamap(data_class=User)
def get_user() -> User:
    return {
        "id": "b0aa940d-61d9-4b83-94dc-1fd8f2b88dbb",
        "username": "BKD7702",
        "name": "David",
        "surname": "Blain",
        "active": True,
    }
```

## Building from source

```bash
poetry build
poetry install
poetry publish -vvv -r artifactory -u USERNAME -p PASSWORD
```
