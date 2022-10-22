from decimal import Decimal
from unittest import TestCase

from budget_parser import BudgetParser, Item


class TestBudgetParser(TestCase):

    def setUp(self) -> None:
        self.budget_parser = BudgetParser()

    def test_cleanup_descriptions(self):
        # Do not include any sensitive data in this file / repository
        expected = ['MCDONALDS-54002',
                    "YASCLINIC GROUP SOLE P",
                    "LEBANESE AUTOMATIC",
                    "Alekhlas Baqala LLC",
                    "HIGH SPIRITS ADNH ETIH",
                    "DISTRICT 10 LLC",
                    "SAADIYAT TO GO SUPERMA",
                    "DUBAI TAXI",
                    "FOOD TO GO CARREFOUR B",
                    "KABAYAN KORNER RESTAUR",
                    "CARREFOUR",
                    "RTA DUBAI METRO",
                    "MINISTRY OF INTERIOR",
                    "CITY GOLF CLUB",
                    "COGNA TECH. SOLUTION",
                    "MCDONALDS-THE GALLERIA",
                    "SALT ABU DHABI",
                    "AL AREESH REST N CAFE"
                    ]

        input = [
            "Credit Card Purchase Card No XXXX0000 AED 8.00 MCDONALDS-54002 DUBAI ARE 16/09/21 22:35 available balance AED 1.23 Your statement payment due date is 19/09/2021 Get up to 10% cashback on online shopping with SHOPSMART. Visit Offers Page on the FAB Mobile app",
            "Credit Card Purchase Card No XXXX0000 AED 50.00 YASCLINIC GROUP SOLE P ABU DHABI ARE available balance AED 1.23 Your August statement payment due date is 19/09/2021",
            "Credit Card Purchase Card No XXXX0000 AED 46.20 LEBANESE AUTOMATIC ABU DHABI ARE",
            "Credit Card Purchase Card No XXXX0000 AED 17.00 Alekhlas Baqala LLC Abu Dhabi ARE Available Balance Get up to 10% cashback on online shopping with SHOPSMART. Visit Offers Page on the FAB Mobile app",
            "Credit Card Purchase Card No XXXX0000 AED 187.50 HIGH SPIRITS ADNH ETIH ABU DHABI ARE Available Balance AED Get up to 10% cashback on online shopping with SHOPSMART. Visit Offers Page on the FAB Mobile app",
            "Credit Card Purchase Card No XXXX0000 AED 17.20 DISTRICT 10 LLC ABU DHABI ARE Available Balance September statement payment due date is 20/10/2021 Get up to 10% cashback on online shopping with SHOPSMART. Visit Offers Page on the FAB Mobile app",
            "Credit Card Purchase Card No XXXX0000 AED 27.65 SAADIYAT TO GO SUPERMA ABU DHABI ARE available balance AED 1.23 Your September statement payment due date is 20/10/2021 Get up to 10% cashback on online shopping with SHOPSMART. Visit Offers Page on the FAB Mobile app",
            "Credit Card Purchase Card No XXXX0000 AED 13.00 DUBAI TAXI DUBAI ARE available balance AED 1.23 Your September statement payment due date is 20/10/2021 Get up to 10% cashback on online shopping with SHOPSMART. Visit Offers Page on the FAB Mobile app",
            "Credit Card Purchase Card No XXXX0000 AED 3.10 FOOD TO GO CARREFOUR B DUBAI ARE available balance AED 1.23 Your statement payment due date is 20/10/2021 Get up to 10% cashback on online shopping with SHOPSMART. Visit Offers Page on the FAB Mobile app",
            "Credit Card Purchase Card No XXXX0000 AED 25.00 KABAYAN KORNER RESTAUR DUBAI ARE available balance AED 1.23 Your September statement payment due date is 20/10/2021 Get up to 10% cashback on online shopping with SHOPSMART. Visit Offers Page on the FAB Mobile app",
            "Credit Card Purchase Card No XXXX0000 AED 10.00 CARREFOUR DUBAI ARE available balance AED 1.23 Your September statement payment due date is 20/10/2021 Get up to 10% cashback on online shopping with SHOPSMART. Visit Offers Page on the FAB Mobile app",
            "Credit Card Purchase Card No XXXX0000 AED 30.00 RTA DUBAI METRO DUBAI ARE available balance AED 1.23 Your September statement payment due date is 20/10/2021 Get up to 10% cashback on online shopping with SHOPSMART. Visit Offers Page on the FAB Mobile app",
            "Credit Card Purchase Card No XXXX0000 AED 54.06 MINISTRY OF INTERIOR ABU DHABI ARE available balance AED 1.23 Your September statement payment due date is 20/10/2021 Get up to 10% cashback on online shopping with SHOPSMART. Visit Offers Page on the FAB Mobile app",
            "Credit Card Purchase Card No XXXX0000 AED 95.00 CITY GOLF CLUB ABU DHABI ARE available balance AED 1.23 Your statement payment due date is Get up to 10% cashback on online shopping with SHOPSMART. Visit Offers Page on the FAB Mobile app",
            "Credit Card Purchase Card No XXXX0000 AED 50.00 COGNA TECH. SOLUTION ABU DHABI ARE 18/10/21 18:58 available balance AED 1.23 Your statement payment due date is Get up to 10% cashback on online shopping with SHOPSMART. Visit Offers Page on the FAB Mobile app viaje",
            "Credit Card Purchase Card No XXXX0000 AED 2.00 MCDONALDS-THE GALLERIA ABU DHABI ARE available balance AED 1.23 Get up to 10% cashback on online shopping with SHOPSMART. Visit Offers Page on the FAB Mobile app",
            "Credit Card Purchase Card No XXXX0000 AED 32 SALT ABU DHABI ABU DHABI ARE available balance AED 1.23 Get up to 10% cashback on online shopping with SHOPSMART. Visit Offers Page on the FAB Mobile app",
            "Credit Card Purchase Card No XXXX0000 AED 15.00 AL AREESH REST N CAFE ABU DHABI ARE"
            ]

        for case in range(len(input)):
            self.assertEqual(expected[case], self.budget_parser.parse_description(input[case]))
            print("Success with " + case.__str__())


    def test_parse_credit_card_movement(self):
        self.assertEqual(Decimal('-8.00'),
                         self.budget_parser.parse_number(
                             'Credit Card Purchase Card No XXXX1234 AED 8.00 TRADER-12345 DUBAI ARE 01/01/01 '
                             '00:00 available balance AED 1.23 Your statement payment due date is 01/02/2021'))

        self.assertEqual(Decimal('-32'),
                         self.budget_parser.parse_number('Credit Card Purchase Card No XXXX0000 AED 32 SALT ABU DHABI ABU DHABI'))

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
