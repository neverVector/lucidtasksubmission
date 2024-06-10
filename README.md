## 1. Setup Virtual Environment
```bash
  python -m venv venv
  source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
## 2. Install Dependencies
```bash
    pip install fastapi uvicorn SQLAlchemy pydantic alembic bcrypt python-jose cachetools
```

## 3. Running the Application
```bash
  uvicorn app.main:app --reload
```
## 4. Alembic for Database Migrations
To set up Alembic for handling database migrations:

#### Initialize Alembic:
```bash
alembic init alembic
```

#### Configure alembic.ini:
Set the database URL in the [alembic] section, if not already done.

#### Create Migration Script:
```bash
alembic revision --autogenerate -m "Create initial tables"
```

#### Apply Migration:
```bash
alembic upgrade head
```
