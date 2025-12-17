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
        items = [] # Declare a temporary spot to hold the item data

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
        
    
    


