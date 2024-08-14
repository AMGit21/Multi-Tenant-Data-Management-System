from sqlalchemy import Table, Column, Integer, String, Float, Boolean, MetaData, text
from sqlalchemy.orm import Session
from typing import Dict

# Mapping of string type names to SQLAlchemy types
type_mapping = {
    "String": String,
    "Integer": Integer,
    "Float": Float,
    "Boolean": Boolean,
    # Add more types as needed
}

metadata = MetaData()

def create_table(metadata: MetaData, table_name: str, columns: Dict[str, str]) -> Table:
    """
    Create a dynamic table based on the provided columns.

    Parameters:
    - metadata: SQLAlchemy MetaData instance.
    - table_name: The name of the table to create.
    - columns: A dictionary where keys are column names and values are SQLAlchemy column type names as strings.

    Returns:
    - An SQLAlchemy Table instance.
    """
    # Convert column type names to SQLAlchemy types using type_mapping
    sql_columns = []
    for column_name, column_type_name in columns.items():
        if column_type_name in type_mapping:
            sql_columns.append(Column(column_name, type_mapping[column_type_name]))
        else:
            raise ValueError(f"Unsupported column type: {column_type_name}")

    # Add an 'id' column as the primary key
    sql_columns.append(Column('id', Integer, primary_key=True, index=True))

    # Create and return the Table object
    return Table(table_name, metadata, *sql_columns)

def create_table_in_db(session: Session, table_name: str, columns: Dict[str, str]) -> Dict[str, str]:
    """
    Dynamically create a table in the database.

    Parameters:
    - session: SQLAlchemy Session instance.
    - table_name: The name of the table to create.
    - columns: A dictionary where keys are column names and values are SQLAlchemy column type names as strings.

    Returns:
    - A message indicating the success of the table creation.
    """
    table = create_table(metadata, table_name, columns)
    metadata.create_all(bind=session.bind)
    return {"message": f"Table {table_name} created successfully"}

def insert_item(session: Session, table_name: str, item: Dict[str, any]) -> None:
    """
    Insert a new item into the specified table.

    Parameters:
    - session: SQLAlchemy Session instance.
    - table_name: The name of the table to insert the item into.
    - item: A dictionary representing the item to insert.

    Returns:
    - None
    """
    columns = ', '.join(item.keys())
    values = ', '.join(f":{key}" for key in item.keys())
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
    session.execute(text(query), item)
    session.commit()

def get_items(session: Session, table_name: str) -> list:
    """
    Retrieve all items from the specified table.

    Parameters:
    - session: SQLAlchemy Session instance.
    - table_name: The name of the table to retrieve items from.

    Returns:
    - A list of items (rows) from the table.
    """
    query = f"SELECT * FROM {table_name}"
    result = session.execute(text(query))
    return result.fetchall()

def update_item(session: Session, table_name: str, item_id: int, item: Dict[str, any]) -> None:
    """
    Update an item in the specified table.

    Parameters:
    - session: SQLAlchemy Session instance.
    - table_name: The name of the table to update the item in.
    - item_id: The ID of the item to update.
    - item: A dictionary representing the new values for the item.

    Returns:
    - None
    """
    columns = ', '.join(f"{key} = :{key}" for key in item.keys())
    query = f"UPDATE {table_name} SET {columns} WHERE id = :id"
    item['id'] = item_id
    session.execute(text(query), item)
    session.commit()

def delete_item(session: Session, table_name: str, item_id: int) -> None:
    """
    Delete an item from the specified table.

    Parameters:
    - session: SQLAlchemy Session instance.
    - table_name: The name of the table to delete the item from.
    - item_id: The ID of the item to delete.

    Returns:
    - None
    """
    query = f"DELETE FROM {table_name} WHERE id = :id"
    session.execute(text(query), {"id": item_id})
    session.commit()
