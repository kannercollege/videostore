APP_NAME = videostore
ENV = FLASK_ENV=development FLASK_APP=$(APP_NAME)

.PHONY: format init-db run

format:
	black .

init-db:
	@echo WARNING: DROPPING ALL TABLES!
	@echo PRESS CTRL+C WITHIN 10 SECONDS TO CANCEL && sleep 10

	$(ENV) flask init-db

run:
	$(ENV) flask run

run-network:
	$(ENV) flask run --host=0.0.0.0
