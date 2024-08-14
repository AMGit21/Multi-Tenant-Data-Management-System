from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class TableCreate(BaseModel):
    table_name: str
    columns: dict  # Columns with types as dict: {'column_name': 'column_type'}

class ItemCreate(BaseModel):
    item: dict  # Dynamic item fields

class ItemUpdate(BaseModel):
    item: dict  # Dynamic item fields
