# Multi-Tenant Data Management System

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Platform](#running-the-platform)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Future Plans](#future-plans)
- [Thanks](#thanks)

## Overview

This project is a backend system supporting multi-tenancy, allowing dynamic schema definitions for data management. Each tenant has a secure, isolated environment to manage their data schemas dynamically.

## Features

- **Multi-Tenancy:** Each user gets a unique PostgreSQL database container.
- **Dynamic Schema Management:** Users can create, update, and manage their data schemas.
- **FastAPI and Docker Integration:** The backend is built with FastAPI and Docker, ensuring scalability and modularity.
- **Power BI Integration:** The system is designed to support data formats compatible with Power BI for enhanced data analysis.

## Getting Started

### Prerequisites

- Docker
- Python 3.8+
- Node.js (for the frontend)

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/Multi-Tenant-Data-Management-System.git
   cd Multi-Tenant-Data-Management-System
   ```

2. **Set Up Environment:**
   - Create a `.env` file in the `server` directory with the necessary environment variables.
   - Update `docker-compose.yml` with your configurations.

### Running the Platform

1. **Start the Backend (FastAPI) and Database (PostgreSQL) in Docker:**

   ```bash
   docker-compose up --build
   ```

2. **Start the Frontend (Next.js) Manually:**
   ```bash
   cd client
   npm install
   npm run dev
   ```

## API Endpoints

- **List Tables:** `GET /users/{username}/tables`
- **Get Table Data:** `GET /users/{username}/tables/{table_name}`
- **Create Table:** `POST /users/{username}/tables`
- **Update Table Data:** `PUT /users/{username}/tables/{table_name}`
- **Modify Table Structure:** `PATCH /users/{username}/tables/{table_name}/structure`
- **Delete Table:** `DELETE /users/{username}/tables/{table_name}`
- **Drop Table:** `DELETE /users/{username}/tables/{table_name}/drop`

## Project Structure

```plaintext
├── client
│   ├── public
│   ├── src
│   │   ├── components
│   │   ├── pages
│   │   ├── api
│   │   ├── assets
│   │   └── lib
│   ├── .env.local
│   ├── next.config.mjs
│   ├── tailwind.config.ts
│   └── package.json
│
├── server
│   ├── main.py            # server main
│   ├── db_routes.py       # necessary user database routes
│   ├── adminUtils.py
│   ├── user_routes.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── userCrud.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env
│
├── docker
│   ├── docker-compose.yml
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── Dockerfile.postgres
│
├── multi-tenant-platform-screeshots
│
└── README.md
```

- **`client/`**: Contains the Next.js frontend.
- **`server/`**: Contains the FastAPI backend, including the main application code and database interaction logic.
- **`docker/`**: Docker-related files for containerization.

## Future Plans

- Explore Kubernetes for container orchestration.
- Further enhance security and resource management.

## Thanks

Thank you for taking the time to review my work.
