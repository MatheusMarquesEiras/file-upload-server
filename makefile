all: run

run:
	cd docker && docker compose up -d
	python main.py

rebuild: clean
	cd docker && docker-compose up --build -d

absc:
	docker system prune -a --volumes

clean:
	cd docker && docker compose down