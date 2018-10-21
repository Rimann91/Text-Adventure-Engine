from adventure import *
import config
import traceback
## TEST GAME CALL
log(" "+"="*100 +"\n---START RUNNING---")


print(config.UserInfo.INTRODUCTION)
user_name = str(input("What is your name? --> "))
player = Player(user_name)
print("Glad to have you {} .... ".format(user_name))
pause()
print("GOOD LUCK !")
log("USERNAME: " + player.user_name)
game = Game("Adventure", player)
#current_location = player.set_location(self.locations[config.starting_location], None)[0]
pause()

def chest_gets_opened():
    game.event_output = "The chest creaks open"
    

def unlock_front_door():
    game.event_output = "click... it unlocked"

def build():

    # Define game locations (map)
    front_porch = game.new_location(
            "Front Porch",
            "You are on a porch to a house",
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


        
    
    chest.on_state_true(chest_gets_opened)

    # FRONT PORCH
    front_porch.add_item(fmap)
    front_porch.add_item(chest)
    front_door = Obstacle("door", " a normal door with a bolt lock", state = False)
    front_door.locked = True
    front_door.locked_response = "It's locked, I wonder if there is a key"
    front_door.on_unlocked(unlock_front_door)
    front_door.state_switch_feedback = ("open", "closed")
    cnct_sitting_room = Connection([NORTH], front_porch, sitting_room, "front door to the house", front_door)
    cnct_sidewalk = Connection([SOUTH], front_porch, sidewalk, "set of steps leading off the porch")

    # SITTING ROOM
    sitting_room.add_item(knife)
    sitting_room.add_item(lamp)
    cnct_attic = Connection([UP, EAST], sitting_room, attic, "stairs leading up")

    # ATTIC
    attic.add_item(key)
    attic.add_item(rope)
    attic.add_requirement(lamp)

    # SIDEWALK - WEST OF HOUSE
    
    cellar_door = Obstacle("door", "a sturdy old door covering an entrance into the ground", state = False)
    cellar_door.state_switch_feedback = ("open", "closed")
    cnct_west_of_house = Connection([WEST], sidewalk, west_of_house, "pathway")
    cnct_tunnel = Connection([DOWN], west_of_house, tunnel, "a sturdy cellar door", obstacle = cellar_door)
    #west_of_house.new_connection([DOWN], tunnel)

    #tunnel.new_connection([SOUTH], cavern)
    tunnel.add_requirement(key)
    tunnel.add_requirement(lamp)

    #cavern.new_connection([DOWN], bottom_of_pit)
    #cavern.new_connection()
    #cavern.new_connection()
    cavern.add_item(rope)

    bottom_of_pit.add_item(chest)
    bottom_of_pit.add_requirement(rope)

    #game.start_location = "Front Porch"

    #current_location = player.set_start_location(game.locations[config.starting_location])
    game.current_location = front_porch

