---
sidebar_position: 2
---

# System Block Diagram

![C4 Container Diagram](../../static/img/c4-container.png)

## Web Application

Responsible for:

* Maintaining game session state, e.g. player hands, completed sets, draw pile.
* Broadcasting chat messages to all players. Messages sent by one player are delivered to the others.

## Single Page Application

Game runs here. Responsible for:

* Implementing game logic. Game rules should be validated, etc.
* Implementing AAC functionality.
* Sending chat and game updates to **Web Application**.