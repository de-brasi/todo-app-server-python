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
    # todo:
    #  1) make closable for using in with-context;
    #  2) new layer for file's content manager (read from file, rstrip, etc.)

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
        with open(STORAGE_FILE_PATH, 'w') as storage_csv_file:
            for record in tasks_to_store:
                csv_entity = to_db_entity(record, CSV_DATA_SCHEME)
                storage_csv_file.write(csv_entity.data)


# todo: for debug
example = TasksRepositoryCSV()
res = example.get_tasks()
for i in res:
    print('todo task', i)
    print('rollback to TodoTaskCSVEntity', to_db_entity(i, CSV_DATA_SCHEME))

# 1,drink coffee,default,False,False
# 2,drink tea,default,True,True
# 3,drink beer,default,True,False
