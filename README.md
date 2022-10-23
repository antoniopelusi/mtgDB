# mtgDB
A Magic The Gathering database manager

## Installation
- Install [MongoDB](https://www.mongodb.com/try/download/community-edition)
- Install [Python](https://www.python.org/downloads/)
- Install Pymongo: ```pip install pymongo```
- Install Pandas: ```pip install pandas```

## Run
Work on all Operative Systems
- Start MongoDB service: ```service mongod start```
- Move to the **/mtgb** directory
- Run: ```python3 mtgdb.py```

## Commands
- **|  0  |** Exit
- **|  1  |** Load database
- **|  2  |** Count cards in the database
- **|  3  |** Add a new card
- **|  4  |** Remove existing card
- **|  5  |** Search card by name
- **|  6  |** Filter cards by maximum mana cost and color
- **|  7  |** Retrieves the top 5 cards by power
- **|  8  |** Find card from description
- **|  9  |** Check card legalities in a certain format
- **| 10  |** Drop database
