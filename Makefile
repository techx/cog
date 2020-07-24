build:
	docker-compose build

sass:
	cd cog/static && sass --watch sass/app.scss:css/app.css
start:
	docker-compose up -d
	@echo "cog listening on port 8000, postgres on 5432"
	@echo "run 'make logs' to watch logs"

stop:
	docker-compose down

# watch the logs from cog
logs:
	docker-compose logs -f -t cog 

# run all the migrations
migrate:
	docker-compose run cog python initialize.py
	# db/containers still running