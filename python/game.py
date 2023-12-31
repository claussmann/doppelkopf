import time
import random
import secrets

from threading import Lock
from datatypes import *
from table import *
from errors import *



class Game:

    def get_player(self, token:str) -> PlayerPrivate:
        """
        Return the player by the given token.
        """
        if token in self.players:
            return self.players[token]
        raise PlayerNotExistingException()

    def get_pub_player(self, index) -> PlayerPub:
        """
        Return the public representation of the player at index.
        """
        return self._get_player_by_index(index)

    def get_table(self) -> Table:
        """
        Return the cards layed along other information.
        """
        return self.table

    def new_player(self, name:str) -> PlayerPrivate:
        """
        Add a new player to the game (as long as no more than
        4 players are in the game then). Sets the game to state
        WAIT_VORBEHALT if 4 players are reached.

        ONLY CALLABLE DURING STATE WAIT_PLAYER_LOGIN
        """
        with self.mutex:
            if self.state != State.WAIT_PLAYER_LOGIN:
                raise PlayerLimitException()
            if len(name) > 20 or len(name) < 3:
                raise NameException()
            for existing_player in self.players.values():
                if existing_player.name == name:
                    raise NameException()
            token = secrets.token_hex(16)
            p = PlayerPrivate()
            self.players[token] = p
            p.token = token
            p.name = name
            num_players = len(self.players)
            p.sequence_index = num_players - 1
            p.hand = self.card_deck[12*(num_players-1) : 12*num_players]
            if num_players == 4:
                self.state = State.WAIT_VORBEHALT
            return p

    def lay_card(self, token:str, card:Card):
        """
        The player lays the card. This function checks whether this is
        allowed. If the stich is finished (all four players layed cards)
        the winner is determined, and points are counted. Game state is
        set to WAIT_VORBEHALT again for next round.

        ONLY CALLABLE DURING STATE PLAYING
        """
        with self.mutex:
            if self.state != State.PLAYING:
                raise GameNotReadyException()
            p = self.get_player(token)
            if not card in p.hand:
                raise CardInvalidError()
            self.table.lay_card(p, card)
            p.hand.remove(card)
            if self.table.stich_finished():
                self.stich_count += 1
                winner = self._get_player_by_index(self.table.get_winner_index())
                winner.runden_punkte += self.table.count()
                self.table.set_next_player(winner.sequence_index)
            if self.stich_count >= 12:
                # TODO: Auswertung
                self.aufspiel_index = (self.aufspiel_index + 1) % 4
                self.state = State.WAIT_VORBEHALT

    def vorbehalt(self, token:str, vorbehalt:Vorbehalt):
        """
        Players can state whether they want a normal game (GESUND)
        or a special game. If all players submitted their "Vorbehalt",
        this method generates a new Table object and game status
        is set to PLAYING.

        ONLY CALLABLE DURING STATE WAIT_VORBEHALT
        """
        player = self.get_player(token)
        with self.mutex:
            if self.state != State.WAIT_VORBEHALT:
                raise VorbehaltInvalidException()
            player.vorbehalt = vorbehalt
            if len([p for p in self.players.values() if p.vorbehalt != Vorbehalt.NOTYET]) >= 4:
                highest_vorbehalt = Vorbehalt.NOTYET
                vorbehalt_von = None
                solos = [Vorbehalt.GESUND, Vorbehalt.SOLO, Vorbehalt.FLEISCHLOSER, Vorbehalt.BUBENSOLO, Vorbehalt.DAMENSOLO]
                for i in range(4):
                    index = (self.aufspiel_index + i) % 4
                    p = self._get_player_by_index(index)
                    if p.vorbehalt in solos and not p.solo_played:
                        highest_vorbehalt = p.vorbehalt
                        vorbehalt_von = p
                        break # Pflichtsolo
                    elif solos.index(p.vorbehalt) > solos.index(highest_vorbehalt):
                        highest_vorbehalt = p.vorbehalt
                        vorbehalt_von = p
                self.table._initialize(vorbehalt_von.sequence_index, highest_vorbehalt)
                # TODO: set teams
                self.state = State.PLAYING

    def schmeissen(self, token:str):
        """
        Player can indicate that he wants new cards. If he is
        eligable, this function gives new cards to everyone and
        asks the players for new "Vorbehalt".

        ONLY CALLABLE DURING STATE WAIT_VORBEHALT
        """
        player = self.get_player(token)
        with self.mutex:
            if self.state != State.WAIT_VORBEHALT:
                raise VorbehaltInvalidException()
            num_of_nines = len([c for c in player.hand if c in [Card.D9, Card.H9, Card.C9, Card.S9]])
            num_of_tens = len([c for c in player.hand if c in [Card.D10, Card.H10, Card.C10, Card.S10, Card.DA, Card.HA, Card.CA, Card.SA]])
            num_of_trumpf = len([c for c in player.hand if c in [Card.H10, Card.CD, Card.SD, Card.HD, Card.DD, Card.CJ, Card.SJ, Card.HJ, Card.DJ, Card.DA, Card.D10, Card.DK, Card.D9]])
            if num_of_nines >= 5 or num_of_tens >= 7 or num_of_trumpf <= 2:
                self._give_new()
            else:
                raise VorbehaltInvalidException()


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
        self.players = dict()
        self.table = Table()
        self.table._initialize(0, Vorbehalt.NOTYET)
        self.aufspiel_index = 0
        self.state = State.WAIT_PLAYER_LOGIN
        self.game_mode = Vorbehalt.GESUND
        self.stich_count = 0
        self.game_count = 0

    def _give_new(self):
        with self.mutex:
            random.shuffle(self.card_deck)
            i = 0
            for p in self.players.values():
                p.hand = self.card_deck[12*(i) : 12*(i+1)]
                i += 1


    def _get_player_by_index(self, index:int) -> PlayerPrivate:
        for p in self.players.values():
            if p.sequence_index == index:
                return p
        raise PlayerNotExistingException()