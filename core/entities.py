from dataclasses import dataclass


@dataclass
class TodoTask:
    task_id: int         # todo: как организовать выбор уникальных id для новых задач в проекте?
    description: str
    group: str
    important: bool
    done: bool
