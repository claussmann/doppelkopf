from fastapi import FastAPI, HTTPException

from doppelkopf.game import Game
from doppelkopf.errors import *
from doppelkopf.datatypes import *
from doppelkopf.table import *

doppelkopf_app = FastAPI()

doppelkopf_app.game = Game()


@doppelkopf_app.get("/")
def status() -> State:
    return doppelkopf_app.game.state

@doppelkopf_app.post("/player/new")
def join_new_player(name:str) -> PlayerPrivate:
    return doppelkopf_app.game.new_player(name)

@doppelkopf_app.get("/player/private")
def get_player(token:str) -> PlayerPrivate:
    return doppelkopf_app.game.get_player(token)

@doppelkopf_app.get("/player/pub")
def get_pub_player(table_position:int) -> PlayerPub:
    return doppelkopf_app.game.get_pub_player(table_position)

@doppelkopf_app.get("/table")
def get_table() -> Table:
    return doppelkopf_app.game.get_table()

@doppelkopf_app.post("/table/lay_card")
def lay_card(token:str, card:Card):
    doppelkopf_app.game.lay_card(token, card)
    return {"status": "ok"}

@doppelkopf_app.post("/table/schmeissen")
def schmeissen(token:str) :
    doppelkopf_app.game.schmeissen(token)
    return {"status": "ok"}

@doppelkopf_app.post("/table/vorbehalt")
def say_vorbehalt(token:str, vorbehalt:Vorbehalt) :
    doppelkopf_app.game.vorbehalt(token, vorbehalt)
    return {"status": "ok"}