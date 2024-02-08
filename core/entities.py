from dataclasses import dataclass


@dataclass
class TodoTask:
    id: int = -1
    label: str = 'no description'
    group: str = 'default'
    important: bool = False
    done: bool = False
