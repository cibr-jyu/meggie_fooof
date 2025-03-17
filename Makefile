.PHONY: format
format:
	black meggie_fooof

.PHONY: check
check:
	black --check meggie_fooof
	pylama meggie_fooof

.PHONY: test
test:
	pytest -s
