from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, WebSocket
from models import Message, MessageKind, QueryResponse, Lobby, Player

import random

app = FastAPI()

lobbies = {}
animals = ["Fish","Turtle","Shark"]

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

@app.post("/lobby/{code}/join")
def join_lobby(code:str, player:str):
    lobby = lobbies.get(code)
    if lobby is None:
        return {"error": "Lobby not found"}
    lobby["players"].append(player)
    return {"code":code, "players":lobby["players"]}

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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_text()

        try:
            message = Message.parse_raw(data)
        except Exception as e:
            await websocket.send_text(f"[Server] Error: {str(e)}")
        else:
            match message.data.type:
                case MessageKind.query:
                    query = message.data
                    response = QueryResponse(type=MessageKind.query_response, count=2)
                    await websocket.send_text(f"[Server] Query received for player {query.target_player_id}, card {query.card}. Responding with count: {response.count} (placeholder)")
                
                case MessageKind.chat:
                    chat = message.data
                    await websocket.send_text(f"[Server] Chat received from player {message.source_player_id}: {chat.message}")
                
                case _:
                    await websocket.send_text("[Server] Unknown message type received.")

                
