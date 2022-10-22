from tokenize import String
from pymongo import MongoClient
from pprint import pprint
import pandas as pd
import json
import os

#-------------------------------#
#--------Initialization---------#
#-------------------------------#

##initialize connection to the database (will not exist until something is loaded into it)
client = MongoClient("localhost", 27017)
db = client["mtgdb"]
collection = db["cards"]

#check if database is already loaded
is_loaded = False
dbnames = client.list_database_names()
if 'mtgdb' in dbnames:
    is_loaded = True

#-------------------------------#
#-----------Functions-----------#
#-------------------------------#

#print logo (only at the start)
def print_logo():
    print("""
  __  __ _____ ____       _       _        _                    
 |  \/  |_   _/ ___|   __| | __ _| |_ __ _| |__   __ _ ___  ___ 
 | |\/| | | || |  _   / _` |/ _` | __/ _` | '_ \ / _` / __|/ _ \ 
 | |  | | | || |_| | | (_| | (_| | || (_| | |_) | (_| \__ \  __/
 |_|  |_| |_| \____|  \__,_|\__,_|\__\__,_|_.__/ \__,_|___/\___|
""")

#print menu (after every command)
def print_menu():
    print("""
_________________________________________________________________
| 0 | Exit
| 1 | Load database
| 2 | Count cards in the database
| 3 | Add a new card
| 4 | Remove existing card
| 5 | Search card by name
| 6 | Filter cards by maximum mana cost and color
| 7 | Retrieves the top 5 cards by power
| 8 | Find card from description
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
""")

#clear the terminal for a clean view (platform indipendent)
def clear_terminal():
    os.system('cls||clear')

#1 - Load database
def load_db():
    with open("StandardCards.json") as json_db:
        database = json.load(json_db)
    collection.insert_one(database)

#2 - Count cards in the database
def print_n_cards():
    cards = collection.aggregate([
        {"$project":
            {"cards":
                {"$map":
                    {
                        "input": {"$objectToArray": "$cards"},
                        "in": "$$this.v"
                    }
                }
            }
        },
        {"$unwind": "$cards"},
        { "$group": { "_id": "$name" , "count": { "$sum": 1 } } },
    ])

    print("\n| Number of cards in the database: " +  str(cards.next()["count"]))
1
#3 - Add a new card
def add_card(name, mana, power, colors, type, text):
    collection.update_one({},{"$set":{"cards." + name:{"name": name, "convertedManaCost": float(mana), "power":power, "colors": colors, "type": type, "text": text}}})

#4 - Remove existing card
def remove_card(name):
    collection.update_one({},{"$unset":{"cards." + name:""}})


#5 - Search card by name
def search_card(name):
    cards = collection.aggregate([
        {"$project":
            {"cards":
                {"$map":
                    {
                        "input": {"$objectToArray": "$cards"},
                        "in": "$$this.v"
                    }
                }
            }
        },
        {"$unwind": "$cards"},
        {"$match": {"cards.name": name}},
        {"$project":
            {
                "_id": 0,
                "cards.name": 1,
                "cards.convertedManaCost": 1,
                "cards.power":1,
                "cards.colors": 1,
                "cards.type": 1,
                "cards.text": 1
            }
        },
        {"$sort": {"cards.name": 1, "cards.convertedManaCost":1}},
    ])

    try:
        print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
        print(pd.DataFrame(cards.next()))
    except:
        print("| Card '" + name + "' not found")

#6 - Filter cards by maximum mana cost and color
def filter_cards(mana, colors):
    cards = collection.aggregate([
        {"$project":
            {"cards":
                {"$map":
                    {
                        "input": {"$objectToArray": "$cards"},
                        "in": "$$this.v"
                    }
                }
            }
        },
        {"$unwind": "$cards"},
        {"$match": {"$and": [{"cards.convertedManaCost": {"$lte": float(mana)}}, {"cards.colors": colors}]}},
        {"$sort": {"cards.name": 1, "cards.convertedManaCost":1}},
        {"$project":
            {
                "_id": 0,
                "cards.name": 1,
                "cards.convertedManaCost": 1,
                "cards.power":1,
                "cards.colors": 1,
                "cards.type": 1,
                "cards.text": 1
            }
        }
    ])

    for card in cards:
        print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
        print(pd.DataFrame(card))

#7 - Retrieves the top 5 cards by power
def filter_top():
    cards = collection.aggregate([
        {"$project":
            {"cards":
                {"$map":
                    {
                        "input": {"$objectToArray": "$cards"},
                        "in": "$$this.v"
                    }
                }
            }
        },
        {"$unwind": "$cards"},
        {"$project":
            {
                "_id": 0,
                "cards.name": 1,
                "cards.convertedManaCost": 1,
                "cards.power":1,
                "cards.colors": 1,
                "cards.type": 1,
                "cards.text": 1
            }
        },
        {"$sort": {"cards.power":-1}},
        {"$limit": 5}
    ])

    for card in cards:
        print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
        print(pd.DataFrame(card))

#8 - Find card from description
def find_description(text):
    cards = collection.aggregate([
        {"$project":
            {"cards":
                {"$map":
                    {
                        "input": {"$objectToArray": "$cards"},
                        "in": "$$this.v"
                    }
                }
            }
        },
        {"$unwind": "$cards"},
        {"$match": {"cards.text": {"$regex" : text}}},
        {"$project":
            {
                "_id": 0,
                "cards.name": 1,
                "cards.convertedManaCost": 1,
                "cards.power":1,
                "cards.colors": 1,
                "cards.type": 1,
                "cards.text": 1
            }
        },
        {"$sort": {"cards.name": 1, "cards.convertedManaCost":1}}
    ])

    for card in cards:
        print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
        print(pd.DataFrame(card))

#-------------------------------#
#-------------Start-------------#
#-------------------------------#

choice = -1

clear_terminal()
print_logo()

while choice != 0:
    print_menu()
    choice = input(">> ")

    if choice == "0": #0 - Exit
        clear_terminal()
        print_logo()
        print("\n| Closing MTG database...\n")
        break

    elif choice == "1": #1 - Load database
        clear_terminal()

        if is_loaded == False:
            load_db()
            is_loaded = True
            print("\n| Database loaded")
        else:
            print("\n| Database already loaded")

    elif choice == "2": #2 - Count cards in the database
        clear_terminal()

        if is_loaded == False:
            print("\n| No database found. Load it first with '1'")
        else:
            print_n_cards()

    elif choice == "3": #3 - Add a new card
        clear_terminal()
        if is_loaded == False:
            print("\n| No database found. Load it first with '1'")
        else:
            print("| Insert the name:")
            name = input("| >> ")

            print("| Insert the mana cost:")
            mana = input("| >> ")

            print("| Insert the power:")
            power = input("| >> ")

            print("| Insert the colors (separated by a comma ','):")
            colors = input("| >> ")
            colors = colors.split(",")

            print("| Insert the type:")
            type = input("| >> ")

            print("| Insert the text:")
            text = input("| >> ")

            add_card(name, mana, power, colors, type, text)

            print("| Card added")
    
    elif choice == "4": #4 - Remove existing card
        clear_terminal()

        if is_loaded == False:
            print("\n| No database found. Load it first with '1'")
        else:
            print("| Insert the card name:")
            name = input("| >> ")
        
            remove_card(name)

            print("| Card removed")

    elif choice == "5": #5 - Search card by name
        clear_terminal()

        if is_loaded == False:
            print("\n| No database found. Load it first with '1'")
        else:
            print("| Insert the card name:")
            name = input("| >> ")

            search_card(name)

    elif choice == "6": #6 - Filter cards by maximum mana cost and color
        clear_terminal()

        if is_loaded == False:
            print("\n| No database found. Load it first with '1'")
        else:
            print("| Insert the mana cost:")
            mana = input("| >> ")

            print("| Insert the colors (separated by a comma ','):")
            colors = input("| >> ")
            colors = colors.split(",")

            filter_cards(mana, colors)

    elif choice == "7": #7 - Retrieves the top 5 cards by power
        clear_terminal()

        if is_loaded == False:
            print("\n| No database found. Load it first with '1'")
        else:
            filter_top()

    elif choice == "8": #8 - Find card from description
        clear_terminal()

        if is_loaded == False:
            print("\n| No database found. Load it first with '1'")
        else:
            print("| Insert the word to search:")
            text = input("| >> ")

            find_description(text)

    else: #Any other character - Wrong input
        clear_terminal()
        print("\n| No command associated with key " + str(choice) + ".")
