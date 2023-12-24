from enum import Enum
from typing import List
from pydantic import BaseModel, Field

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


class Player(BaseModel):
    hand: List[Card] = list()
    name: str = Field(max_length=20, min_length=3, default="Anonymous")
    token: str = ""