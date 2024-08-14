from fastapi import FastAPI, HTTPException, Request
import docker

app = FastAPI()

# Helper function to get Docker container
def get_docker_container(username: str):
    container_name = f"postgres_{username}"
    client = docker.from_env()
    try:
        return client.containers.get(container_name)
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail=f"Container {container_name} not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Helper function to execute SQL queries
def execute_sql(container, sql_query: str, username: str, db_name: str):
    try:
        exec_result = container.exec_run(f"psql -U {username} -d {db_name} -c \"{sql_query}\"")
        if exec_result.exit_code == 0:
            return exec_result.output.decode('utf-8')
        else:
            raise HTTPException(status_code=400, detail=exec_result.output.decode('utf-8'))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Endpoint to list all tables
@app.get("/users/{username}/tables")
async def list_tables(username: str):
    container = get_docker_container(username)
    sql_query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';"
    result = execute_sql(container, sql_query, username, username)

    # Process the result to return only the table names, excluding "table_name" and "(x rows)"
    lines = result.split('\n')
    table_names = [line.strip() for line in lines if line.strip() and not line.startswith('table_name') and not line.startswith('-') and not line.endswith('rows)')]

    # Remove the "table_name" header if it exists
    if "table_name" in table_names:
        table_names.remove("table_name")

    return {"message": "Tables retrieved successfully.", "tables": table_names}

# Endpoint to get data from a specific table
@app.get("/users/{username}/tables/{table_name}")
async def get_table_data(username: str, table_name: str):
    container = get_docker_container(username)
    sql_query = f"SELECT * FROM {table_name};"
    result = execute_sql(container, sql_query, username, username)
    return {"message": f"Data from {table_name} retrieved successfully.", "data": result}

# Endpoint to create a new table
@app.post("/users/{username}/tables")
async def create_table(username: str, request: Request):
    request_data = await request.json()
    sql_query = request_data.get("sql_query")
    if not sql_query:
        raise HTTPException(status_code=400, detail="SQL query for table creation is required.")
    
    container = get_docker_container(username)
    result = execute_sql(container, sql_query, username, username)
    return {"message": "Table created successfully.", "result": result}

# Endpoint to delete a table
@app.delete("/users/{username}/tables/{table_name}")
async def delete_table(username: str, table_name: str):
    container = get_docker_container(username)
    sql_query = f"DROP TABLE IF EXISTS {table_name};"
    result = execute_sql(container, sql_query, username, username)
    return {"message": f"Table {table_name} deleted successfully.", "result": result}

# Endpoint to update data in a table
@app.put("/users/{username}/tables/{table_name}")
async def update_table_data(username: str, table_name: str, request: Request):
    request_data = await request.json()
    sql_query = request_data.get("sql_query")
    if not sql_query:
        raise HTTPException(status_code=400, detail="SQL query for updating table data is required.")
    
    container = get_docker_container(username)
    result = execute_sql(container, sql_query, username, username)
    return {"message": f"Table {table_name} updated successfully.", "result": result}

# Endpoint to modify table structure (add/remove columns, change data type, add constraints, etc.)
@app.patch("/users/{username}/tables/{table_name}/structure")
async def modify_table_structure(username: str, table_name: str, request: Request):
    request_data = await request.json()
    sql_query = request_data.get("sql_query")
    if not sql_query:
        raise HTTPException(status_code=400, detail="SQL query for modifying table structure is required.")
    
    container = get_docker_container(username)
    result = execute_sql(container, sql_query, username, username)
    return {"message": f"Table {table_name} structure modified successfully.", "result": result}

# Endpoint to drop a table (for completeness, same as delete but often used in different contexts)
@app.delete("/users/{username}/tables/{table_name}/drop")
async def drop_table(username: str, table_name: str):
    container = get_docker_container(username)
    sql_query = f"DROP TABLE IF EXISTS {table_name};"
    result = execute_sql(container, sql_query, username, username)
    return {"message": f"Table {table_name} dropped successfully.", "result": result}
