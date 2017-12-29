PROJECT TRAINING 1 INSTALLATION:

-install Python3.5 or higher
-install postgresql and pgadmin4

CONFIGURE PG ADMIN:

At installation, choose the username 'postgres' (usually the default user name), 'root' as password, port must be 5432 (default port value at installation).
Run pgadmin4, create a database and name it 'project_training'.
Restore the database 'project_training' by using the bachup file 'project_training.backup' loacted at project root.

PYTHON ENVIRONMENT:
setup a virtual environment using venv (linux) or virtualenv (windows)
--> venv env
go into the created folder 'env'
cd env/scripts
run the script named 'activate'
go ack to project root
use command: pip install -r requirements.txt
run the app.py file
--> py app.py
