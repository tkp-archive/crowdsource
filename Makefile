server:  ## run server
	python3 -m crowdsource.server --debug

questions:  ## run example questions
	python3 examples/local/sample_questions.py

answers:  ## run example answers
	python3 examples/local/sample_answers.py

bonds:  ## run bonds example
	python3 examples/competitions/corporate_bonds.py

tests: ## Clean and Make unit tests
	CROWDSOURCE_KEY=TEST CROWDSOURCE_SECRET=TEST python3 -m pytest -vvv crowdsource/tests/ --cov=crowdsource

fixtures:  ## make db fixtures
	python3 -m crowdsource.persistence.fixtures sqlite:///crowdsource.db

# db:  ## Remake the db
# 	echo crowdsource > tmppw
# 	initdb -D db/ -A md5  -U cs --pwfile=tmppw
# 	rm tmppw
# 	sed -i -le 's/\#port\ \=\ 5432/port\ \=\ 8890/' db/postgresql.conf
# 	pg_ctl -D db -l logfile start
# 	createdb -O cs cs -E utf-8 -U cs -p 8890

# migrations:  ## apply migrations to the db
# 	python3 crowdsource/persistence/migrations/0001.py
# 	python3 crowdsource/persistence/migrations/0002.py

example: ## run simple example
	python3 crowdsource/example.py

tests: ## Make unit tests
	python -m pytest -v crowdsource --cov=crowdsource --junitxml=python_junit.xml --cov-report=xml --cov-branch

lint: ## run linter
	python -m flake8 crowdsource setup.py docs/conf.py
	yarn lint

js:  ## build the js
	yarn
	yarn build

fix:  ## run black fix
	python -m black crowdsource/ setup.py docs/conf.py
	./node_modules/.bin/tslint --fix src/ts/**/*.ts

clean: ## clean the repository
	find . -name "__pycache__" | xargs  rm -rf 
	find . -name "*.pyc" | xargs rm -rf 
	rm -rf .coverage cover htmlcov logs build dist *.egg-info
	make -C ./docs clean
	rm -rf ./docs/*.*.rst  # generated

docs:  ## make documentation
	make -C ./docs html
	open ./docs/_build/html/index.html

install:  ## install to site-packages
	python -m pip install .

dev:
	python -m pip install .[dev]

dist:  ## create dists
	rm -rf dist build
	python setup.py sdist bdist_wheel
	python -m twine check dist/*
	
publish: dist  ## dist to pypi
	python -m twine upload dist/* --skip-existing

# Thanks to Francoise at marmelab.com for this
.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

print-%:
	@echo '$*=$($*)'

.PHONY: clean test tests help annotate annotate_l docs dist
