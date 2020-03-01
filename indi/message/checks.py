def children(value, child_class):
    if value is None:
        return []
    return value


def dictionary(value, dictionary_class):
    if value not in dictionary_class.__dict__.values():
        raise Exception(
            f'Invalid value: "{value}" not found in {dictionary_class.__name__}'
        )
    return value
