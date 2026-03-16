.PHONY: install test smoke regression performance clean help

help:
	@echo ""
	@echo "  API Test Automation Framework"
	@echo "  ─────────────────────────────"
	@echo "  make install       Install dependencies"
	@echo "  make test          Run all tests"
	@echo "  make smoke         Run smoke tests only"
	@echo "  make regression    Run regression tests only"
	@echo "  make performance   Run performance tests only"
	@echo "  make clean         Remove reports, logs, caches"
	@echo ""

install:
	pip install -r requirements.txt

test:
	pytest -v

smoke:
	pytest -m smoke -v

regression:
	pytest -m regression -v

performance:
	pytest -m performance -v

clean:
	rm -rf reports/*.html reports/*.json logs/*.log .pytest_cache __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleaned."
