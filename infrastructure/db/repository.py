import os

from typing import List

from core.entities import TodoTask
from core.repositories import TasksRepository

from infrastructure.db.entities import TodoTaskCSVEntity

from infrastructure.db.mappers import to_domain
from infrastructure.db.mappers import to_db_entity

from infrastructure.db.storage.data_schema import CSV_DATA_SCHEME

STORAGE_FILE_PATH = os.path.dirname(__file__) + '/storage/data.csv'


class TasksRepositoryCSV(TasksRepository):
    def get_tasks(self) -> List[TodoTask]:
        tasks = []

        with open(STORAGE_FILE_PATH) as storage_csv_file:
            for record in storage_csv_file.readlines():
                record = record.rstrip('\n')
                csv_entity = TodoTaskCSVEntity(record, CSV_DATA_SCHEME)
                todo_domain_entity = to_domain(csv_entity)
                tasks.append(todo_domain_entity)

        return tasks

    def save_tasks(self, tasks_to_store: List[TodoTask]) -> None:
        # todo: TodoTask[] -> CSVEntity[] -> csv file
        # todo: определиться с тем как записывать типы bool
        pass


example = TasksRepositoryCSV()
res = example.get_tasks()
for i in res:
    print(i)
