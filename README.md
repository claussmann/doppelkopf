# Doppelkopf
An API with which you can play the card game "Doppelkopf"


## How to start?

Assuming you have Python 3 installed, you first need to create a virtual environment:
`python -m venv env`

Activate the virtual environment with
`source env/bin/activate`

Install the dependencies:
`pip install -r requirements.txt`

Start the app:
`cd python; uvicorn main:doppelkopf_app`

Swagger UI will be available at
`http://127.0.0.1:8000/docs#/`