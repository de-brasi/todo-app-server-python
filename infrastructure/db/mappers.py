from typing import List

from infrastructure.db.storage.field_description import FieldDescription

from core.entities import TodoTask
from infrastructure.db.entities import TodoTaskCSVEntity


def to_domain(to_map: TodoTaskCSVEntity) -> TodoTask:
    result = TodoTask()

    to_map_data = to_map.data.split(',')
    assert len(to_map_data) == len(to_map.data_schema)

    for i in range(len(to_map.data_schema)):
        field = to_map.data_schema[i]
        result.__dict__[field.name] = field.type(to_map_data[i])

    return result


def to_db_entity(to_map: TodoTask, data_scheme: List[FieldDescription]) -> TodoTaskCSVEntity:
    # todo: make documentation

    """

    :param to_map:
    :param data_scheme:
    :return:
    """

    db_entity_data = ','.join(
        [str(to_map.__dict__[field_description.name]) for field_description in data_scheme])

    return TodoTaskCSVEntity(db_entity_data, data_scheme)

