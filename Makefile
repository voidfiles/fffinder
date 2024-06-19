

crawl_mr:
	manage runspider crawls/mr.py

lint:
	rye run isort . --check --dif
	rye run black --check .
	rye run flake8 src/*

runprod:
	rye run python -m gunicorn fffinder.asgi:application -k uvicorn.workers.UvicornWorker

build:
	./bin/build

test:
	rye run python src/fffinderbase/manage.py test