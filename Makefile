.PHONY: format
format:
	black meggie_fooof

.PHONY: check
check:
	black --check meggie_fooof
	ruff check meggie_fooof

.PHONY: test
test:
	pytest -s
