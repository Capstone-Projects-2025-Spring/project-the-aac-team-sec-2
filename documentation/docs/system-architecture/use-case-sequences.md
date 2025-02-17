---
sidebar_position: 5
---

# Use Case Sequences
## **Use Case 1 - Start a Lobby**

```mermaid
sequenceDiagram
    participant LobbyCreator as Lobby Creator
    participant WebApplication as Web Application
    participant Backend
    participant OtherPlayers as Other Players

    LobbyCreator->>WebApplication: Accesses the web application
    WebApplication-->>LobbyCreator: Return landing page
    LobbyCreator->>WebApplication: Clicks the "Start Lobby" button
    WebApplication->>Backend: Request unique game code
    Backend-->>WebApplication: Return unique game code
    WebApplication-->>LobbyCreator: Return the lobby leader screen with the unique game code
    LobbyCreator->>OtherPlayers: Shares the game code with external communication
```


## **Use Case 2 - Join a Lobby**

```mermaid
sequenceDiagram
    participant User
    participant WebApplication as Web Application
    participant Backend

    User->>WebApplication: Accesses the web application
    WebApplication-->>User: Return landing page
    User->>WebApplication: Clicks the "Join Game" button
    WebApplication-->>User: Displays game code entry screen
    User->>WebApplication: Enters game code
    User->>WebApplication: Clicks the "Join" button
    WebApplication->>Backend: Validates game code and informs of new player
    Backend-->>WebApplication: Return game details or error
    WebApplication-->>User: Display lobby page
```

## **Use Case 3 - Start a Game**

```mermaid
sequenceDiagram

    participant LobbyCreator as Lobby Creator
    participant WebApplication as Web Application
    participant Backend

    LobbyCreator->>WebApplication: Sees list of players in the lobby
    LobbyCreator->>WebApplication: Clicks the "Start Game" button
    WebApplication->>Backend: Initiates game start
    Backend-->>WebApplication: Return game state and starting hands
    WebApplication-->>LobbyCreator: Displays game page and starting hand
```

## **Use Case 4 - Lobby starts**

```mermaid
sequenceDiagram

    participant User
    participant LobbyLeader as Lobby Leader
    participant WebApplication as Web Application
    participant Backend

    LobbyLeader->>WebApplication: Clicks the "Start Game" button
    WebApplication->>Backend: Initiates game start
    Backend-->>WebApplication: Return game state and starting hands
    WebApplication-->>User: Displays message that game has started
    WebApplication-->>User: Displays game board and starting hand
```
## **Use Case 5 - Take a Card from a Player Successfully**

```mermaid
sequenceDiagram

    participant User
    participant WebApplication as Web Application
    participant Backend
    participant OtherPlayer as Other Player

    User->>WebApplication: Clicks on a card in their hand to select that type
    User->>WebApplication: Clicks on another player's hand to request that type from the player
    WebApplication->>Backend: Update backend on card request
    Backend-->>WebApplication: Return result of request
    WebApplication-->>User: Move requested card(s) from the other player's hand to user's hand
    WebApplication-->>User: Display message confirming result of card request
    WebApplication-->>User: Continue user's turn

```
## **Use Case 6 - Take a Card from a Player and Fail ("Go Fish")**

```mermaid
sequenceDiagram

    participant User
    participant WebApplication as Web Application
    participant Backend
    participant OtherPlayer as Other Player

    User->>WebApplication: Clicks on a card in their hand to select that type
    User->>WebApplication: Clicks on another player's hand to request that type from the player
    WebApplication->>Backend: Update backend on card request
    Backend-->>WebApplication: Return result (player does not have the requested card)
    WebApplication-->>User: Display "Go Fish" message and sound
    WebApplication->>WebApplication: Check if card is available in the deck
    WebApplication-->>User: Give the user a card from the deck (if available)
    WebApplication->>Backend: Update backend on card draw
    WebApplication-->>User: End user's turn automatically

```

## **Use Case 7 - Place a Four-of-a-Kind Set in the Pool Automatically**

```mermaid
sequenceDiagram

    participant User
    participant WebApplication as Web Application
    participant Backend

    User->>WebApplication: Collects four matching cards in their hand
    WebApplication->>Backend: Update backend with the completed set
    WebApplication-->>User: Move four matching cards to the pool
    WebApplication-->>User: Display completed set on the board
    WebApplication-->>User: Display message confirming completed set
```

## **Use Case 8 - Run Out of Cards and Draw More**

```mermaid
sequenceDiagram
    participant User
    participant WebApplication as Web Application
    participant Backend

    User->>WebApplication: Puts down a set or gets cards taken, hand is empty
    WebApplication->>Backend: Update backend with request to draw up to 3 cards
    Backend-->>WebApplication: Return up to 3 cards
    WebApplication-->>User: Show user receiving up to 3 cards
```

## **Use Case 9 - Run Out of Cards Completely**

```mermaid
sequenceDiagram
    participant User
    participant WebApplication as Web Application
    participant Backend

    User->>WebApplication: Puts down a set or gets cards taken, hand is empty
    WebApplication->>Backend: Check if cards are available in the deck
    Backend-->>WebApplication: No cards available in the deck
    WebApplication-->>User: Display message saying no cards available
    WebApplication-->>User: Automatically pass user's turn
```

## **Use Case 10 - Use Game Text Chat**

```mermaid
sequenceDiagram
    participant User
    participant WebApplication as Web Application
    participant Backend

    User->>WebApplication: Clicks the "Chat" button
    WebApplication-->>User: Display chat window
    User->>WebApplication: Starts typing a message
    WebApplication-->>User: Display message as it is being typed
    User->>WebApplication: Clicks the send button
    WebApplication->>Backend: Send message to backend
    Backend-->>WebApplication: Acknowledge message received
    WebApplication-->>User: Display message in chat window
```

## **Use Case 11 - Receive Message in Game Text Chat**

```mermaid
sequenceDiagram
    participant User
    participant WebApplication as Web Application
    participant Backend
    participant Player 2
    participant Player 2 Web Application

    User->>WebApplication: Clicks the "Chat" button
    WebApplication->>Backend: Retrieve previously sent messages
    Backend-->>WebApplication: Return list of previously sent messages
    WebApplication-->>User: Display previously sent messages

    Player 2->>Player 2 Web Application: Starts typing a message
    Player 2 Web Application->>Backend: Notify that Player 2 is typing
    Backend-->>WebApplication: Broadcast that Player 2 is typing
    WebApplication-->>User: Show indicator that Player 2 is typing

    Player 2 Web Application->>Player 2: Clicks the "Send" button
    Player 2 Web Application->>Backend: Sends typed message to backend
    Backend-->>Player 2 Web Application: Acknowledge that the message was received
    Backend-->>WebApplication: Send out Player 2's message to other users
    WebApplication-->>User: Display Player 2's message in chat window
```

## **Use Case 12 - Use the AAC Menu**

```mermaid
sequenceDiagram
    participant User
    participant WebApplication as Web Application
    participant Backend
    participant Other User's Frontend

    User->>WebApplication: Clicks the "AAC Menu" button
    WebApplication-->>User: Display AAC Menu with available phrases/words with pictures
    User->>WebApplication: Selects a phrase or word from the menu
    WebApplication->>Backend: Send selected phrase or word
    Backend-->>WebApplication: Acknowledge selected phrase or word
    WebApplication-->>User: Display selected phrase or word in the chat
    Backend->>Other User's Frontend: Broadcast selected phrase to other users
    WebApplication-->>User: Play the phrase out loud
```

## **Use Case 13 - Receive AAC Communication**

```mermaid
sequenceDiagram
    participant User as User
    participant WebApplication as Web Application
    participant Backend
    participant OtherUsersWebApplication as Other User's Web Application
    participant OtherUser as Other User

    OtherUser->>OtherUsersWebApplication: Selects AAC phrase or word
    OtherUsersWebApplication->>Backend: Sends selected AAC phrase or word
    Backend-->>WebApplication: Broadcasts AAC phrase or word
    WebApplication-->>User: Displays selected phrase or word in the chat
    WebApplication-->>User: Plays the phrase or word out loud
```

## **Use Case 14 - Win the Game**

```mermaid
sequenceDiagram
    participant User
    participant WebApplication as Web Application
    participant Backend

    User->>WebApplication: Places second four-of-a-kind set in the pool
    WebApplication->>Backend: Update backend with the completed set
    Backend-->>WebApplication: Acknowledge the second completed set and game result
    WebApplication-->>User: Display message indicating user won
    WebApplication-->>User: Display end game screen
```

## **Use Case 15 - End the Game When Only One Player Can Move**

```mermaid
sequenceDiagram
    participant User
    participant WebApplication as Web Application
    participant Backend

    WebApplication->>Backend: Check if only one player can move
    Backend-->>WebApplication: Confirms only one player can move and that the game is over
    WebApplication-->>User: Display message indicating game is over
    WebApplication-->>User: Display message showing the winner
```
