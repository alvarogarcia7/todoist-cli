.ONESHELL:

test:
	$(MAKE) typecheck
.PHONY: test

typecheck:
	. ${PWD}/venv/bin/activate
	find . \( -path ./venv -o -path ./build \) -prune -false -o -iname "*.py" -type f -exec mypy {} \;
.PHONY: typecheck

save-existing-data:
	rm -rf ./tmp
	mkdir tmp
	mv *.json tmp
	mv tmp data/$(shell date +"%Y-%m-%dT%H%M%S")
.PHONY: save-existing-data

update-data:
	$(MAKE) save-existing-data
	./get_all_projects.sh
	./get_all_tasks.sh
.PHONY: update-data