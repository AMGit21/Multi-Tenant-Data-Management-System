import docker
from fastapi import HTTPException
from dotenv import load_dotenv
import os, random
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from schemas import UserCreate

load_dotenv()

MAIN_DB_HOST = os.getenv("MAIN_DB_HOST")
MAIN_DB_NAME = os.getenv("MAIN_DB_NAME")
MAIN_DB_USER = os.getenv("MAIN_DB_USER")
MAIN_DB_PASSWORD = os.getenv("MAIN_DB_PASSWORD")

MAIN_DB_URL = f"postgresql://{MAIN_DB_USER}:{MAIN_DB_PASSWORD}@{MAIN_DB_HOST}/{MAIN_DB_NAME}"

engine = create_engine(MAIN_DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_random_port():
    return random.randint(1024, 65535)

def create_postgresql_container(user: UserCreate):
    client = docker.from_env()
    network_name = "docker_mynetwork"
    try:
        network = client.networks.get(network_name)
    except docker.errors.NotFound:
        network = client.networks.create(network_name, driver="bridge")

    port = get_random_port()
    container_name = f"postgres_{user.username}"

    container = client.containers.run(
        "custom-postgres",
        name=container_name,
        environment={
            "POSTGRES_USER": user.username,
            "POSTGRES_PASSWORD": user.password,
            "POSTGRES_DB": user.username
        },
        ports={f"5432/tcp": port},
        network=network_name,
        detach=True
    )

    print(f"PostgreSQL container for user '{user.username}' is running with name {container_name} on port {port}.")
    return container, container_name, port

def init_main_db():
    """Initialize the main database by creating the 'users' table if it does not exist."""
    print("Starting database initialization...")
    try:
        with SessionLocal() as session:
            session.execute(text('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(100) NOT NULL,
                    registration_time TIMESTAMP NOT NULL,
                    container_id VARCHAR(100) NOT NULL,
                    container_hostname VARCHAR(100) NOT NULL,
                    container_port INTEGER NOT NULL
                );
            '''))
            session.commit()
        print("Users table created or already exists.")
    except SQLAlchemyError as e:
        print(f"Database initialization failed: {e}")
        raise HTTPException(status_code=500, detail=f"Database initialization failed: {e}")



def save_user_to_db(user: UserCreate, container_id: str, hostname: str, port: int):
    """Save the user details along with container information to the main database."""
    try:
        with SessionLocal() as session:
            registration_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            session.execute(
                text('''
                INSERT INTO users (username, password, registration_time, container_id, container_hostname, container_port)
                VALUES (:username, :password, :registration_time, :container_id, :container_hostname, :container_port)
                '''),
                {
                    "username": user.username,
                    "password": user.password,
                    "registration_time": registration_time,
                    "container_id": container_id,
                    "container_hostname": hostname,
                    "container_port": port
                }
            )
            session.commit()
            print(f"User '{user.username}' saved successfully.")
    except Exception as e:
        print(f"Failed to save user to database: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save user to database: {e}")
