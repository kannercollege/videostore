APP_NAME = videostore
ENV = FLASK_ENV=development FLASK_APP=$(APP_NAME)
PROD_ENV = FLASK_APP=$(APP_NAME)

all: run

.PHONY: format run run-network prod-run prod-run-network

format:
	black .

run:
	$(ENV) flask run

run-network:
	$(ENV) flask run --host=0.0.0.0

prod-run:
	$(PROD_ENV) flask run

prod-run-network:
	$(PROD_ENV) flask run --host=0.0.0.0
