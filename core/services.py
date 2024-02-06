import json

from core.entities import TodoTask
from core.repositories import TasksRepository


def task_entity_to_dict_mapper(arg: TodoTask) -> dict:
    res = {
        'task_id': arg.task_id,
        'description': arg.description,
        'group': arg.group,
        'important': arg.important,
        'done': arg.done
    }
    return res


def task_entity_to_todo_task_mapper(arg: dict) -> TodoTask:
    return TodoTask(
        task_id=arg['task_id'],
        description=arg['description'],
        group=arg['group'],
        important=arg['important'],
        done=arg['done']
    )


def get_tasks_from_db(storage: TasksRepository) -> str:
    tasks = storage.get_tasks()
    print("got tasks from db:", tasks)
    tasks_as_dicts = []
    for todo in tasks:
        tasks_as_dicts.append(task_entity_to_dict_mapper(todo))

    result = json.dumps(tasks_as_dicts)
    return result


def save_tasks_to_db(storage: TasksRepository, to_save: str):
    try:
        tasks = json.loads(to_save)

        tasks_as_entity = []
        for todo in tasks:
            assert isinstance(todo, dict)
            tasks_as_entity.append(task_entity_to_todo_task_mapper(todo))

        print("got tasks from client:", tasks_as_entity)

        storage.save_tasks(tasks_as_entity)
    except json.JSONDecodeError as e:
        print("decoding error when decode string:", to_save)
        raise RuntimeError("internal error")
    except AssertionError:
        print("assertion error when decode string:", to_save, "; expected encoded list od dicts")
        raise RuntimeError("internal error")
