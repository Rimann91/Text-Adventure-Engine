class UserInfo:
    INTRODUCTION = "Welcome to Adventure!! This game is called a 'text adventure' game. It is one of the original styles of video game. There are no graphics, only text. You will interact with the world simply by typing in commands and reading the output. Move to different locations using the cardinal directions. To see a list of verbs that are understood, simply type in 'verbs', 'commands', or 'help'. Exit the game at any time by typing 'quit'. Lets begin! but first, "
    RULES = ""


class DefaultResponse:
    # responses for the player.take(method)
    wont_move = "hnnng.... the thing doesn't budge" 
    max_inventory = "ypu don't have anymore room, maybe drop something" 
    unlock = "it unlocks"
    nothing_interesting = "nothing interesting happens"


pause_time = 0.5
starting_location = "Front Porch"
max_inventory = 4


