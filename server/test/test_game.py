import pytest
from doppelkopf.game import *
from doppelkopf.datatypes import *
from doppelkopf.errors import *

def test_player_creation():
    game = Game()
    aragorn = game.new_player("Aragorn")
    assert aragorn.name == "Aragorn"
    assert aragorn.vorbehalt == Vorbehalt.NOTYET
    assert len(aragorn.hand) == 12


def test_player_creation_four_players():
    game = Game()
    aragorn = game.new_player("Aragorn")
    frodo = game.new_player("Frodo")
    gandalf = game.new_player("Gandalf")
    sam = game.new_player("Sam")

    # game accepts vorbehalt
    assert game.get_state() == State.WAIT_VORBEHALT

    # each card exactly twice
    cards = {c:0 for c in Card}
    for c in aragorn.hand:
        cards[c] += 1
    for c in frodo.hand:
        cards[c] += 1
    for c in gandalf.hand:
        cards[c] += 1
    for c in sam.hand:
        cards[c] += 1
    for c in cards:
        assert cards[c] == 2


def test_vorbehalt_gesund():
    game = Game()
    aragorn = game.new_player("Aragorn")
    frodo = game.new_player("Frodo")
    gandalf = game.new_player("Gandalf")
    sam = game.new_player("Sam")
    game.vorbehalt(aragorn.token, Vorbehalt.GESUND)
    game.vorbehalt(sam.token, Vorbehalt.GESUND)
    game.vorbehalt(frodo.token, Vorbehalt.GESUND)
    game.vorbehalt(gandalf.token, Vorbehalt.GESUND)
    assert game.get_state() == State.PLAYING
    assert game.get_game_mode() == Vorbehalt.GESUND


def test_vorbehalt_pflichtsolo():
    game = Game()
    aragorn = game.new_player("Aragorn")
    frodo = game.new_player("Frodo")
    gandalf = game.new_player("Gandalf")
    sam = game.new_player("Sam")
    game.vorbehalt(aragorn.token, Vorbehalt.GESUND)
    game.vorbehalt(frodo.token, Vorbehalt.SOLO)
    game.vorbehalt(gandalf.token, Vorbehalt.GESUND)
    game.vorbehalt(sam.token, Vorbehalt.DAMENSOLO)
    assert game.get_state() == State.PLAYING
    assert game.get_game_mode() == Vorbehalt.SOLO


def test_vorbehalt_lustsolo():
    game = Game()
    aragorn = game.new_player("Aragorn")
    frodo = game.new_player("Frodo")
    gandalf = game.new_player("Gandalf")
    sam = game.new_player("Sam")
    aragorn.solo_played = True
    frodo.solo_played = True
    gandalf.solo_played = True
    sam.solo_played = True
    game.aufspiel_index = 1
    game.vorbehalt(aragorn.token, Vorbehalt.GESUND)
    game.vorbehalt(sam.token, Vorbehalt.SOLO)
    game.vorbehalt(frodo.token, Vorbehalt.GESUND)
    game.vorbehalt(gandalf.token, Vorbehalt.DAMENSOLO)
    assert game.get_state() == State.PLAYING
    assert game.get_game_mode() == Vorbehalt.DAMENSOLO


def test_lay_card():
    game = Game()
    aragorn = game.new_player("Aragorn")
    with pytest.raises(GameNotReadyException):
        game.lay_card(aragorn.token, aragorn.hand[0])

    frodo = game.new_player("Frodo")
    gandalf = game.new_player("Gandalf")
    sam = game.new_player("Sam")
    game.vorbehalt(aragorn.token, Vorbehalt.GESUND)
    game.vorbehalt(frodo.token, Vorbehalt.GESUND)
    game.vorbehalt(gandalf.token, Vorbehalt.GESUND)
    game.vorbehalt(sam.token, Vorbehalt.GESUND)

    with pytest.raises(CardInvalidError):
        cards_not_in_hand = list({c for c in Card} - set(aragorn.hand))
        game.lay_card(aragorn.token, cards_not_in_hand[0])
    with pytest.raises(PlayerSequenceError):
        game.lay_card(frodo.token, frodo.hand[0])

    game.lay_card(aragorn.token, aragorn.hand[0])
    assert len(aragorn.hand) == 11


def test_full_round():
    game = Game()
    aragorn = game.new_player("Aragorn")
    frodo = game.new_player("Frodo")
    gandalf = game.new_player("Gandalf")
    sam = game.new_player("Sam")
    game.vorbehalt(aragorn.token, Vorbehalt.GESUND)
    game.vorbehalt(frodo.token, Vorbehalt.GESUND)
    game.vorbehalt(gandalf.token, Vorbehalt.GESUND)
    game.vorbehalt(sam.token, Vorbehalt.GESUND)

    aragorn.hand = [Card.SA, Card.D9, Card.DD]
    frodo.hand = [Card.S10, Card.C9, Card.CJ]
    gandalf.hand = [Card.HK, Card.HA, Card.CJ]
    sam.hand = [Card.CA, Card.H9, Card.S9]

    game.lay_card(aragorn.token, Card.D9)
    game.lay_card(frodo.token, Card.CJ)
    game.lay_card(gandalf.token, Card.CJ)
    game.lay_card(sam.token, Card.H9)
    assert game.whose_turn() == frodo.sequence_index