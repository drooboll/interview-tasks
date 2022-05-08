import re
from datetime import datetime

checked_numbers = []

checked_fields = {
    'naissance': r'\d{2}/\d{2}/\d{4}',
    'date': r'\d{2}/\d{2}/\d{4}',
    'taille': r'\d{2,3}cm',
    'yeux': r'[a-z]+',
    'numero': r'\d+',
    'pays': r'[A-Za-z]+',
}


def is_date_valid(date_string, limit_date=datetime.strptime("01/03/2020", "%d/%m/%Y")):
    try:
        date = datetime.strptime(date_string, "%d/%m/%Y")
        return limit_date >= date
    except ValueError:
        return False


def is_passport_number_valid(number_string):
    global checked_numbers

    number = int(number_string)
    if number in checked_numbers:
        return False

    checked_numbers.append(number)
    return True


def is_color_valid(color):
    return color in {'marron', 'bleu', 'vert', 'gris'}


fields_verification = {
    'date': is_date_valid,
    'numero': is_passport_number_valid,
    'yeux': is_color_valid
}

optional_fields = {'pays'}
required_fields = set(checked_fields.keys()) - optional_fields
forbidden = checked_fields.keys()


def get_string_records():
    """
    Reads input passports file.
    :return: list of string passport records
    """
    file = open('passeports2.txt', 'r')
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

    # Check if field is presented only once as field name
    if f'{field}:' not in record:
        return field in optional_fields

    # If field is present, it's key-value should be valid
    match = re.search(rf'{field}:{checked_fields[field]}', record)

    if match is None:
        return False

    field_value = match.group(0).split(':')[1]

    if field_value in forbidden:
        return False

    # Additional verification for certain fields
    if field in fields_verification:
        return fields_verification[field](field_value)

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
