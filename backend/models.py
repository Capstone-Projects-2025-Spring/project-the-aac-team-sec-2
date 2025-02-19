from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field


def make_deck(x):
    """
    Makes a deck composing of x of each card

    Parameters:
        x (int): The amount of each card to add to deck
    """
    # Single character representation of a deck of cards, no suits
    cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]

    # Add x of each card to deck
    deck = []

    for card in cards:
        for i in range(x):
            deck.append(card)

    return deck


class Lobby(BaseModel):
    """
    A class representing a game state

    Attributes:
        id (int): The lobby's internal ID
        code (str): The code used to join the lobby
        players (dict): A list of player objects participating in the game
        player_count (int): Number of players in game, max 4

        started (bool): Whether the game has started

        current_turn (int): The ID of the player whose turn it current is

    Methods:
        get_deck_count(): Returns size of the deck
    """

    id: int
    code: str = "ABC"
    players: dict = dict()
    player_count: int = 0

    started: bool = False

    current_turn: int = -1
    deck: list[str] = make_deck(4)

    def get_deck_count(self):
        return len(self.deck)


class Player(BaseModel):
    """
    A class representing a player's ingame data

    Attributes:
        id (int): The player's internal ID
        code (str): The code used to join the game
        socket (): TODO: A web socket object (this is probably its own class idk yet)

        cards (list[str]): A list of cards this player has, private
        books (list[str]): A list of books this player has, visible to other players

    Methods:
        get_card_count(): Returns player's hand size
    """

    id: int
    name: str = "Unnamed Player"
    socket: None = None

    cards: list[str] = []
    books: list[str] = []

    def get_card_count(self):
        return len(self.cards)


class MessageKind(StrEnum):
    """Enum for different message kinds."""

    query = "query"
    query_response = "query_response"
    chat = "chat"


class Query(BaseModel):
    """
    Represents the action of a player asking for a card.

    Attributes:
        target_player_id: The id of the player being asked for cards.
    """

    type: Literal[MessageKind.query]
    target_player_id: int
    card: int


class QueryResponse(BaseModel):
    """
    The server response to a player query.

    Attributes:
        count: Non-negative number of cards the target player had.
    """

    type: Literal[MessageKind.query_response]
    count: int


class Chat(BaseModel):
    """
    Represents a chat message from a player.

    Attributes:
        message: The message.
    """

    type: Literal[MessageKind.chat]
    message: str


class Message(BaseModel):
    """
    Represents a generic message.

    Attributes:
        source_player_id: The id of the player that sent this message.
    """

    data: Query | QueryResponse | Chat = Field(discriminator="type")
    source_player_id: int
