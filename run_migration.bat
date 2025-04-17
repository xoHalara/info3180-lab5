@echo off
set FLASK_APP=run.py
set DATABASE_URL=postgresql://postgres:J@ybabe2002@localhost:5433/lab5
flask db migrate -m "Initial migration"
flask db upgrade 