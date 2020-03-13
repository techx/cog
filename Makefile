build:
	docker-compose build

sass:
	cd hardwarecheckout/static && sass --watch sass/app.scss:css/app.css
start:
	docker-compose up -d
	@echo "hardwarecheckout listening on port 8000, postgres on 5432"
	@echo "run 'make logs' to watch logs"

stop:
	docker-compose down

# watch the logs from hardwarecheckout
logs:
	docker-compose logs -f -t hardwarecheckout 

# run all the migrations
migrate:
	docker-compose run hardwarecheckout python initialize.py
	# db/containers still running