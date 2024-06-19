PORT?=8000
IP_ADDR?=0.0.0.0

crawl_mr:
	manage runspider crawls/mr.py

lint:
	rye run isort . --check --dif
	rye run black --check .
	rye run flake8 src/*

runprod:
	IP_ADDR=${IP_ADDR} PORT=${PORT} ./bin/run

build:
	./bin/build

test:
	rye run python src/fffinderbase/manage.py test