from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
import random

from lobby import Lobby
from player import Player

app = FastAPI()

lobbies = {}
animals = ["Turtle","Shark","Fish"]

def generate_unique_code():
    while True:
        code = '-'.join(random.choices(animals,k=3))
        if code not in lobbies:
            return code

@app.post("/create_lobby")
def create_lobby():
    code = generate_unique_code()
    lobbies[code] = {"players": []}
    return {"code":code}   

@app.get("/lobby/{code}")
def get_lobby(code: str):
    lobby = lobbies.get(code)
    if lobby is None:
        return {"error": "Lobby not found"}
    return {"code": code, "players": lobby["players"]}    
          

@app.get("/testGameState/")
async def test_game_state():
    # create lobby
    game = Lobby(id=0)

    # add players to lobby
    player1 = Player(id=1,name="player 1")
    game.players[player1.id] = player1
    game.player_count += 1
    player2 = Player(id=2,name="player 2")
    game.players[player2.id] = player2
    game.player_count += 1

    # give each player 7 cards
    for i in range(7):
        for id in game.players:
            random_card = random.choice(game.deck)
            game.deck.remove(random_card)
            game.deck_size -= 1

            game.players[id].cards.append(random_card)
            game.players[id].card_count += 1

    # start game
    game.started = True
    game.current_turn = player1.id

    return game

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
