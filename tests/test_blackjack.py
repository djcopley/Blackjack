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
        pass

    def tearDown(self):
        pass

    def test_blackjack(self):
        pass


class TestBlackjackHand(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_blackjack(self):
        pass


class TestBlackjack(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_blackjack(self):
        pass
