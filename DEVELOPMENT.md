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
  - `QUILL` is the URL to your Quill instance for auth. 
  - `SECRET` needs to be the same JWT secret used in your Quill instance. 
- Run `python initialize.py` 
  - This initializes the database - run it if you make any changes to the models and
  are fine with overwriting data.

## Running 
- Run `make run` 
- The site will be visible at `localhost:8000`

## Tests 
- Run `make test` to run all tests

## Customizing Semantic Themes
In order to build Semantic you must have node, npm, and gulp installed. 

- Run `npm install semantic-ui` in the root directory to install the Semantic
UI source and build tool dependencies 
  - When prompted by the install script, select `Yes, extend my current settings.` 
  - Continue with default install options until prompted to choose an install 
  directory (`Where should we put Semantic UI inside your project?`) 
    - Enter the existing Semantic directory: `hardwarecheckout/static/vendor/semantic/` 
- Navigate to the Semantic directory and run `gulp build` in order to build Semantic UI 
  - You must run `gulp build` any time you tweak a theme for the change to take effect