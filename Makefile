.venv: pyproject.toml
	python3 -m venv .venv

.venv/deps: .venv pyproject.toml
	.venv/bin/python -m pip install .[dev]
	touch .venv/deps

build: .venv/deps
	rm -rf ./dist/
	.venv/bin/python -m build

format: .venv/deps
	.venv/bin/black deepmerge

# only works with python 3+
lint: .venv/deps
	.venv/bin/validate-pyproject pyproject.toml
	.venv/bin/black --check deepmerge
	.venv/bin/mypy deepmerge

test: .venv/deps
	.venv/bin/pytest deepmerge

docs: .venv/deps
	$(MAKE) -C docs html

docs-serve: docs
	.venv/bin/python -m http.server --directory docs/_build/html

ready-pr: test lint

clean:
	rm -rf .venv
	rm -rf build
	