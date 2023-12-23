import time
import random

from threading import Lock
from datatypes import Card



class Game:

    def __init__(self):
        self.mutex = Lock()
        self.card_deck = [
            Card.D9, Card.D9, Card.DJ, Card.DJ, Card.DD, Card.DD,
            Card.DK, Card.DK, Card.D10, Card.D10, Card.DA, Card.DA,
            Card.H9, Card.H9, Card.HJ, Card.HJ, Card.HD, Card.HD,
            Card.HK, Card.HK, Card.H10, Card.H10, Card.HA, Card.HA,
            Card.S9, Card.S9, Card.SJ, Card.SJ, Card.SD, Card.SD,
            Card.SK, Card.SK, Card.S10, Card.S10, Card.SA, Card.SA,
            Card.C9, Card.C9, Card.CJ, Card.CJ, Card.CD, Card.CD,
            Card.CK, Card.CK, Card.C10, Card.C10, Card.CA, Card.CA
        ]
        self.is_active_round = False
    
    def shuffle(self):
        with self.mutex:
            random.shuffle(self.card_deck)
    
