import json
from django.http.request import RawPostDataException


def intstr2bool(value) -> bool:
    value = int(value)
    assert value in [
        0,
        1,
    ], f"Input string cound not be converted to either 0 or 1. Received: {value}"
    return bool(value)


def unpack_request_data(request) -> dict:
    try:
        return json.loads(request.body)
    except RawPostDataException:
        return request.data


def check_required_fields(required_fields: list, input_fields: dict):
    for field in required_fields:
        assert input_fields[field] is not None, f"{field} field is required as input."


def check_unexpected_fields(
    required_fields: list, optional_fields: list, input_fields: dict
):
    for field in input_fields:
        assert (field in required_fields) or (field in optional_fields), (
            f"Unexpected field: {field}.Required fields: {required_fields}."
            f"\nOptional fields: {optional_fields}"
        )
