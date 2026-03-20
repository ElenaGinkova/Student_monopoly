# Student Monopoly

## Overview

**Student Monopoly** is a Python-based multiplayer board game inspired by the classic Monopoly formula and reimagined around student life. The game is designed for **two to three players** and combines traditional board game mechanics with original rules, character abilities, random events, and student-themed locations.

Each player starts with the same amount of money but has a **unique special ability** that can influence the game in different ways. The main objective is to become the wealthiest player by the end of the game while managing budget, health, diplomas, and other gameplay effects.

Unlike traditional Monopoly, this project introduces new mechanics such as traps, negative and positive random events, player attacks, temporary rule changes, reverse movement, custom fields, and more dynamic interactions between players.

## Features

- Multiplayer gameplay for **2 to 3 players**
- **11x11 board**
- Student-life-inspired gameplay and locations
- Unique playable characters with **special abilities**
- Traditional and custom field types
- Randomized dice mechanics with additional rules
- Budget and health management
- Coursework project evaluation and game progression logic
- Visual representation built with **Pygame**

## Gameplay

Players move across the board and interact with different types of fields. Some fields follow mechanics similar to classic Monopoly, while others introduce completely new effects based on student life.

At the beginning of each turn, the player may choose to activate special gameplay options before rolling the dice, such as using a character ability, applying a Mystery Shot, or spending a diploma bonus. Each of these actions can be used according to the game’s turn limitations.

### Field Types

#### Classic-inspired fields
- **Pocket Money from Home** – starting tile that provides bonus money
- **Properties** – purchasable locations such as student-themed buildings and places
- **Try Your Luck** – draw a random chance card
- **Yellow Book** – equivalent of jail
- **Dormitory / Apartment** – equivalent of houses/hotels

#### Custom fields
- **8th of December** – a trap that removes a significant amount of money and applies a two-turn cooldown
- **Exam** – asks a question that can lead to a positive or negative outcome
- **UNWE** – grants +1 diploma
- **Student Canteen** – may increase or decrease health depending on luck
- **Exe** – reverses player movement until they return to the starting tile
- **Erasmus** – teleports the player to a random tile and grants a budget bonus
- **Student Radio** – spreads a rumor that changes the rules of the game for all players for three turns

## Player Attributes

Each player has the following attributes:

- **Budget**
- **Health**
- **Special ability**
- **Diplomas**
- **Mystery Shots**

### Available Characters

- **BookWorm** – challenges another player to a dice duel. The other player choses amount of money to gamble.
- **CaffeineAddict** – can gain extra energy by drinking coffee - rolls an additional die
- **CleaningLady** - can move a player one field forward or backwards
- **GirlsMagnet** – distracts opponents and causes them to lose a turn. Can use this power once in 3 turns
- **Librarian** – can silence someone, who needs to roll dice. for result 1–6 they loose on eturn because of the strict order. otherwise they continue
- **NightLife** – receives more Mystery Shots
- **Roommate** – manipulates a player, decides that they want to "reorder the furniture" and they switch places with the player
- **TicketChecker** – can charge another player 50lv 
- **Tutor** – decreases the mood of all student players by introducing an extra test
  
## Dice Mechanics

The game uses randomized dice with an additional special rule:

- If a player rolls any other pair, they receive a **Mystery Shot**

## Additional Rules

- A player may use at most:
  - **one Mystery Shot**
  - **one diploma**
  - **one special ability**
  during a single turn
- A field can be marked as **Reserved**, making its effect inactive for other players until it is passed again
- A player loses the game if they:
  - run out of health
  - go bankrupt

## Technologies Used

- **Python**
- **Pygame**
- Built-in Python modules

## Project Goals

This project focuses on:

- object-oriented design
- game loop implementation
- player interaction
- random event handling
- creating a more dynamic and humorous alternative to classic Monopoly

## How to Run

To start the game, run:

```bash
python -m Monopoly.main
```

To start the tests, run:

```bash
python -m unittest discover test
```
