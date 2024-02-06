from dataclasses import dataclass


@dataclass
class TodoTask:
    id: int         # todo: как организовать выбор уникальных id для новых задач в проекте?
    description: str
    group: str
    important: bool
    done: bool
