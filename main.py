from adventure import *
import sys
## TEST GAME CALL
def main():
    game = Game("Adventure")

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

    key = Item("key", "a small dull gray key")
    fmap = Item("map", "an unreadable map")
    knife = Item("knife", "a rusty shank")
    apple = Item("apple", "a bright red apple")
    lamp = Item("lamp", "a small source of light")

    front_porch.new_connection([NORTH], sitting_room)
    front_porch.new_connection([SOUTH], sidewalk)
    front_porch.add_item(fmap)
    front_porch.add_item(apple)

    sidewalk.new_connection([WEST], west_of_house)

    sitting_room.new_connection([EAST, UP], attic)
    sitting_room.add_item(knife)
    sitting_room.add_item(lamp)

    attic.add_item(key)
    attic.add_requirement([lamp])

    west_of_house.new_connection([DOWN], tunnel)

    tunnel.add_requirement([lamp, key])

    game.start_location = "Front Porch"

    try:
        game.run()
    except:
        print("An unexpected error occured:", sys.exc_info()[0])
        log("Unhandled Exception:\n" + sys.exc_info()[0])


main()
