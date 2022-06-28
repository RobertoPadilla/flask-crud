# CRUD con FLASK

## Developer guide

### Dependencies
**sqlite3** to dummy database
~~~bash
sudo apt-get install sqlite
~~~

### Steps
Create a virtual environment

~~~bash
# Creating venv
python3 -m venv venv

# Using venv on Linux
source venv/bin/activate
~~~

Create environment variables duplicating the "env" file and naming it ".env" and fill it with your own values.

Execute migration to get database
~~~bash
flask db init

flask db migrate

flask db upgrade
~~~

Next execute the following statements to run app:

~~~bash
# Flask settings
export FLASK_APP=app.main:app
export FLASK_ENV=development

# Installing dependencies
pip install -r requirements.txt

# Run application
flask run
~~~
