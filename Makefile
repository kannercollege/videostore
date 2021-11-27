APP_NAME = videostore
ENV = FLASK_ENV=development FLASK_APP=$(APP_NAME)
PROD_ENV = FLASK_APP=$(APP_NAME)

.PHONY: format init-db run run-network prod-run prod-run-network

format:
	black .

init-db:
	@echo WARNING: RESETTNG DATABASE
	@echo PRESS CTRL+C WITHIN 10 SECONDS TO CANCEL && sleep 10

	$(ENV) flask init-db

run:
	$(ENV) flask run

run-network:
	$(ENV) flask run --host=0.0.0.0

prod-run:
	$(PROD_ENV) flask run

prod-run-network:
	$(PROD_ENV) flask run --host=0.0.0.0
