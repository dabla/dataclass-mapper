from functools import wraps
from typing import Type, Optional, Tuple, Sequence, Dict

from datamap.dicts import from_dicts, T, rename_keys, remove_keys


def datamap(
    data_class: Optional[Type[T]] = None,
    data_class_type_key: Optional[str] = None,
    module: Optional[str] = None,
    flatten: bool = False,
    rename: Sequence[Tuple[str]] = [],
    remove: Sequence[str] = [],
):
    def decorator(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            data = method(*args, **kwargs)
            return from_dicts(
                data=data,
                data_class=data_class,
                data_class_type_key=data_class_type_key,
                module=module,
                flatten=flatten,
                rename=rename,
                remove=remove,
            )

        return wrapper

    return decorator


def rename_dict_keys(*key_mappings):
    def decorator(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            if args:
                updated_args = []
                for arg in args:
                    updated_args.append(
                        rename_keys(arg, *key_mappings)
                        if isinstance(arg, Dict)
                        else arg
                    )
                return method(*tuple(updated_args), **kwargs)
            data = method(*args, **kwargs)
            if isinstance(data, Dict):
                return rename_keys(data, *key_mappings)
            return data

        return wrapper

    return decorator


def remove_dict_keys(*keys_to_remove):
    def decorator(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            if args:
                updated_args = []
                for arg in args:
                    updated_args.append(
                        remove_keys(arg, *keys_to_remove)
                        if isinstance(arg, Dict)
                        else arg
                    )
                return method(*tuple(updated_args), **kwargs)
            data = method(*args, **kwargs)
            if isinstance(data, Dict):
                return remove_keys(data, *keys_to_remove)
            return data

        return wrapper

    return decorator
