---
sidebar_position: 1
---

# System Overview
## Project Abstract
This project offers an interactive and accessible social experience for children in elementary school who struggle with verbal communication. Users will be able to participate in a game of “Go Fish” with their peers while having AAC communication available to them. Each user will take turns until the game is complete and one of the users has won. The game can be played between multiple devices, as long as each user has access to a web browser. There are two modes, one for children who require AAC communication, and one for children who do not. The game will show the AAC communication while it is in progress to build empathy. The goal of this project is to provide a seamless and interactive experience for children regardless of their ability to communicate verbally.

## Conceptual Design
The game will be played on two to four separate devices. One player will host the game and others can join using a unique code. The frontend will be built using React.js, which will be used to build and manage the game components. The backend will be built using Python, which will be used to store game identifiers and connections and the state of the game and its logic. FastAPI will be used to process requests between the frontend and backend.

## Background
The system used to connect devices together will mirror what is used by Kahoot. Specifically, the creation of the unique code to connect to a game session through a web browser. The game will also abide by AAC system design guidelines and principles, as well as prior research on AAC communication. This includes the use of grid displays, a commonly used tool that creates sentences for people who struggle with verbal communication. This is also why AAC communication is shown in real time in order to build empathy between students.
