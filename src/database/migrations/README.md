"""
Database migrations with Alembic.

LEARNING NOTES:

Alembic provides version control for your database schema.

To initialize Alembic in this folder:
alembic init alembic

To create a new migration after changing models.py:
alembic revision --autogenerate -m "description of change"

To apply migrations:
alembic upgrade head

To downgrade:
alembic downgrade -1

Migrations are SQL scripts that can be:

- applied in order (upgrade)
- rolled back (downgrade)
- tracked in git for reproducibility

Phase 1 task: Initialize Alembic and create the first migration.
"""
