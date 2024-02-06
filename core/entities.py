from dataclasses import dataclass


@dataclass
class TodoTask:
    task_id: int = -1
    description: str = 'no description'
    group: str = 'default'
    important: bool = False
    done: bool = False
