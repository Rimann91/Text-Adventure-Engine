from adventure import *
import traceback
game = Game("Adventure")
## TEST GAME CALL
log(" "+"="*100 +"\n---START RUNNING---")
def build():

    # Define game locations (map)
    front_porch = game.new_location(
            "Front Porch",
            "You are on a porch to a house, there is a door to your north, a staircase decends to the street",
            )
    sitting_room = game.new_location(
            "Sitting Room",
            "You are in the first room of the house, a sofa and a chair are in the middle of the room, a bookshelf is on the wall, to your South the front door. And to the east a staircase. A radio sits on a table in the corner",
            )
    sidewalk = game.new_location(
        "sidewalk",
        "perhaps try going back to the house"
    )
    attic = game.new_location(
        "attic",
        "it is dark, but your lamp illuminates the small musty space. through a small vent in the west side of the attic, you can just make out the door of a cellar"
    )
    west_of_house = game.new_location(
        "west of house",
        "You are on the west side of the house, there is nothing but a locked cellar door"
    )
    tunnel = game.new_location(
        "tunnel",
        "This is a long dim passageway, the passage extends straight south with no end in sight"
    )
    cavern = game.new_location(
        "cavern",
        "A large damp cavern. There are several passages leading out of here. One to the north east, one to the southeast, a larger passageway directly to the west, and a deep hole that dissapears in darkeness."
    )
    bottom_of_pit = game.new_location(
        "Bottom of Pit",
        "This is the bottom of a muddy pit"
    )

    # TODO[] names of items can not currently contain spaces, fix this. Unable to give descriptive names
    key = Item("key", "a small dull gray key")
    fmap = Item("map", "an unreadable map")
    knife = Item("knife", "a rusty shank")
    apple = Item("apple", "a bright red apple")
    lamp = Item("lamp", "a small source of light")
    rope = Item("rope", "a thick and sturdy cordage, perfect for binding or climbing")
    sword = Item("sword", " an impressive hand forged short sword")

    chest = Container("chest", "an old oak chest bound together with solid steel", True, False)
    chest.set_fixed()
    chest.contents["sword"] = sword
    chest.state_switch_feedback = ("open", "closed")

    front_porch.new_connection([NORTH], sitting_room)
    front_porch.new_connection([SOUTH], sidewalk)
    front_porch.add_item(fmap)
    front_porch.add_item(apple)

    sidewalk.new_connection([WEST], west_of_house)

    sitting_room.new_connection([EAST, UP], attic)
    sitting_room.add_item(knife)
    sitting_room.add_item(lamp)
    attic.add_item(key)
    attic.add_item(rope)
    attic.add_requirement(lamp)

    west_of_house.new_connection([DOWN], tunnel)

    tunnel.new_connection([SOUTH], cavern)
    tunnel.add_requirement(key)
    tunnel.add_requirement(lamp)

    cavern.new_connection([DOWN], bottom_of_pit)
    #cavern.new_connection()
    #cavern.new_connection()
    cavern.add_item(rope)

    bottom_of_pit.add_item(chest)
    bottom_of_pit.add_requirement(rope)

    game.start_location = "Front Porch"

def main():

    log("BUILDING GAME")
    try:
        build()
        log("GAME BUILD SUCCESSFULL")
    except:
        print("Unexpected Error: problem in main.py with build() function")
        log("Unexpected Error: problem in main.py with build() function\n"+traceback.format_exc())
        raise

    log("STARTING GAME")
    try:
        game.run()
    except:
        print("WARNING: An unexpected error occured. Check the runtime log for traceback")
        log("An unexpected error occured\n"+traceback.format_exc())
        raise
    log("GAME CLOSED")

main()
