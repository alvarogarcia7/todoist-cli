from decimal import Decimal
from unittest import TestCase

from budget_parser import BudgetParser, Item


class TestBudgetParser(TestCase):

    def setUp(self) -> None:
        self.budget_parser = BudgetParser()

    def test_parse_numbers_are_always_turned_negative(self):
        self.assertEqual(Decimal('-4.00'), self.budget_parser.parse_number('Example. 4,00 eur'))

    def test_parse_numbers(self):
        with self.subTest("with comma"):
            with self.subTest("without decimals"):
                self.assertEqual(Decimal('-4.00'), self.budget_parser.parse_number('Example. 4,00 eur'))
            with self.subTest("with decimals"):
                self.assertEqual(Decimal('-4.99'), self.budget_parser.parse_number('Example. 4,99 eur'))

        with self.subTest("with dot"):
            with self.subTest("without decimals"):
                self.assertEqual(Decimal('-5.00'), self.budget_parser.parse_number('Example. 5.00 eur'))
            with self.subTest("with decimals"):
                self.assertEqual(Decimal('-5.01'), self.budget_parser.parse_number('Example. 5.01 eur'))

        with self.subTest("without any decimal separator"):
            self.assertEqual(Decimal('-6.00'), self.budget_parser.parse_number('6'))

    def test_parse_whole(self):
        whole_text = 'Example. 5.00 eur'
        expected = Item(original=whole_text, description="Example eur", amount=Decimal('-5.00'))
        self.assertEqual(expected, self.budget_parser.parse(whole_text))

    def test_parse_whole_with_text_around_the_amount(self):
        whole_text = 'Example. 5.00 eur, another one'
        expected = Item(original=whole_text, description="Example eur, another one", amount=Decimal('-5.00'))
        self.assertEqual(expected, self.budget_parser.parse(whole_text))

    def test_parse_description(self):
        with self.subTest('Ending dot'):
            self.assertEqual('Example', self.budget_parser.parse_description('Example.'))
        with self.subTest('Spaces at the end'):
            self.assertEqual('Example Example', self.budget_parser.parse_description('Example Example '))
        with self.subTest('Comma(s) at the end'):
            self.assertEqual('Example, Example', self.budget_parser.parse_description('Example, Example,,'))
        with self.subTest('Comma(s) in the middle are replace'):
            self.assertEqual('Example, Example', self.budget_parser.parse_description('Example, Example,,'))
        with self.subTest('Dots in the middle'):
            self.assertEqual('E.xam.ple', self.budget_parser.parse_description('E.xam.ple'))
