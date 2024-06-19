

crawl_mr:
	manage runspider crawls/mr.py

lint:
	rye run isort . --check --dif
	rye run black --check .
	rye run flake8 src/*

runprod:
	rye run python -m gunicorn fffinder.asgi:application -k uvicorn.workers.UvicornWorker

build:
	which rye || curl -sSf https://rye.astral.sh/get | RYE_VERSION="0.34.0" RYE_INSTALL_OPTION="--yes" bash
	rye sync
	rye run python src/fffinderbase/manage.py collectstatic --no-input

test:
	rye run python src/fffinderbase/manage.py test