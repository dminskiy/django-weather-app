def intstr2bool(value) -> bool:
    value = int(value)
    assert value in [
        0,
        1,
    ], f"Input string cound not be converted to either 0 or 1. Received: {value}"
    return bool(value)
