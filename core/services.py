import sys
import json

from core.entities import TodoTask
from core.repositories import TasksRepository


class MainService:
    def __init__(self, storage: TasksRepository):
        self.storage = storage

    @staticmethod
    def task_entity_to_dict_mapper(arg: TodoTask) -> dict:
        res = {
            'id': arg.id,
            'label': arg.label,
            'group': arg.group,
            'important': arg.important,
            'done': arg.done
        }
        return res

    @staticmethod
    def task_entity_to_todo_task_mapper(arg: dict) -> TodoTask:
        return TodoTask(
            id=arg['id'],
            label=arg['label'],
            group=arg['group'],
            important=arg['important'],
            done=arg['done']
        )

    def get_tasks_from_db(self) -> str:
        tasks = self.storage.get_tasks()
        tasks_as_dicts = []
        for todo in tasks:
            tasks_as_dicts.append(MainService.task_entity_to_dict_mapper(todo))

        result = json.dumps(tasks_as_dicts)
        return result

    def save_tasks_to_db(self, to_save: str):
        try:
            tasks = json.loads(to_save)

            tasks_as_entity = []
            for todo in tasks:
                assert isinstance(todo, dict)
                tasks_as_entity.append(MainService.task_entity_to_todo_task_mapper(todo))

            print("got tasks from client:" + str(tasks_as_entity) + '\n')
            self.storage.save_tasks(tasks_as_entity)
        except json.JSONDecodeError:
            sys.stderr.write("decoding error when decode string:" + str(to_save) + '\n')
            raise RuntimeError("internal error")
        except AssertionError:
            sys.stderr.write("assertion error when decode string:" + str(to_save) + "; expected encoded list od dicts\n")
            raise RuntimeError("internal error")
