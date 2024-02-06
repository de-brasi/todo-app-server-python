from dataclasses import dataclass


@dataclass
class TodoTask:
    task_id: int
    description: str
    group: str
    important: bool
    done: bool
