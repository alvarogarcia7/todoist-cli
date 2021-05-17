# Todoist integration

## Installation

Get your API token from [Settings > Integrations > API token](https://todoist.com/prefs/integrations).

Place it in `keys.sh`.

## Running it

Update your data:

```
make update-data
```

Then query it:

```
python3 processer.py --due=yesterday
python3 processer.py --due=today

python3 processer.py --project=$PROJECT_NAME --limit=10
```

For more actions, see the Filters configuration in the code.

## Other notes

Note: neither this project, the author are affiliated in any way to Doist (the company behind the Todoist product).

Note: any Doist trademark belongs to the respective owner.

