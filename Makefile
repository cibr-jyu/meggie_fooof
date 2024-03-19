.PHONY: format
format:
	black -t py39 meggie_fooof

.PHONY: check
check:
	black --check -t py39 meggie_fooof
	pylama meggie_fooof

.PHONY: test
test:
	pytest -s
