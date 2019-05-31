# Development

## Setup
- Set up a Python2
[virtualenv](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/)
to manage Python dependencies 
- Source your virtualenv 
- Run `pip install -r requirements.txt` to install all dependencies 
- Install [PostgreSQL](https://www.postgresql.org/download/) to run a database locally
  - If you're using Mac, install *Postgres.app* from
  [here](https://www.postgresql.org/download/) 
- Set three environment variables: 
  - `DATABASE_URL` points to the URL of a development database,
which has to be set up using Postgres on your system. A sample `DATABASE_URL`
could look like `postgres://username:password@localhost/cog`. 
  - `SECRET` some random JWT secret
- Run `python initialize.py` 
  - This initializes the database - run it if you make any changes to the models and
  are fine with overwriting data.

## Running 
- Run `make run` 
- The site will be visible at `localhost:80`

## Tests 
- Run `make test` to run all tests
