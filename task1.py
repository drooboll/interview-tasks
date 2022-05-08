import re

checked_fields = {
    'naissance': r'[0-9]{4}',
    'date': r'\d{4}',
    'taille': r'[0-9]{2,3}cm',
    'yeux': r'[a-z]+',
    'numero': r'[0-9]+',
    'pays': r'[0-9]+',
}

optional_fields = {'pays'}
required_fields = set(checked_fields.keys()) - optional_fields
forbidden = checked_fields.keys()


def get_string_records():
    """
    Reads input passports file.
    :return: list of string passport records
    """
    file = open('passeports.txt', 'r')
    content = file.read()

    return content.strip().split('\n\n')


def is_field_valid(field, record):
    """
    Check if defined field is valid in record
    :param record: string representation of passport
    :param field: field name for checking. Key and value are :-separated
    :return: validity of record
    """
    # Case of repetition
    if record.count(field) > 1:
        return False

    # Check if field is present only once as field name
    if f'{field}:' not in record:
        return field in optional_fields

    # If field is present, it's key-value should be valid
    match = re.search(rf'{field}:{checked_fields[field]}', record)

    if match is None:
        return False

    field_value = match.group(0).split(':')[1]

    if field_value in forbidden:
        return False

    return True


if __name__ == '__main__':
    records = get_string_records()

    invalid_count = 0

    for record in records:
        fields_count = record.count(':')

        # If there're not enough fields or multiple field occurrence,
        # then record is definitely broken and there's no need to check the fields
        if fields_count > len(checked_fields) or fields_count < len(required_fields):
            invalid_count += 1
            continue

        for field in checked_fields:
            if not is_field_valid(field, record):
                invalid_count += 1
                break

    print('Valid records:', len(records) - invalid_count)
