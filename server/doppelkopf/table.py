from doppelkopf.datatypes import *
from doppelkopf.errors import *
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

    def evaluate(self):
        points = sum(c.counting_value() for c in self.cards_layed.values())
        winner = 0 # TODO
        return (winner, points)

    def set_next_player(self, index):
        self.player_index = index


    def _initialize(self, start_player_index:int, game_mode:Vorbehalt):
        self.player_index = start_player_index
        self.game_mode = game_mode
        self.cards_layed = {i: None for i in range(4)}

    def _check_correct_bedient(self, player, card):
        return True # TODO