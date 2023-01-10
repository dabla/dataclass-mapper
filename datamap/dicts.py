import logging
from abc import ABCMeta, abstractmethod
from collections.abc import Collection
from copy import deepcopy
from dataclasses import fields
from types import ModuleType
from typing import (
    Dict,
    MutableMapping,
    Type,
    Union,
    List,
    Optional,
    TypeVar,
    Tuple,
    Any,
    Iterable,
    Sequence,
)

import dacite
from inflector import Inflector

from datamap.converters import convert_attributes


def pep8_compliant_keys(value: Dict, inflector: Inflector = Inflector()) -> Dict:
    return {inflector.underscore(key): value for key, value in value.items()}


class KeyMergerStrategy(metaclass=ABCMeta):
    @abstractmethod
    def apply(self, parent_key: str, key: str) -> str:
        pass


class DefaultKeyMergerStrategy(KeyMergerStrategy):
    def __init__(self):
        self._inflector = Inflector()

    def apply(self, parent_key: Optional[str], key: str) -> str:
        if parent_key:
            return f"{parent_key}{self._inflector.camelize(key)}"
        return key


def flatten_dict(
    records: MutableMapping[Any, Any],
    parent_key: Optional[str] = None,
    key_merger=DefaultKeyMergerStrategy(),
) -> Dict:
    items: List[Tuple[Any, Any]] = []
    for key, value in records.items():
        new_key = key_merger.apply(parent_key, key)
        if isinstance(value, MutableMapping):
            items.extend(flatten_dict(value, new_key, key_merger=key_merger).items())
        else:
            items.append((new_key, value))
    return dict(items)


T = TypeVar("T")


def from_dict(
    data: Dict,
    data_class: Optional[Type[T]] = None,
    data_class_type_key: Optional[str] = None,
    module: Optional[Union[str, ModuleType]] = None,
    flatten: bool = False,
    rename: Sequence[Tuple[str]] = [],
    remove: Sequence[str] = [],
) -> Union[Dict, T]:
    if data:
        if not isinstance(data, Dict):
            raise AttributeError(
                f"Invalid argument type {type(data).__name__} passed as data, expected a dict!"
            )
        if flatten is True:
            data = flatten_dict(data)
        data = pep8_compliant_keys(data)
        data = rename_keys(data, *rename)
        data = remove_keys(data, *remove)
        data_class = resolve_data_class(data, data_class, data_class_type_key, module)
        if data_class:
            attributes = fields(data_class)
            data = convert_attributes(attributes, data)
            return dacite.from_dict(data_class=data_class, data=data)
    return data


def resolve_data_class(
    data: Dict,
    data_class: Optional[Type[T]] = None,
    data_class_type_key: Optional[str] = None,
    module: Optional[Union[str, ModuleType]] = None,
) -> Optional[Type[T]]:
    if data_class is None and module is not None:
        data_class_name = data.get(
            data_class_type_key if data_class_type_key else "resource_type"
        )
        if data_class_name:
            try:
                if isinstance(module, str):
                    data_class = getattr(
                        __import__(module, fromlist=[data_class_name]), data_class_name
                    )
                else:
                    data_class = getattr(module, data_class_name)
            except AttributeError as e:
                logging.warning(e)
    return data_class


def from_iterable(
    data: Union[Dict, List[Dict]],
    data_class: Optional[Type] = None,
    data_class_type_key: Optional[str] = None,
    module: Optional[Union[str, ModuleType]] = None,
    flatten: bool = False,
    rename: Sequence[Tuple[str]] = [],
    remove: Sequence[str] = [],
):
    if isinstance(data, Iterable) and not isinstance(data, Collection):
        return map(
            lambda row: from_dicts(
                data=row,
                data_class=data_class,
                data_class_type_key=data_class_type_key,
                module=module,
                flatten=flatten,
                rename=rename,
                remove=remove,
            ),
            data,
        )
    raise AttributeError(
        f"Invalid argument type {type(data).__name__} passed as data, "
        "expected an iterable which isn't a collection!"
    )


def from_collection(
    data: Union[Dict, List[Dict]],
    data_class: Optional[Type] = None,
    data_class_type_key: Optional[str] = None,
    module: Optional[Union[str, ModuleType]] = None,
    flatten: bool = False,
    rename: Sequence[Tuple[str]] = [],
    remove: Sequence[str] = [],
):
    if isinstance(data, Collection) and not isinstance(data, Dict):
        return list(
            map(
                lambda row: from_dict(
                    data=row,
                    data_class=data_class,
                    data_class_type_key=data_class_type_key,
                    module=module,
                    flatten=flatten,
                    rename=rename,
                    remove=remove,
                ),
                data,
            )
        )
    raise AttributeError(
        f"Invalid argument type {type(data).__name__} passed as data, expected a collection!"
    )


def from_dicts(
    data: Union[Dict, List[Dict]],
    data_class: Optional[Type] = None,
    data_class_type_key: Optional[str] = None,
    module: Optional[Union[str, ModuleType]] = None,
    flatten: bool = False,
    rename: Sequence[Tuple[str]] = [],
    remove: Sequence[str] = [],
) -> Union[Dict, T, Iterable[Dict], List[T]]:
    if isinstance(data, Iterable) and not isinstance(data, Collection):
        return from_iterable(
            data=data,
            data_class=data_class,
            data_class_type_key=data_class_type_key,
            module=module,
            flatten=flatten,
            rename=rename,
            remove=remove,
        )
    if isinstance(data, Collection) and not isinstance(data, Dict):
        return from_collection(
            data=data,
            data_class=data_class,
            data_class_type_key=data_class_type_key,
            module=module,
            flatten=flatten,
            rename=rename,
            remove=remove,
        )
    return from_dict(
        data=data,
        data_class=data_class,
        data_class_type_key=data_class_type_key,
        module=module,
        flatten=flatten,
        rename=rename,
        remove=remove,
    )


def rename_keys(data: Dict, *key_mappings, **kwargs) -> Dict:
    if data:
        if not isinstance(data, Dict):
            raise AttributeError(
                f"Invalid argument type {type(data).__name__} passed as data, expected a dict!"
            )
        suppress = kwargs.get("suppress_none", False)
        if key_mappings:
            data = deepcopy(data)
            for old_key, new_key in key_mappings:
                value = data.pop(old_key, None)
                if value or not suppress:
                    data[new_key] = value
    return data


def remove_keys(data: Dict, *keys_to_remove: str) -> Dict:
    if data and keys_to_remove:
        if not isinstance(data, Dict):
            raise AttributeError(
                f"Invalid argument type {type(data).__name__} passed as data, expected a dict!"
            )
        return {
            key: value for key, value in data.items() if key not in set(keys_to_remove)
        }
    return data
