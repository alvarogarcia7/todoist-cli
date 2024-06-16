.ONESHELL:

test: typecheck test-python
.PHONY: test

test-python: check-virtual-env
	pytest .
.PHONY: test-python

check-virtual-env:
	@# Test if the variable is set
	@if [ -z "${VIRTUAL_ENV}" ]; then                                               \
  		echo "Need to activate virtual environment: source ./venv/bin/activate";    \
  		false;       																\
  	fi
.PHONY: check-virtual-env

typecheck: check-virtual-env
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
	sqlite3 budget.db ".read create_views.sql"

_indent-file:
	jq -r '.' ${FILE} > .temporary.file
	mv .temporary.file ${FILE}

select-project-budget:
	sqlite-utils budget.db "select * from tasks where project_name='budget' AND content like '%Credit Card%' AND content like '%AED%'" --json-cols > all_budget.json
	FILE=all_budget.json $(MAKE) _indent-file
	cp all_budget.json selected_budget.json
	vim selected_budget.json
	#sqlite-utils budget.db "delete from tasks where project_name='budget' AND content like '%Credit Card%'"

process-budget: check-virtual-env
	python3 budget_main.py < selected_budget.json > parsed_budget.json
	sqlite-utils insert ./budget.db parsed_budget --pk=id parsed_budget.json

select-budget:
	sqlite-utils budget.db "select '',description,substr(created,1,10),retailer,amount from parsed_budget" --csv | pbcopy
	@echo "Paste and import into Google Sheets"
	@echo "Date paste as value."
	@echo "Now process the remaining: make see-diff"

insert-splitwise:
	sqlite-utils insert budget.db splitwise_lines_ la-pela-es*.csv --csv
	sqlite3 budget.db ".read create_views.sql"

convert-todoist-budget: clean insert select-project-budget process-budget select-budget see-diff

see-diff:
	@echo "compare files using PyCharm all_budget.json selected_budget.json"
