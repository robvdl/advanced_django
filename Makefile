#
# Initialize database
#

.PHONY: install
install: migrate fixtures superuser

.PHONY: migrate
migrate:
	docker-compose run --rm web ./manage.py migrate

.PHONY: fixtures
fixtures:
	docker-compose run --rm web ./manage.py loaddata teams persons projects sites types sensors measurements

.PHONY: superuser
superuser:
	docker-compose run --rm web ./manage.py createsuperuser

#
# Database shell
#

.PHONY: psql
psql:
	docker-compose exec db psql -U train

#
# Django shell
#

.PHONY: shell
shell:
	docker-compose exec web ./manage.py shell

#
# Run tests
#

.PHONY: test
test:
	docker-compose exec web ./manage.py test
