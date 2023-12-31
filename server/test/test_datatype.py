import pytest
from doppelkopf.datatypes import *

def test_vorbehalt():
    v1 = Vorbehalt.GESUND
    assert not v1.is_solo()

    v2 = Vorbehalt.SOLO
    assert v2.is_solo()

    v3 = Vorbehalt.DAMENSOLO
    assert v3.is_solo()
    assert v3.has_priority_over(v2)
    assert not v2.has_priority_over(v3)
    assert not v3.has_priority_over(v3)
    assert v3.has_priority_over(v1)

def test_card():
    c1 = Card.CK
    c2 = Card.H10

    assert c1.counting_value() == 4
    assert c1.is_cross()
    assert not c1.is_heart()

    assert c2.counting_value() == 10
    assert not c2.is_cross()
    assert c2.is_heart()
