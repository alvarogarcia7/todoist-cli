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
        value = ""
        if "Credit Card Purchase Card" in description:
            search = re.compile("([A-Z]{3}) \d+(\.\d{2})?").search(description)
            if search:
                value = search.group().split(" ")[1]
        else:
            value = re.compile(BudgetParser._amount_regex).findall(description)[0]
        return Decimal('-'+value.replace(',', '.'))

    @staticmethod
    def parse_description(description) -> str:
        if "Credit Card Purchase Card" in description:
            description = description.split("Available Balance AED")[0]
            description = " ".join(description.split(" ")[8:])
            ARE_as_word = "\\bARE\\b"
            search = re.search(ARE_as_word, description)
            if search:
                description = re.split(ARE_as_word, description)[0].strip()
                chunks = description.split(" ")
                selected_chunks = chunks
                if "DUBAI" == chunks[-1].upper():
                    selected_chunks = chunks[:-1]
                elif "DHABI" == chunks[-1].upper():
                    selected_chunks = chunks[:-2]

                description = " ".join(selected_chunks)
            return description

        raw_values = re.compile(BudgetParser._amount_regex).split(description)
        raw_values = list(map(lambda item_description: item_description
                              .strip()
                              .strip('., '), raw_values))
        return " ".join(raw_values)
