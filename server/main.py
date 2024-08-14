from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from adminUtils import (
    create_postgresql_container, 
    init_main_db,
    save_user_to_db,
)
from schemas import UserCreate
from database import add_database
from user_routes import router as user_router
from db_routes import app as db_app

app = FastAPI()

# Define the origins that should be allowed to make requests
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_main_db()

# app.include_router(user_router, prefix="/users")
app.mount("/db", db_app)
# app.include_router(db_router, prefix="/db")

@app.post("/register")
def register_user(user: UserCreate):
    """
    Register a new user by creating a PostgreSQL container for them and
    saving their details to the main database.

    Parameters:
    - user: The user details including username and password.

    Returns:
    - A message indicating successful registration.
    """
    container, container_hostname, port,  = create_postgresql_container(user)
    
    save_user_to_db(user, container.id, container_hostname, port)
    # Construct the database URL
    # database_url = f"postgresql://{user.username}:{user.password}@{container_hostname}/{user.username}"
    # print(f"db url: {database_url}")
    # # Add the user's database connection to the DATABASES dictionary
    # add_database(user.username, database_url)

    return {"message": f"User '{user.username}' registered successfully."}

# ------------------------------------------------------------------------------
# This is a one function to perform multiple tasks on the database
# ------------------------------------------------------------------------------
#  @app.post("/users/{username}/managedb")
# async def create_user_table(username: str, request: Request):
#     container_name = f"postgres_{username}"
#     client = docker.from_env()

#     try:
#         # Parse the JSON request body to get the SQL command and database name
#         request_data = await request.json()
#         sql_query = request_data.get("query")
#         db_name = username # request_data.get("database")

#         if not sql_query:
#             raise HTTPException(status_code=400, detail="No SQL query provided.")
#         if not db_name:
#             raise HTTPException(status_code=400, detail="No database name provided.")

#         # Get the container and execute the SQL query using psql
#         container = client.containers.get(container_name)
#         exec_result = container.exec_run(f"psql -U {username} -d {db_name} -c \"{sql_query}\"")

#         if exec_result.exit_code == 0:
#             return {"message": "Query executed successfully."}
#         else:
#             return {
#                 "message": "Failed to execute query.",
#                 "error": exec_result.output.decode('utf-8')
#             }
#     except docker.errors.NotFound:
#         raise HTTPException(status_code=404, detail=f"Container {container_name} not found.")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)