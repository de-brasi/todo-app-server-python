from typing import List
from core.entities import TodoTask


class TasksRepository:
    def get_tasks(self) -> List[TodoTask]:
        raise NotImplementedError

    def save_tasks(self, tasks_to_store: List[TodoTask]) -> None:
        raise NotImplementedError
