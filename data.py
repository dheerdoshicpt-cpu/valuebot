import os
import yaml
import pydantic

class Item(pydantic.BaseModel):
    """
    Pydantic model for Item Data
    """
    name: str
    value: str
    demand: str
    overpay: str

# TODO: make this a singleton and add caching
class Database:
    """
    This is a class for all things Data!
    """
    
    def _read_file(self, file_path):
        """
        Returns the Item objects with the given file_path, Raises:
        - FileNotFound Error when there is no item data
        - Validation Error when the data is in an unexpected format (fails to convert)
        """
        items: list[Item] = [] # Declare a temporary spot to hold the item data

        # Read file_path
        with open(file_path, "r") as f:
            file_data: dict = yaml.safe_load(f)
            
            # Convert the items
            for key, value in file_data.items():
                # Convert raw data into a format Pydantic understands
                reformatted_data = {"name": key}
                reformatted_data.update(value)

                # Unpack the dictonary into a pydantic model and add it to items
                items.append(Item(**reformatted_data))

        # Return a the item data 
        return items
        
    
    def __init__(self) -> None:
        self.items = []

        # Load data into items
        for file in os.listdir("./data"):
            if file.endswith(".yml"):
                self.items.extend(
                    self._read_file("./data/" + file)
                )

    def get_item(self, item_name: str) -> Item | None:
        """
        This is a HORRIFICALLY inefficent way of searching but.... its only a small database so... we dont care :D

        In all fairness i will probably revisit this when im not tired and implement a nicer system
        """
        
        # Search for our precious item
        for item in self.items:
            if item.name.lower() == item_name.lower():
                return item
        
        # If no items foundd
        return None


