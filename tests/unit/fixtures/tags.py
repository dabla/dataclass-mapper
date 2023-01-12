from dataclasses import dataclass
from typing import Any, Optional, Dict

from datamapper.decorators import datamap, rename_dict_keys, remove_dict_keys


@dataclass
class Tag:
    id: int
    tag: str
    filter: str
    color_code: str
    is_smart_tag: bool = False
    is_visible: bool = False
    is_category_model_tag: Optional[Any] = None


@datamap(Tag, rename=[("is_smarttag", "is_smart_tag"), ("visible", "is_visible")], remove=["category_model_tag"])
def get_tags():
    return iter([[{"tag": "(LANGUAGE)",
                   "id": 35792,
                   "is_smarttag": False,
                   "color_code": "rgb(83,146,255)",
                   "filter": "usertag:\"(LANGUAGE)\"",
                   "visible": True,
                   "category_model_tag": False
                   },
                  {"tag": "2019 We Are Infrabel - Wave 1",
                   "id": 7956854,
                   "parent_id": 7956853,
                   "is_smarttag": False,
                   "color_code": "rgb(250,163,56)",
                   "filter": "usertag:\"2019 We Are Infrabel - Wave 1\"",
                   "visible": False,
                   "category_model_tag": False
                   }],
                 [{"tag": "3ième voie Bruges-Dudzele",
                   "id": 4557288,
                   "is_smarttag": False,
                   "color_code": "rgb(201,78,157)",
                   "filter": "usertag:\"3ième voie Bruges-Dudzele\"",
                   "visible": False,
                   "category_model_tag": False
                   },
                  {"tag": "_Info Search",
                   "id": 300976,
                   "parent_id": 7956853,
                   "is_smarttag": False,
                   "color_code": "rgb(122,140,64)",
                   "filter": "usertag:\"_Info Search\"",
                   "visible": False,
                   "category_model_tag": False
                   }],
                 ])


@remove_dict_keys("category_model_tag")
@rename_dict_keys(("is_smarttag", "is_smart_tag"), ("visible", "is_visible"))
def validate_tag(data: Dict, validate: bool) -> Dict:
    if validate:
        assert data
    return data


@remove_dict_keys("category_model_tag")
@rename_dict_keys(("is_smarttag", "is_smart_tag"), ("visible", "is_visible"))
def get_tag() -> Dict:
    return {"tag": "(LANGUAGE)",
            "id": 35792,
            "is_smarttag": False,
            "color_code": "rgb(83,146,255)",
            "filter": "usertag:\"(LANGUAGE)\"",
            "visible": True,
            "category_model_tag": False
            }
