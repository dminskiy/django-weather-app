from typing import List, Optional

from utils.utils import (
    check_required_fields,
    check_unexpected_fields,
    unpack_request_data,
)


def check_request_fields(
    required_fields: List[str], optional_fields: Optional[List[str]] = None
):
    def decorator(func):
        def wrapper(request):
            request_dict = unpack_request_data(request)
            check_required_fields(
                required_fields=required_fields, input_fields=request_dict
            )
            if optional_fields:
                check_unexpected_fields(
                    optional_fields=optional_fields,
                    required_fields=required_fields,
                    input_fields=request_dict,
                )
            return func(request)

        return wrapper

    return decorator
