# Development

## Setup
- Install Docker
- Install Docker Compose
- Copy `sample.env` to `.env` and enter in the proper values
- `make migrate` to initialize and set up the db

## Build
- If you need to rebuild (in case you change the Dockerfile), run `make build`

## Running 
- Run `make start` 
- The site will be visible at `localhost:80`
- `make logs` for a live stream of logs.

## Destroying 
- Run `make stop` to destroy