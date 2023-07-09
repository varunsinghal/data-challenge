start:
	docker compose up -d 

stop:
	docker compose stop 

bash:
	docker compose exec app bash

test:
	docker compose exec -T app pytest

lint:
	docker compose exec -T app isort .
	docker compose exec -T app black .
	docker compose exec -T app flake8 .

lint_check:
	docker compose exec -T app flake8
	docker compose exec -T app black . --check
	docker compose exec -T app isort . -c

requirements:
	docker compose exec -T app poetry export -f requirements.txt -o requirements.txt --without-hashes

lock:
	docker compose exec -T app poetry lock --no-update

install:
	docker compose exec -T app poetry install 

clean:
	docker compose down --rmi local --volumes

init_db:
	docker compose exec -T database bash ./.makefile/init_db.sh

clean_db:
	docker compose exec -T database bash ./.makefile/clean_db.sh 

calendar:
	docker compose exec -T database bash ./.makefile/setup_calendar.sh $(start) $(end)

customer: 
	docker compose exec -T app python main.py customer_csv --file_path=$(FILE)

transaction: 
	docker compose exec -T app python main.py transaction_csv --file_path=$(FILE)

exchange_rate: 
	docker compose exec -T app python main.py exchange_rate_csv --file_path=$(FILE)
