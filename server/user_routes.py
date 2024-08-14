from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import DATABASE_POOLS, get_session
from userCrud import create_table, insert_item, get_items, update_item, delete_item
from schemas import TableCreate, ItemCreate, ItemUpdate
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

router = APIRouter()

def get_db_session(username: str) -> Session:
    # Fetch the database URL for the username
    if username in DATABASE_POOLS:
        database_url = DATABASE_POOLS[username]["database_url"]
    else:
        raise HTTPException(status_code=404, detail=f"Database for user '{username}' not found.")
    
    return get_session(username, database_url)


@router.get("/{username}/test_connection")
def test_connection(username: str, session: Session = Depends(get_db_session)):
    """
    Test the connectivity to the user's database by executing a simple query.

    Parameters:
    - username: The username of the user whose database to test.

    Returns:
    - A message indicating whether the connection was successful.
    """
    try:
        # Execute a simple query to test the connection
        result = session.execute(text("SELECT 1"))
        # Commit if the connection is successful
        session.commit()
        return {"message": f"Connection to database for user '{username}' is successful."}
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")
    
@router.post("/{username}/create_table")
def create_table_endpoint(username: str, table: TableCreate, db: Session = Depends(get_db_session)):
    try:
        create_table(db, table.table_name, table.columns)
        return {"message": f"Table {table.table_name} created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{username}/insert_item")
def insert_item_endpoint(username: str, table_name: str, item: ItemCreate, db: Session = Depends(get_db_session)):
    try:
        insert_item(db, table_name, item.item)
        return {"message": f"Item inserted successfully into table '{table_name}'"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{username}/get_items")
def get_items_endpoint(username: str, table_name: str, db: Session = Depends(get_db_session)):
    try:
        items = get_items(db, table_name)
        return {"items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{username}/update_item/{item_id}")
def update_item_endpoint(username: str, table_name: str, item_id: int, item: ItemUpdate, db: Session = Depends(get_db_session)):
    try:
        update_item(db, table_name, item_id, item.item)
        return {"message": f"Item with ID {item_id} updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{username}/delete_item/{item_id}")
def delete_item_endpoint(username: str, table_name: str, item_id: int, db: Session = Depends(get_db_session)):
    try:
        delete_item(db, table_name, item_id)
        return {"message": f"Item with ID {item_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/test")
def test_endpoint():
    return {"message": "Test endpoint is working"}
