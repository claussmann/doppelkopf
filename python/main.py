from fastapi import FastAPI, HTTPException
from game import Game

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