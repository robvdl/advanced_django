.PHONY: install
install: migrate fixtures superuser

.PHONY: migrate
migrate:
	docker-compose exec app ./manage.py migrate

.PHONY: fixtures
fixtures:
	docker-compose exec app ./manage.py loaddata teams persons projects sites types sensors measurements

.PHONY: superuser
superuser:
	docker-compose exec app ./manage.py createsuperuser

.PHONY: psql
psql:
	docker-compose exec db psql -U train
