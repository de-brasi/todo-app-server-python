from typing import List
from abc import ABC
from abc import abstractmethod

from core.entities import TodoTask


class TasksRepository(ABC):
    @abstractmethod
    def get_tasks(self) -> List[TodoTask]:
        pass

    @abstractmethod
    def save_tasks(self, tasks_to_store: List[TodoTask]) -> None:
        pass
