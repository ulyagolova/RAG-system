install:
	pip install -r requirements.txt -r requirements-dev.txt

lint:
	ruff check src tests
	ruff format --check src tests
	mypy src

test:
	pytest -q
