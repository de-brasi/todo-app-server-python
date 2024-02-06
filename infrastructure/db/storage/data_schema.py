from infrastructure.db.storage.field_description import FieldDescription

CSV_DATA_SCHEME = [
    FieldDescription('task_id', int),
    FieldDescription('description', str),
    FieldDescription('group', str),
    FieldDescription('important', bool),
    FieldDescription('done', bool)
]
