# inventory_management
bookstore inventory management
# How to create DB for Postgre

-After installing postgresql: (Do everything past this point within the virtualenv)
-Install: pip install psycopg2-binary
-Open PostgreSQL: psql postgres
-Create new database: CREATE DATABASE inventory_management_db;
-Create a new user: CREATE USER inventory_user WITH PASSWORD 'find_this_pw_in_.env_file'
-Grant all privileges to new user: GRANT ALL PRIVILEGES ON DATABASE inventory_management_db TO inventory_user
-Exit PostgreSQL shell: \q

-To install dependencies: pip install -r requirements.txt
-After installation: python3 manage.py migrate
-You will need to create a new superuser before running the server