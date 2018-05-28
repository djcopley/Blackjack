import unittest
import blackjack


class TestCard(unittest.TestCase):
    def setUp(self):
        self.cards = []
        for i in range(52):
            self.cards.append(blackjack.Card(i))

    def test_get_value(self):
        for index, card in enumerate(self.cards):
            card_num = index % 13
            value = 11 if card_num == 0 else 10 if card_num > 9 else card_num + 1

            assert value == card.get_value()

    def test_visibility(self):
        for card in self.cards:
            card.face_up()
            assert card.visible
            card.face_down()
            assert not card.visible

    def test_suit(self):
        for index, card in enumerate(self.cards):
            if index < 13:
                assert card.get_suit() == 'Spades'
            elif index < 26:
                assert card.get_suit() == 'Hearts'
            elif index < 39:
                assert card.get_suit() == 'Clubs'
            elif index < 52:
                assert card.get_suit() == 'Diamonds'

    def test_rank(self):
        rank = {0: 'Ace', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6',
                6: '7', 7: '8', 8: '9', 9: '10', 10: 'Jack', 11: 'Queen',
                12: 'King'}

        for index, card in enumerate(self.cards):
            assert rank[index % 13] == card.get_rank()


class TestChipBank(unittest.TestCase):
    def setUp(self):
        self.bank = blackjack.ChipBank(1000)

    def test_bank(self):
        assert self.bank.get_balance() == 1000

    def test_withdraw(self):
        assert self.bank.get_balance() == 1000
        assert self.bank.withdraw(100) == 100
        assert self.bank.get_balance() == 900
        assert self.bank.withdraw(1000) == 900
        assert self.bank.get_balance() == 0

    def test_deposit(self):
        assert self.bank.get_balance() == 1000
        self.bank.deposit(250)
        assert self.bank.get_balance() == 1250
        self.bank.deposit(50)
        assert self.bank.get_balance() == 1300

    def test_chip_count(self):
        assert self.bank.get_balance() == 1000
        assert self.bank.chip_count() == (10, 0, 0, 0)
        self.bank.deposit(341)
        assert self.bank.chip_count() == (13, 1, 3, 1)
