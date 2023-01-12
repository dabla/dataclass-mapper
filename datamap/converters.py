import re
from copy import deepcopy
from dataclasses import Field
from functools import lru_cache
from itertools import chain
from typing import Iterable, Dict, Callable, Any, get_args, Optional

from more_itertools import flatten

from datamap.time import parse_timestamp


def identity(value: Optional[Any]) -> Optional[Any]:
    return value


converters: Dict[str, Callable[[Any], Any]] = {
    "int_datetime": parse_timestamp,
}


def converter_names(value: Any, attribute_type_names: Iterable[str]) -> Iterable[str]:
    return chain(
        map(
            lambda attribute_type_name: f"{type(value).__name__}_{attribute_type_name}".lower(),
            attribute_type_names,
        ),
        map(str.lower, attribute_type_names),
    )


def resolve_attribute_type_names(attribute: Field) -> Iterable[str]:
    if isinstance(attribute.type, str):
        return list(
            flatten(
                map(
                    lambda match: match.split(","),
                    iter(re.findall(r"\[(.*?)\]", attribute.type) or [attribute.type]),
                )
            )
        )
    attribute_types = filter(
        lambda attribute_type: hasattr(attribute_type, "__name__"),
        get_args(attribute.type),
    )
    return list(
        map(lambda attribute_type: attribute_type.__name__, attribute_types)
    ) or ([attribute.type.__name__] if hasattr(attribute.type, "__name__") else [])


@lru_cache(typed=True)
def resolve_converter(attribute: Field, value: Any) -> Callable[[Any], Any]:
    attribute_type_names = resolve_attribute_type_names(attribute)
    converter = next(
        filter(
            None,
            map(
                converters.get,
                converter_names(value, attribute_type_names),
            ),
        ),
        identity,
    )
    return converter


def convert_attributes(attributes: Iterable[Field], data: Dict) -> Dict:
    data = deepcopy(data)
    for attribute in attributes:
        if attribute.name in data:
            value = data.get(attribute.name)
            converter = resolve_converter(attribute, value)
            converted_value = converter(value)
            data[attribute.name] = converted_value
    return data
