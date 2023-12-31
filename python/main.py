from fastapi import FastAPI, HTTPException
from game import Game
from errors import *
from datatypes import *

doppelkopf_app = FastAPI()

doppelkopf_app.game = Game()


@doppelkopf_app.get("/")
def greeting():
    return {"message": "Welcome to Doppelkopf!"}

@doppelkopf_app.post("/new_player")
def join_new_player(name:str) -> PlayerPrivate:
    try:
        return doppelkopf_app.game.new_player(name)
    except PlayerLimitException:
        raise HTTPException(status_code=400, detail="There are already 4 players in the game.")
    except NameException:
        raise HTTPException(status_code=400, detail="The name is invalid. Names must be unique and between 3 and 20 chars.")

@doppelkopf_app.post("/get_player")
def get_player(token:str) -> PlayerPrivate:
    try:
        return doppelkopf_app.game.get_player(token)
    except PlayerNotExistingException:
        raise HTTPException(status_code=400, detail="The player doesn't exist.")