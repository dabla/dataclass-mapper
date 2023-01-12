from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import tests
from datamapper.decorators import datamap


@dataclass
class DateAttribute:
    id: str
    created_by: str
    asset_id: str
    asset_name: Optional[str]
    type_name: str
    system: bool
    value: datetime
    created_on: datetime = datetime.now()


@datamap(module="tests.unit.fixtures.date_attributes", flatten=True)
def get_date_attribute():
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
