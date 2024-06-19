

crawl_mr:
	manage runspider crawls/mr.py

lint:
	rye run isort . --check --dif
	rye run black --check .
	rye run flake8 src/*

runprod:
	python -m gunicorn fffinder.asgi:application -k uvicorn.workers.UvicornWorker

build:
	./bin/build
