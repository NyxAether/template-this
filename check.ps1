black template_this tests
autoflake -r --in-place template_this tests
isort template_this tests
mypy template_this tests
flake8 template_this tests
pylint template_this tests