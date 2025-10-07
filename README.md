# Vidysea Notes Backend

A FastAPI backend for a Notes Application with user authentication, role-based access, and CRUD operations. Supports both user and admin dashboards, pagination, search, and sorting.

## Features

- **User Authentication**
  - Sign-up (name, email, password, role: admin/user)
  - Sign-in (email, password)
- **Notes Management**
  - Create, read, update, delete notes
  - Pagination, search by title, sort by newest/oldest
- **Role-Based Access**
  - Users: manage their own notes
  - Admins: manage all notes, create/edit/delete for any user

## API Endpoints

### Authentication

- `POST /auth/register` — Register a new user
- `POST /auth/login` — Login and receive JWT token

### Notes (User)

- `GET /notes/` — List user's notes (pagination, search, sort)
- `POST /notes/create` — Create a new note
- `PUT /notes/edit/{note_id}` — Edit a note
- `DELETE /notes/delete/{note_id}` — Delete a note

### Notes (Admin)

- `GET /notes/all` — List all notes (pagination, search, sort)
- `POST /notes/admin/create` — Create a note for any user
- `PUT /notes/admin/edit/{note_id}` — Edit any note
- `DELETE /notes/admin/delete/{note_id}` — Delete any note

## Pagination, Search, and Sorting

- **Pagination:** Use `page` and `limit` query parameters
- **Search:** Use `q` query parameter to search by title
- **Sort:** Use `sort_by=newest` or `sort_by=oldest` for sorting by creation date

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL (or MySQL)
- [Poetry](https://python-poetry.org/) or `pip` for dependencies

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/UmranMirza/vidysea_notes_backend
    cd vidysea_notes_backend
    ```

2. Install dependencies:
    ```bash
    poetry install
    # or
    pip install -r requirements.txt
    ```

3. Set up environment variables in `.env` (DB connection, JWT secret, etc.)

4. Run database migrations (Alembic):
    ```bash
    alembic upgrade head
    ```

5. Start the server:
    ```bash
    uvicorn app:app --reload --host 127.0.0.1 --port 5000
    ```

## Usage

- Use an API client (Postman, Insomnia) or connect via frontend (Next.js recommended).
- Authenticate to receive JWT token, include it in `Authorization: Bearer <token>` header for protected endpoints.

## Frontend

A Next.js frontend is recommended for best experience. See the implementation guide in the documentation for details.

## License

MIT

## Author

- MOHD UMRANUDDIN
# Project setup:
1. Create Virtual Environment:
    On Windows: python -m venv venv
    On Linux: python3 -m venv venv
    On MAC: python3 -m venv venv
2. Run Virtual Environment:
    On Windows: .\venv\Scripts\activate
    On Linux: source ./venv/bin/activate
    On MAC: source ./venv/bin/activate
3. Install pip requirements:
    pip3 install -r requirements.txt
4. Create .env file in root and add following details in env (Ask your team members for exact values. Don't share that with anyone. It's used for database access)
5. Deactivate virtual environment (It runs without deactivating too. Need more information on this behaviour):
    deactivate
6. Run Project Locally:
    uvicorn app:app --reload --host 127.0.0.1 --port 5000
    Note: For server deployment, change host to 0.0.0.0 and port to 8000(Needs Verification)
7. Optional:
    Sometimes, you need to also install pip packages on your local system outside venv. In that case, follow step 5 and then step 3 and then step 6.

# Quick Setup on Linux:
virtualenv venv
source ./venv/bin/activate
pip install -r requirements.txt
deactivate

# Debug Configuration: ./venv/launch.json
{
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "app:app",
                "--host",
                "localhost",
                "--port",
                "5004",
                "--reload"
            ],
            "jinja": true,
            "justMyCode": true
        }
    ]
}

