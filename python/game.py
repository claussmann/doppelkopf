import time
import random
import secrets

from threading import Lock
from datatypes import *
from errors import *



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
        random.shuffle(self.card_deck)
        self.is_active_round = False
        self.players = dict()
    
    def shuffle(self):
        with self.mutex:
            random.shuffle(self.card_deck)
    
    def new_player(self, name:str) -> Player:
        with self.mutex:
            if len(self.players) >= 4:
                raise PlayerLimitException()

            if len(name) > 20 or len(name) < 3:
                raise NameException()

            for existing_player in self.players.values():
                if existing_player.name == name:
                    raise NameException()

            token = secrets.token_hex(16)
            p = Player()
            self.players[token] = p
            p.token = token
            p.name = name
            num_players = len(self.players)
			p.sequence_index = num_players - 1
            p.hand = self.card_deck[12*(num_players-1) : 12*num_players]
        return p
	
	def get_player(self, token:str) -> Player:
		if token in self.players:
			return self.players[token]
		raise PlayerNotExistingException()
        

	def lay_card(self, token:str, card:Card):
		p = self.get_player(token)
		this.round.lay_card(p, card)



class Round():
	def __init__(self, start_with:int):
		self.is_active = True
		self.cards_played = 0
		self.current_player = start_with
		self.current_vorbehalt = Vorbehalt.GESUND
		self.vorbehalt_is_pflichtsolo = False
		self.table = {i : None for i in range(4)}
		self.previous_table = None
		self.points = {i : 0 for i in range(4)}
	
	def player_vorbehalt(self, player:Player, vorbehalt:Vorbehalt, is_pflichtsolo:bool):
		if vorbehalt >= Vorbehalt.SCHMEISSEN:
			self.current_vorbehalt = vorbehalt
		elif not self.vorbehalt_is_pflichtsolo:
			if self.current_vorbehalt < vorbehalt:
				self.current_vorbehalt = vorbehalt
	
	def lay_card(self, player:Player, card:Card):
		if not player.sequence_index == self.current_player:
			raise PlayerSequenceError()
		if not card in player.hand:
			raise CardInvalidError()
		if not self.__check_card_valid(card):
			raise CardInvalidError()
		player.hand.remove(card)
		self.table[self.current_player] = card
		self.current_player = (self.current_player + 1) % 4
		self.cards_played += 1
		if self.cards_played >= 48:
			self.is_active = False
		if self.cards_played % 4 == 0:
			self.points[self.__who_wins(self.table)] = self.__value_of(self.table)
			self.previous_table = table
			self.table = {i : None for i in range(4)}
		
	
	def __check_card_valid(self, card):
		return True
	
	def __who_wins(self, table):
		return 0
	
	def __value_of(self, table):
		points = 0
		for card in table.values():
			if card in [Card.D10, Card.H10, Card.S10, Card.C10]:
				points += 10
			elif card in [Card.DJ, Card.HJ, Card.SJ, Card.CJ]:
				points += 2
			elif card in [Card.DD, Card.HD, Card.SD, Card.CD]:
				points += 3
			elif card in [Card.DK, Card.HK, Card.SK, Card.CK]:
				points += 4
			elif card in [Card.DA, Card.HA, Card.SA, Card.CA]:
				points += 11
		return points