PROJECT TRAINING 1 INSTALLATION:

-install Python3.5 or higher
-install postgresql and pgadmin4

CONFIGURE PG ADMIN AND POSTGRES:

username must be 'postgres' (usually the default user name)
password must be 'root'
port must be '5432' (default port value at installation)
database name must be 'project_training'

Run pgadmin4, create a database and name it 'project_training'.
Restore the database 'project_training' by using the bachup file 'project_training.backup' loacted at project root.

PYTHON ENVIRONMENT AND RUN THE SERVER:
setup a virtual environment using venv (linux) or virtualenv (windows)
--> venv env
go into the created folder 'env'
--> cd env/scripts
run the script named 'activate'
go back to project root
use command: pip install -r requirements.txt
run the app.py file
--> py app.py

requirements.txt contains the dependencies you need to install. If you lost it:
alembic==0.9.6
antiorm==1.2.1
app==0.0.1
click==6.7
db==0.1.1
Flask==0.12.2
Flask-Migrate==2.1.1
Flask-Script==2.0.6
itsdangerous==0.24
Jinja2==2.10
Mako==1.0.7
MarkupSafe==1.0
psycopg2==2.7.3.2
python-dateutil==2.6.1
python-editor==1.0.3
six==1.11.0
SQLAlchemy==1.1.15
Werkzeug==0.12.2