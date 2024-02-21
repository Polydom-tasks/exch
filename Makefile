install:
	poetry env use python3.11
	poetry config virtualenvs.create true
	poetry config virtualenvs.in-project true
	poetry install
	source .venv/bin/activate

install-deploy:
	poetry config virtualenvs.create false
	poetry install --only main --no-root --no-cache

lint:
	mypy .
	ruff .
	black --check .

format:
	ruff --fix .
	black .

test:
	pytest tests --slow -vv --cov=.

start:
	uvicorn main:app --host 0.0.0.0 --port 8888 --reload
