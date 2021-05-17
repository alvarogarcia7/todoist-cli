.ONESHELL:

test:
	$(MAKE) typecheck
.PHONY: test

typecheck:
	. ${PWD}/venv/bin/activate
	find . \( -path ./venv -o -path ./build \) -prune -false -o -iname "*.py" -type f -exec mypy {} \;
.PHONY: typecheck
