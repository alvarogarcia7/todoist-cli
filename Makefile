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

update-data:  ## Sync data from todoist
	$(MAKE) save-existing-data || true
	./get_all_projects.sh
	./get_all_tasks.sh
.PHONY: update-data

clean: ## Clean the existing database
	rm -rf budget.db

insert: ## Parse JSON -> SQL
	sqlite-utils insert ./budget.db tasks_ --pk=id all_tasks.json
	sqlite-utils insert ./budget.db projects --pk=id all_projects.json
	sqlite-utils budget.db "alter table tasks_ add processed BOOLEAN default FALSE not null;"
	sqlite3 budget.db ".read create_view_tasks.sql"

_indent-file:
	jq -r '.' ${FILE} > .temporary.file
	mv .temporary.file ${FILE}

select-project-budget:
	sqlite-utils budget.db "select * from tasks where project_name='budget'" --json-cols > all_budget.json
	FILE=all_budget.json $(MAKE) _indent-file
	cp all_budget.json selected_budget.json
	vim selected_budget.json

process-budget:
	python3 budget_main.py < selected_budget.json > parsed_budget.json
	sqlite-utils insert ./budget.db parsed_budget --pk=id parsed_budget.json

select-budget:
	sqlite-utils budget.db "select '',description,substr(created,1,10),amount from parsed_budget" --csv | pbcopy
	@echo "Paste and import into Google Sheets"
	@echo "Date paste as value."
	@echo "Now process the remaining: make see-diff"

convert-todoist-budget: clean insert select-project-budget process-budget select-budget see-diff

see-diff:
	@echo "compare files using PyCharm all_budget.json selected_budget.json"
