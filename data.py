

import os
import yaml
import pydantic
from typing import Dict, List


class Item(pydantic.BaseModel):
    """
    Pydantic model for Item Data
    """
    name: str
    value: str
    demand: str
    overpay: str


class Database:
    """
    This is a class for all things Data!
    Singleton + caching
    """

    _instance = None
    _file_cache: Dict[str, List[Item]] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def _read_file(self, file_path: str) -> List[Item]:
        """
        Returns the Item objects with the given file_path
        Uses caching to avoid rereading files
        """

        # ✅ Return cached data if present
        if file_path in self._file_cache:
            return self._file_cache[file_path]

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} does not exist")

        items: List[Item] = []

        with open(file_path, "r") as f:
            file_data: dict = yaml.safe_load(f) or {}

            for key, value in file_data.items():
                reformatted_data = {"name": key}
                reformatted_data.update(value)

                items.append(Item(**reformatted_data))

        # ✅ Cache result
        self._file_cache[file_path] = items
        return items

    def __init__(self) -> None:
        # Prevent re-initialization (important for singleton)
        if hasattr(self, "_initialized"):
            return

        self.items: List[Item] = []

        for file in os.listdir("./data"):
            if file.endswith((".yml", ".yaml")):
                self.items.extend(
                    self._read_file(os.path.join("./data", file))
                )

        self._initialized = True

    def get_item(self, item_name: str) -> Item | None:
        """
        Inefficient linear search, acceptable for small datasets
        """

        for item in self.items:
            if item.name.lower() == item_name.lower():
                return item

        return None

    def clear_cache(self):
        """
        Clears cached files (useful for dev / reloads)
        """
        self._file_cache.clear()