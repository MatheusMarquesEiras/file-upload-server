all: run

dmk:
	mkdir uploads

run:
	cd docker && docker compose up -d

run_dev:
	cd docker && docker compose up -d
	python main.py

rebuild: clean
	cd docker && docker-compose up --build -d

absc: clean
	docker system prune -a --volumes

clean:
	cd docker && docker compose down