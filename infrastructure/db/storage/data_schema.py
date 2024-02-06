from infrastructure.db.storage.field_description import FieldDescription

CSV_DATA_SCHEME = [
    FieldDescription('task_id', int),
    FieldDescription('description', str),
    FieldDescription('group', str),
    FieldDescription('important',
                     lambda x: True if x == 'true' or x == 'true\n' else False),
    FieldDescription('done',
                     lambda x: True if x == 'true' or x == 'true\n' else False)
]
