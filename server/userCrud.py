from sqlalchemy.orm import Session
from models import create_table_in_db, insert_item, get_items, update_item, delete_item

def create_table(session: Session, table_name: str, columns: dict):
    return create_table_in_db(session, table_name, columns)

def insert_item(session: Session, table_name: str, item: dict):
    insert_item(session, table_name, item)

def get_items(session: Session, table_name: str):
    return get_items(session, table_name)

def update_item(session: Session, table_name: str, item_id: int, item: dict):
    update_item(session, table_name, item_id, item)

def delete_item(session: Session, table_name: str, item_id: int):
    delete_item(session, table_name, item_id)
