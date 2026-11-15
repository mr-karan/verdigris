.PHONY: build check validate screenshots

build:
	python3 build.py

check:
	python3 build.py --check
	python3 -m unittest discover -s tests

validate:
	python3 tools/validate.py

screenshots:
	python3 tools/screenshots.py
