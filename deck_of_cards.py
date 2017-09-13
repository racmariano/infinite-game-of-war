from numpy.random import shuffle

class Card:

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        true_vals = {11: 'Jack',
                     12: 'Queen',
                     13: 'King',
                     14: 'Ace',
                    }

        if self.value in true_vals.keys():
            val = true_vals[self.value]
        else:   
            val = str(self.value)
        
        return(val+" of "+self.suit)

    def is_red(self):
        return(self.suit == 'Hearts' or self.suit == 'Diamonds') 

class Hand:

    def __init__(self, from_deck, hand_size=7):
    #Set after dropping to upper threshold for comeback (default = 10) cards
        self.hi_comeback = False
    #Set after dropping to lower threshold for comeback (default = 5) cards
        self.lo_comeback = False

        self.cards = []
        for i in range(hand_size):      
            try:
                self.cards.append(from_deck.deck.pop())
            except IndexError:
                print("You don't have enough cards to make a full hand! Not giving you a hand and returning cards to deck.")
                from_deck.deck += self.cards
                self.cards = []
                return

    def flip(self):
        return(self.cards.pop())

    def gain(self, new_cards):
        self.cards = new_cards+self.cards

class Deck:
    
    def __init__(self):
        suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
        self.deck = [Card(v, s) for v in range(2, 15) for s in suits]
        self.shuffle_cards()

    def shuffle_cards(self):
        for i in range(3):
            shuffle(self.deck)

    def draw(self):
        return(self.deck.pop())



