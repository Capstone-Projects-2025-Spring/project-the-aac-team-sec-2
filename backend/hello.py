from typing import Union

from fastapi import FastAPI

import random

from .models import Lobby, Player

app = FastAPI()

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

            game.players[id].cards.append(random_card)

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
