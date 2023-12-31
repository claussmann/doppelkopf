from datatypes import *
from pydantic import BaseModel, Field

class Table(BaseModel):

    player_index: int = Field(description="The player who is next.", default=0)
    game_mode: Vorbehalt = Field(description="The Vorbehalt which is played this round.", default=Vorbehalt.NOTYET)
    cards_layed: dict = Field(description="The cards already layed in this round.", default=dict())

    def is_stich_finished(self):
        for card in self.cards_layed.values():
            if card == None:
                return False
        return True

    def lay_card(self, player, card):
        if not player.sequence_index == self.player_index:
            raise PlayerSequenceError()
        if not self._check_correct_bedient(player, card):
            raise CardInvalidError()
        self.cards_layed[self.player_index] = card
        self.player_index = (self.player_index + 1) % 4

    def winner(self):
        return 0 # TODO

    def count(self):
        ret = 0
        for card in self.cards_layed.values():
            if card in [Card.DJ, Card.HJ, Card.CJ, Card.SJ]:
                ret += 2
            if card in [Card.DD, Card.HD, Card.CD, Card.SD]:
                ret += 3
            if card in [Card.DK, Card.HK, Card.CK, Card.SK]:
                ret += 4
            if card in [Card.D10, Card.H10, Card.C10, Card.S10]:
                ret += 10
            if card in [Card.DA, Card.HA, Card.CA, Card.SA]:
                ret += 11
        return ret

    def set_next_player(self, index):
        self.player_index = index


    def _initialize(self, start_player_index:int, game_mode:Vorbehalt):
        self.player_index = start_player_index
        self.game_mode = game_mode
        self.cards_layed = {i: None for i in range(4)}

    def _check_correct_bedient(self, player, card):
        return True # TODO