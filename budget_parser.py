import re
from decimal import Decimal


class Item:
    def __init__(self, **kwargs) -> None:
        self.original: str = kwargs['original']
        self.description: str = kwargs['description']
        self.amount: Decimal = kwargs['amount']

    def __repr__(self):
        return f"description: {self.description}, amount: {self.amount}. Original: {self.original}"

    def __eq__(self, other):
        return self.original == other.original \
               and self.description == other.description \
               and self.amount == other.amount


class BudgetParser:
    _amount_regex = '\d+[.,]?\d*'

    def parse(self, description) -> Item:
        amount = self.parse_number(description)
        item_description = self.parse_description(description)
        return Item(amount=amount, description=item_description, original=description)

    @staticmethod
    def parse_number(description: str) -> Decimal:
        value = re.compile(BudgetParser._amount_regex).findall(description)[0]
        return Decimal('-'+value.replace(',', '.'))

    @staticmethod
    def parse_description(description) -> str:
        raw_values = re.compile(BudgetParser._amount_regex).split(description)
        raw_values = list(map(lambda item_description: item_description
                              .strip()
                              .strip('., '), raw_values))
        return " ".join(raw_values)
