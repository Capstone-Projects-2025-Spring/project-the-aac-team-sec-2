---
sidebar_position: 2
---

# Component Overview

Describes component functionality, their interfaces, and how they fit together. The system block diagram provides an overview (see [system block diagram](../requirements/system-block-diagram.md)).

## Web Application (FastAPI)

Handles game state, lobby creation, and chat. Issues state updates to the Single Page Application.

### External Interface

* HTTP - Creating and joining lobbies.
* WSS - Used for game state updates (whose turn, player queries, etc.) and chat.

#### HTTP

* `POST /create` - Initialize game state, creates randomized lobby code.
* `POST /join` - Users specify a game code for a lobby to join.
* `POST /start` - Starts the game. Only available to users that have created a lobby.

#### WSS

Protocol for WSS messages.

```json
{
  "$defs": {
    "Chat": {
      "description": "Represents a chat message from a player.",
      "properties": {
        "type": {
          "const": "chat",
          "title": "Type",
          "type": "string"
        },
        "message": {
          "title": "Message",
          "type": "string"
        }
      },
      "required": [
        "type",
        "message"
      ],
      "title": "Chat",
      "type": "object"
    },
    "Query": {
      "description": "Represents a player asking for a card.",
      "properties": {
        "type": {
          "const": "query",
          "title": "Type",
          "type": "string"
        },
        "target_player_id": {
          "title": "Target Player Id",
          "type": "integer"
        },
        "card": {
          "title": "Card",
          "type": "integer"
        }
      },
      "required": [
        "type",
        "target_player_id",
        "card"
      ],
      "title": "Query",
      "type": "object"
    },
    "QueryResponse": {
      "description": "The server response to a player query.",
      "properties": {
        "type": {
          "const": "query_response",
          "title": "Type",
          "type": "string"
        },
        "count": {
          "title": "Count",
          "type": "integer"
        }
      },
      "required": [
        "type",
        "count"
      ],
      "title": "QueryResponse",
      "type": "object"
    }
  },
  "description": "Represents a generic message.",
  "properties": {
    "data": {
      "discriminator": {
        "mapping": {
          "chat": "#/$defs/Chat",
          "query": "#/$defs/Query",
          "query_response": "#/$defs/QueryResponse"
        },
        "propertyName": "type"
      },
      "oneOf": [
        {
          "$ref": "#/$defs/Query"
        },
        {
          "$ref": "#/$defs/QueryResponse"
        },
        {
          "$ref": "#/$defs/Chat"
        }
      ],
      "title": "Data"
    },
    "source_player_id": {
      "title": "Source Player Id",
      "type": "integer"
    }
  },
  "required": [
    "data",
    "source_player_id"
  ],
  "title": "Message",
  "type": "object"
}
```

## Single Page Application (React)

Two-way communication of moves and chat messages between client and server. Communicates with the FastAPI backend via common WebSocket protocol. Currently, no functionality with HTTP endpoints.
