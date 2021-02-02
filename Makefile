requirements:
	poetry export -f requirements.txt -o requirements.txt

run: requirements
	docker-compose up

db:
	cat output/dump.json | jq -c  | sqlite-utils insert --alter --nl --truncate output/dump.sqlite requests -

serve: db
	datasette -o output/dump.sqlite
