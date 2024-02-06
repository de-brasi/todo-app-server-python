from typing import List
from core.entities import TodoTask


class TasksRepository:
    def get_tasks(self):
        raise NotImplementedError

    def save_tasks(self, tasks_to_store: List[TodoTask]):
        raise NotImplementedError
