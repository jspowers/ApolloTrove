def get_value_mask(raw_value: str) -> str:
    if raw_value == None or len(raw_value) <= 1:
        return None
    elif len(raw_value) > 20:
        return raw_value[:4] + '.' * 8 + raw_value[-10:]
    elif len(raw_value) < 10:
        return 'x' * 4 + raw_value[-1:]
    else:
        return raw_value[:2] + '.' * 4 + raw_value[-4:]
