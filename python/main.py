from fastapi import FastAPI

doppelkopf_app = FastAPI()


@doppelkopf_app.get("/")
async def greeting():
    return {"message": "Welcome to Doppelkopf!"}