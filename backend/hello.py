import asyncio
import random
from typing import Annotated

from fastapi import Depends, FastAPI, WebSocket

from .dependencies import event_queue
from .gofish import game_loop
from .models import Lobby, Message, MessageKind, Player, QueryResponse

app = FastAPI()

lobbies = {}
running_games = set()
animals = ["Fish", "Turtle", "Shark"]


def generate_unique_code():
    while True:
        code = "-".join(random.choices(animals, k=3))
        if code not in lobbies:
            return code


@app.post("/create_lobby")
def create_lobby():
    code = generate_unique_code()
    lobbies[code] = {"players": []}
    return {"code": code}


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
    player1 = Player(id=1, name="player 1")
    game.players[player1.id] = player1
    game.player_count += 1
    player2 = Player(id=2, name="player 2")
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


@app.websocket("/gofish")
async def event_input(websocket: WebSocket, queue: Annotated[asyncio.Queue[tuple[int, str]], Depends(event_queue)]):
    """Websocket endpoint for game and chat messages."""
    await websocket.accept()

    while True:
        t = await websocket.receive_text()
        await queue.put((id(websocket), t))


@app.post("/start")
async def start():
    """Starts the game."""
    task = asyncio.create_task(asyncio.to_thread(game_loop(...)))  # pyright: ignore
    running_games.add(task)
    task.add_done_callback(running_games.discard)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_text()

        try:
            message = Message.parse_raw(data)
        except Exception as e:
            await websocket.send_text(f"[Server] Error: {e!s}")
        else:
            match message.data.type:
                case MessageKind.query:
                    query = message.data
                    response = QueryResponse(type=MessageKind.query_response, count=2)
                    await websocket.send_text(
                        f"[Server] Query received for player {query.target_player_id}, card {query.card}. Responding with count: {response.count} (placeholder)"
                    )

                case MessageKind.chat:
                    chat = message.data
                    await websocket.send_text(
                        f"[Server] Chat received from player {message.source_player_id}: {chat.message}"
                    )

                case _:
                    await websocket.send_text("[Server] Unknown message type received.")
