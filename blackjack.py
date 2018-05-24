import random
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.CRITICAL)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)

logger.addHandler(handler)


class Card:
    """
    Stores playing card information
    """

    def __init__(self, card_num):
        """
        :param card_num: int [0 to 51]
        """
        logger.debug('Card object created')
        rank = {0: 'Ace', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6',
                6: '7', 7: '8', 8: '9', 9: '10', 10: 'Jack', 11: 'Queen',
                12: 'King'}

        self.visible = True
        self.value = card_num % 13
        self._rank = rank[self.value]

        if card_num < 13:
            self._suit = 'Spades'
        elif card_num < 26:
            self._suit = 'Hearts'
        elif card_num < 39:
            self._suit = 'Clubs'
        elif card_num < 52:
            self._suit = 'Diamonds'
        else:
            raise ValueError("card number is out of deck range")

    def __str__(self):
        if self.visible:
            return '{} of {}'.format(self._rank, self._suit)
        else:
            return "<facedown>"

    def __repr__(self):
        return str(self)

    def get_suit(self):
        return self._suit

    def get_rank(self):
        return self._rank

    def get_value(self):
        return 11 if self.value == 0 else 10 if self.value > 9 else self.value + 1

    def face_down(self):
        self.visible = False

    def face_up(self):
        self.visible = True


class ChipBank:
    """
    Stores information about chip count and balance
    """

    def __init__(self, balance):
        """
        :param balance: int
        """
        logger.debug('ChipBank object created')
        self._balance = balance

    def __str__(self):
        return '{} blacks, {} greens, {} reds, {} blues - ' \
               'totaling ${}'.format(*self.chip_count(), self._balance)

    def __repr__(self):
        return str(self)

    def chip_count(self):
        """
        Returns count of chips by color
        """
        logger.debug('ChipBank chip_count() method executed')

        balance = self._balance

        black, balance = balance // 100, balance % 100
        green, balance = balance // 25, balance % 25
        red, balance = balance // 5, balance % 5
        blue, balance = balance // 1, balance % 1

        logger.debug('black={}, green={}, red={}, blue={}'.format(black, green, red, blue))

        return black, green, red, blue

    def withdraw(self, amount):
        logger.debug('ChipBank withdraw() method executed')
        if amount < self._balance:
            logger.info('WITHDRAW - (BALANCE={}, WITHDRAWN={})'.format(self._balance, -amount))
            self._balance -= amount
            return amount
        else:
            previous_balance = self._balance
            self._balance = 0
            logger.info('WITHDRAW - (BALANCE={}, WITHDRAWN={})'.format(previous_balance, -previous_balance))
            return previous_balance

    def deposit(self, amount):
        logger.debug('ChipBank deposit() method executed')
        logger.info('DEPOSIT - (BALANCE={}, DEPOSITED={})'.format(self._balance, amount))
        self._balance += amount

    def get_balance(self):
        logger.debug('ChipBank get_balance() method executed')
        return self._balance


class BlackjackHand:

    def __init__(self):
        logger.debug('BlackjackHand object created')
        self.hand = []

    def __str__(self):
        return ', '.join(map(str, self.hand))

    def __repr__(self):
        return str(self)

    def add_new_card(self, *args):
        logger.debug('BlackjackHand add_new_card() method executed')
        for item in args:
            self.hand.append(item)

    def get_value(self):
        logger.debug('BlackjackHand get_value() method executed')
        value_list = [item.get_value() for item in self.hand]
        value = sum(value_list)

        if value > 21 and 11 in value_list:
            value -= 10

        logger.info('VALUE - {}'.format(value))

        return value


class Blackjack:
    logger.debug('Blackjack object created')

    def __init__(self, starting_dollars):
        logger.debug('Blackjack __init__() method executed')
        self._deck = []
        self._wager = None
        self._active = False

        self._dealer_hand = BlackjackHand()
        self._player_hand = BlackjackHand()
        self.bank = ChipBank(starting_dollars)

    def draw(self):
        logger.debug('Blackjack draw() method executed')
        if not self._deck:
            self._deck = [Card(i) for i in range(52)]
            random.shuffle(self._deck)

        return self._deck.pop()

    def start_hand(self, wager):
        logger.debug('Blackjack start_hand() method executed')
        logger.info('New hand')

        # Sets game to active
        self._active = True

        # Setup dealer hand
        card1, card2 = self.draw(), self.draw()
        card1.face_down()
        self._dealer_hand.add_new_card(card1, card2)

        # Setup player hand
        self._player_hand.add_new_card(self.draw(), self.draw())
        self.bank.withdraw(wager)

        # Remember wager
        self._wager = wager
        logger.info('Wager: {}'.format(self._wager))

        print('Your starting hand: {}'.format(self._player_hand))
        print('Dealer starting hand: {}'.format(self._dealer_hand))

    def hit(self):
        logger.debug('Blackjack hit() method executed')
        new_card = self.draw()
        self._player_hand.add_new_card(new_card)

        print('You drew a {}'.format(new_card))
        print('Your new hand: {}'.format(self._player_hand))

        if self._player_hand.get_value() > 21:
            print('You bust!')
            self.end_hand('lose')

    def stand(self):
        logger.debug('Blackjack stand() method executed')

        while self._dealer_hand.get_value() < 16:
            new_card = self.draw()
            self._dealer_hand.add_new_card(new_card)
            print('Dealer draws a {}'.format(new_card))
            print('Dealers hand is now {}'.format(self._dealer_hand))

        if self._dealer_hand.get_value() > 21:
            print('Dealer busts! You win!')
            self.end_hand('wins')

        elif self._player_hand.get_value() > self._dealer_hand.get_value():
            print('You beat the dealers hand!')
            self.end_hand('wins')

        elif self._dealer_hand.get_value() == self._player_hand.get_value():
            print('You and the dealer tied. Push.')
            self.end_hand('push')

        else:
            print('Dealer beat your hand.')
            self.end_hand('lose')

    def end_hand(self, outcome):
        logger.debug('Blackjack end_hand() method executed')
        logger.info('Outcome: {}'.format(outcome))

        self._dealer_hand.hand[0].face_up()  # Flip dealers first card up

        print('Your finishing hand: {}'.format(self._player_hand))
        print('Dealers finishing hand: {}'.format(self._dealer_hand))

        if outcome == 'wins':
            self.bank.deposit(self._wager * 2)

        elif outcome == 'push':
            self.bank.deposit(self._wager)

        logger.info('New balance: {}'.format(self.bank.get_balance()))
        logger.info('Hand over')
        self.__init__(self.bank.get_balance())

    def game_active(self):
        logger.debug('Blackjack game_active() method executed')
        return self._active

def main():
    blackjack = Blackjack(250)
    while blackjack.bank.get_balance() > 0:
        print("Your remaining chips: {}".format(blackjack.bank))
        wager_input = int(input("How much would you like to wager?: "))
        blackjack.start_hand(wager_input)
        while blackjack.game_active():
            selection = input("STAND or HIT: ").upper()
            if selection == "STAND":
                blackjack.stand()
            elif selection == "HIT":
                blackjack.hit()
        print()
    print("Out of money casino wins!")


if __name__ == '__main__':
    main()
