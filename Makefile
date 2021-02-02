requirements:
	poetry export -f requirements.txt -o requirements.txt

run: requirements
	docker-compose up
