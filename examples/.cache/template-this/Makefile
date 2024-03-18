check:
	black {{ project_src }} tests
	autoflake -r --in-place {{ project_src }} tests
	isort {{ project_src }} tests
	mypy {{ project_src }} tests
	flake8 {{ project_src }} tests
	pylint {{ project_src }} tests
