from typing import Union
from deepmerge import always_merger as merger


def success(operation: str, model: str, data: Union[list[dict], dict], **kwargs):
    defaults = {
        "status": 200,
        "message": f"{operation} {model} successful",
        "message-key": f"{operation}-{model}",
        "data": data,
    }

    return merger.merge(defaults, kwargs)


def bad_request(operation: str, model: str, **kwargs):
    defaults = {
        "status": 400,
        "message": f"{operation} {model} failed",
        "message-key": f"{operation}-{model}",
        "data": None,
    }

    return merger.merge(defaults, kwargs)
