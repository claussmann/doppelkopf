from enum import Enum
from typing import List
from pydantic import BaseModel, Field


class State(Enum):
    WAIT_PLAYER_LOGIN = "WAIT_PLAYER_LOGIN"
    WAIT_VORBEHALT = "WAIT_VORBEHALT"
    PLAYING = "PLAYING"

class Card(Enum):
    # Diamonds
    D9 = "D9"
    DJ = "DJ"
    DD = "DD"
    DK = "DK"
    D10 = "D10"
    DA = "DA"

    # Heart
    H9 = "H9"
    HJ = "HJ"
    HD = "HD"
    HK = "HK"
    H10 = "H10"
    HA = "HA"

    # Spades
    S9 = "S9"
    SJ = "SJ"
    SD = "SD"
    SK = "SK"
    S10 = "S10"
    SA = "SA"

    # Clubs
    C9 = "C9"
    CJ = "CJ"
    CD = "CD"
    CK = "CK"
    C10 = "C10"
    CA = "CA"

    def is_diamond(self):
        dia = [Card.D9, Card.DK, Card.DJ, Card.DD, Card.D10, Card.DA]
        return self in dia

    def is_heart(self):
        hearts = [Card.H9, Card.HK, Card.HJ, Card.HD, Card.H10, Card.HA]
        return self in hearts

    def is_spades(self):
        spades = [Card.S9, Card.SK, Card.SJ, Card.SD, Card.S10, Card.SA]
        return self in spades

    def is_cross(self):
        cross = [Card.C9, Card.CK, Card.CJ, Card.CD, Card.C10, Card.CA]
        return self in cross

    def counting_value(self):
        if self in [Card.DJ, Card.HJ, Card.CJ, Card.SJ]:
            return 2
        if self in [Card.DD, Card.HD, Card.CD, Card.SD]:
            return 3
        if self in [Card.DK, Card.HK, Card.CK, Card.SK]:
            return 4
        if self in [Card.D10, Card.H10, Card.C10, Card.S10]:
            return 10
        if self in [Card.DA, Card.HA, Card.CA, Card.SA]:
            return 11
        return 0


class Vorbehalt(Enum):
    NOTYET = "NOT_YET"
    GESUND = "GESUND"
    # HOCHZEIT # TODO: Implement in future version
    # ARMUT # TODO: Implement in future version

    SOLO = "SOLO"
    FLEISCHLOSER = "FLEISCHLOSER"
    BUBENSOLO = "BUBENSOLO"
    DAMENSOLO = "DAMENSOLO"

    def is_solo(self):
        return self in [Vorbehalt.SOLO, Vorbehalt.FLEISCHLOSER, Vorbehalt.BUBENSOLO, Vorbehalt.DAMENSOLO]

    def has_priority_over(self, other):
        priority = [Vorbehalt.SOLO, Vorbehalt.FLEISCHLOSER, Vorbehalt.BUBENSOLO, Vorbehalt.DAMENSOLO]
        if other not in priority:
            return True
        return priority.index(self) > priority.index(other)

class Team(Enum):
    RE = "Re"
    CONTRA = "Contra"
    NONE = "None"

class PlayerPub(BaseModel):
    name: str = Field(max_length=20, min_length=3, default="Anonymous")
    solo_played: bool = False
    vorbehalt: Vorbehalt = Field(default=Vorbehalt.NOTYET)
    sequence_index: int = 0
    sieg_punkte: int = 0

class PlayerPrivate(PlayerPub):
    hand: List[Card] = list()
    token: str = ""
    runden_punkte: int = 0
    team: Team = Team.NONE