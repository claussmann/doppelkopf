from fastapi import FastAPI, HTTPException
from game import Game
from errors import *
from datatypes import Player

doppelkopf_app = FastAPI()

doppelkopf_app.game = Game()


@doppelkopf_app.get("/")
def greeting():
    return {"message": "Welcome to Doppelkopf!"}

@doppelkopf_app.post("/give_new_cards")
def give_new():
    if doppelkopf_app.game.is_active_round:
        raise HTTPException(status_code=400, detail="The game is still running.")
    doppelkopf_app.game.shuffle()
    return {"cards": doppelkopf_app.game.card_deck}

@doppelkopf_app.post("/new_player")
def join_new_player(name:str) -> Player:
    try:
        return doppelkopf_app.game.new_player(name)
    except PlayerLimitException:
        raise HTTPException(status_code=400, detail="There are already 4 players in the game.")
    except NameException:
        raise HTTPException(status_code=400, detail="The name is invalid. Names must be unique and between 3 and 20 chars.")