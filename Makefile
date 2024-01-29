.venv: pyproject.toml
	python3 -m venv .venv

.venv/deps: .venv pyproject.toml
	.venv/bin/python -m pip install .[dev]
	touch .venv/deps

build: .venv/deps
	rm -rf ./dist/
	.venv/bin/python -m build

# only works with python 3+
lint: .venv/deps
	.venv/bin/validate-pyproject pyproject.toml
	.venv/bin/black --check deepmerge
	.venv/bin/mypy deepmerge

test: .venv/deps
	.venv/bin/pytest deepmerge

ready-pr: test lint
