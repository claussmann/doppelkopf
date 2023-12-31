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


class Vorbehalt(Enum):
    NOTYET = "NOT_YET"
    GESUND = "GESUND"
    # HOCHZEIT # TODO: Implement in future version
    # ARMUT # TODO: Implement in future version

    SOLO = "SOLO"
    FLEISCHLOSER = "FLEISCHLOSER"
    BUBENSOLO = "BUBENSOLO"
    DAMENSOLO = "DAMENSOLO"

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