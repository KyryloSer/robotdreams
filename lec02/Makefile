include .env
export

.PHONY:  help tests clean pre-commit

help:
	@echo "Available commands:"
	@echo "  tests        - Run tests"
	@echo "  pre-commit  - Install pre-commit hooks"
	@echo "  clean       - Clean up cache files"


tests:
	 source venv/Scripts/activate && cd .. && python -m pytest lec02/hw/job1/tests lec02/hw/job2/tests lec02/utils/tests -v

pre-commit:
	source venv/Scripts/activate && pre-commit install
	source venv/Scripts/activate && pre-commit run --all-files
