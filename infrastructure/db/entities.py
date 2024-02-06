from dataclasses import dataclass


@dataclass
class TodoTaskCSVEntity:
    data: str

    def get_data(self):
        return self.data
