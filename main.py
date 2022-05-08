import re

checked_fields = {
    'naissance': r'[0-9]{4}',
    'date': r'\d{4}',
    'taille': r'[0-9]{2,3}cm',
    'yeux': r'[a-z]*',
    'numero': r'[0-9]*',
    'pays': r'[0-9]*',
}

optional_fields = {'pays'}
required_fields = set(checked_fields.keys()) - optional_fields
forbidden = checked_fields.keys()


def get_string_records():
    file = open('passeports.txt', 'r')
    content = file.read()

    return content.strip().split('\n\n')

records = get_string_records()
defect_count = 0

for record in records:
    fields_count = record.count(':')

    # If there're not enough fields or multiple field occurrence,
    # then record is definitely broken and there's no need to check the fields
    if fields_count > len(checked_fields) or fields_count < len(required_fields):
        defect_count += 1
        continue

    last_defect = defect_count

    for field in checked_fields:
        # Case of repetition
        if record.count(field) > 1:
            defect_count += 1
            break

        # Check if field is present only once as field name
        if record.count(f'{field}:') != 1 and field not in optional_fields:
            defect_count += 1
            break

        match = re.search(rf'{field}:{checked_fields[field]}', record)

        if match is None:
            if field in optional_fields:
                continue

            defect_count += 1
            break

        field_value = match.group(0).split(':')[1]

        # Only literal-value fields are checked here (in fact, only yeux)
        if field_value in forbidden:
            defect_count += 1
            break

print('Valid records:', len(records) - defect_count)
