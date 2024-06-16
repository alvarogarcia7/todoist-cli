import argparse

import json
import locale
import sys

from budget_parser import BudgetParser


def parse_item(x):
    budget_parser = BudgetParser()
    item = budget_parser.parse(x['content'])
    x['description'] = x['description'] or item.description
    x['retailer'] = item.description
    x['amount'] = item.amount
    return x


def stringize(x):
    locale.setlocale(locale.LC_MONETARY, 'es_ES')
    x['amount'] = locale.currency(x['amount'], grouping=True, symbol=False)
    return x


def main(args):
    items = json.load(sys.stdin)
    items = list(map(parse_item, items))
    items = list(map(stringize, items))
    print(json.dumps(items, sort_keys=False, indent=4))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    main(parser.parse_args())
