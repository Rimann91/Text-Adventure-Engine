from time import sleep
import config 
import datetime


# A "direction" is all the ways you can describe going some way
directions = {}
direction_name = {}

# These are code-visible canonical names for directions for adventure authors
NORTH = 1
SOUTH = 2
EAST = 3
WEST = 4
UP = 5
DOWN = 6
RIGHT = 7
LEFT = 8
IN = 9
OUT = 10
FORWARD = 11
BACK = 12
NORTH_WEST = 13
NORTH_EAST = 14
SOUTH_WEST = 15
SOUTH_EAST = 16
NOT_DIRECTION = -1

# map direction names to direction numbers
def define_direction( number, name ):
  # check to see if we are trying to redefine an existing direction
  if name in directions:
    print(name, "is already defined as,", directions[name])
  directions[name] = number
  if not number in direction_name or (len(direction_name[number]) < len(name)):
    direction_name[number] = name

# define player words used to describe known directions
define_direction( NORTH, "north" )
define_direction( NORTH, "n" )
define_direction( SOUTH, "south" )
define_direction( SOUTH, "s" )
define_direction( EAST, "east" )
define_direction( EAST, "e" )
define_direction( WEST, "west" )
define_direction( WEST, "w" )
define_direction( UP, "up" )
define_direction( UP, "u" )
define_direction( DOWN, "down" )
define_direction( DOWN, "d" )
define_direction( RIGHT, "right" )
define_direction( LEFT, "left" )
define_direction( IN, "in" )
define_direction( OUT, "out" )
define_direction( FORWARD, "forward" )
define_direction( FORWARD, "fd" )
define_direction( FORWARD, "fwd" )
define_direction( FORWARD, "f" )
define_direction( BACK, "back" )
define_direction( BACK, "bk" )
define_direction( BACK, "b" )
define_direction( NORTH_WEST, "nw" )
define_direction( NORTH_EAST, "ne" )
define_direction( SOUTH_WEST, "sw" )
define_direction( SOUTH_EAST, "se" )


articles = ['a', 'an', 'the']

# changes "lock" to "a lock", "apple" to "an apple", etc.
# note that no article should be added to proper names; store
# a global list of these somewhere?  For now we'll just assume
# anything starting with upper case is proper.
# Do not add an article to plural nouns.
def add_article ( name ):
  # simple plural test
  if len(name) > 1 and name[len(name)-1] == 's' and name[len(name)-2] != 's':
    return name
  consonants = "bcdfghjklmnpqrstvwxyz"
  vowels = "aeiou"
  if name and (name[0] in vowels):
     article = "an "
  elif name and (name[0] in consonants):
     article = "a "
  else:
     article = ""
  return "%s%s" % (article, name)


def remove_superfluous_input(text):
  superfluous = articles +  ['to', 'using', 'with', 'on', 'at']
  rest = []
  for word in text.split():
    if word not in superfluous:
      rest.append(word)
  return ' '.join(rest)


def proper_list_from_dict( d ):
  names = list(d.keys())
  buf = []
  name_count = len(names)
  for (i,name) in enumerate(names):
    if i != 0:
      buf.append(", " if name_count > 2 else " ")
    if i == name_count-1 and name_count > 1:
      buf.append("and ")
    buf.append(add_article(name))
  return "".join(buf)

def log(message):
    now = datetime.datetime.now()
    current_time = "{}:{} {}/{}/{} \n".format(now.hour, now.minute, now.month, now.day, now.year)
    logFile = open('runtime.log', 'a')
    logFile.write(current_time)
    logFile.write(message+"\n")
    logFile.close()



##########################################################
# Basic game interaction and low level game object
# Creates foundation for the rest of the game and objects
##########################################################
class Base(object):
    def __init__(self, name):
        self.name = name
        self.command = "" 

    def get_user_input(self):
        self.command = str(input("--> "))
        return self.command.lower()

class Game(Base):
    def __init__(self, name):
        Base.__init__(self, name)
        self.output = ""
        self.locations = {}
        self.start_location = ""

    def new_location(self, name, description):
        place = Location(name, description)
        self.locations[name] = place
        return self.locations[name]
    
    def parse_command(self, user_input):
        # This method takes the user input and returns a "verb, noun, indirect noun" command
        # EXAMPLE "unlock the door with the key" becomes {"verb": unlock, "noun": door, "inoun": key}
        command_dict = {}
        user_input = user_input.lower()
        user_input = remove_superfluous_input(user_input)
        user_input_list = user_input.split(' ')

        if len(user_input_list) > 0:
            command_dict['verb'] = user_input_list[0]

        if len(user_input_list) > 1:
            command_dict['noun'] =  user_input_list[1]

        if len(user_input_list) > 2:
            command_dict['inoun'] = user_input_list[2]

        return command_dict

    def update(self, player, current_location):
        # if player moved, describe the room. But only if fresh location.
        # otherwise, only show the name of the room
        if player.moved:
            print("\n<| {} |>".format(player.location.name))      # if moved, Display location name
            if current_location.fresh_location:
                print(player.look())
                self.locations[player.location.name]
                current_location.fresh_location = False

    def run(self):
        running = True
        log(" "+"="*100 +"\n---START RUNNING---")
        #print("+++++++++ NEW GAME +++++++++++")
        print(config.UserInfo.INTRODUCTION)
        user_name = str(input("What is your name? --> "))
        player = Player(user_name)
        print(" Glad to have you {} .... \n Good luck ;) ".format(user_name))
        current_location = player.set_location(self.locations["Front Porch"])[0]
        sleep(1)
        while running:

            self.update(player, current_location)
            
            # See if command was a direction to move
            user_input = self.get_user_input()  
            #command = remove_superfluous_input(user_input) 
            #command = command.lower()
            command = self.parse_command(user_input)
            #ommand_list = command.split(' ')                   # split the command up
            #verb = ""
            item = ""
            #inoun = command["inoun"]
            understood = False

            if user_input == "quit" or user_input == 'q':
                running = False
                understood = True

            if "inoun" in command:
                verb = command["verb"]
                noun = command["noun"]
                inoun = command["inoun"]
                if verb in player.verbs:
                    if noun in current_location.items or noun in player.inventory: # see if command refrences an item in the location
                        if inoun in current_location.items or inoun in player.inventory: # see if command refrences an item in the location
                            try:
                                self.output = player.verbs[verb](noun, inoun)
                                understood = True
                            except TypeError:
                                pass
                        else:
                            self.output = "there is no {} to use with the {}".format(inoun, noun)
                            understood = True
                    else:
                        self.output = "there is no {} in sight!".format(noun)
                        understood = True

            elif "noun" in command:
                verb = command["verb"]
                noun = command["noun"]
                if noun in current_location.items or noun in player.inventory: # see if command refrences an item in the location
                    try:
                        self.output = player.verbs[verb](noun)
                        understood = True
                    except TypeError:
                        self.output = "You can't do that with {}".format(add_article(noun))
                        understood = True
                ###### FOR USE OF THE player.go() FUNCTION WHICH CURRENTLY CAUSES SEVERAL BUGS
                #if noun in directions:
                #    if directions[noun] in current_location.connection:
                #        try:
                #            self.output = player.verbs[verb](noun)
                #            understood = True
                #        except: 
                #            pass
                #    else:
                #        self.output = "you can't go that way"
                #        understood = True
                #else:
                    player.moved = False
                
            elif "verb" in command:
                verb = command["verb"]
                if verb in directions:
                    if directions[verb] in current_location.connection:
                       #  update players location
                       # this should be condensed into the player.go() function at somepoint
                        to_location =  player.set_location(current_location.connection[directions[verb]])
                        current_location = to_location[0]
                        self.output = to_location[1]
                        #self.output = player.go(verb)
                        understood = True

                    else:
                        self.output = "you can't go that way"
                        understood = True
                else:
                    player.moved = False
                    for v in player.verbs:
                        if verb == v:
                            try:
                                self.output = player.verbs[verb]()
                                understood = True
                            except TypeError:
                                pass 

            if not understood:
                self.output = "I don't understand"

            print(self.output)


##########################################################
# Player and Character objects
#
##########################################################
class Actor(object):
    def __init__(self, user_name):
        self.health = 100
        self.inventory = {}
        self.inventory_max = 2
        self.moved = False
        self.location = None

class Player(Actor):
    def __init__(self, user_name):
        Actor.__init__(self, user_name)
        self.user_name = user_name
        self.saved_progress = None
        self.verbs = {}

        self.verbs['take'] = self.take
        self.verbs['get'] = self.take
        self.verbs['drop'] = self.drop
        self.verbs['inventory'] = self.check_inventory
        self.verbs['i'] = self.check_inventory
        self.verbs['look'] = self.look
        #self.verbs['go'] = self.go
        self.verbs['verbs'] = self.give_help
        self.verbs['commands'] = self.give_help
        self.verbs['help'] = self.give_help
        self.verbs['script'] = self.script

    def set_location(self, location):
        need = "" 
        feedback = ""
        if not location.requirements:
            self.location = location
            self.moved = True
        elif location.requirements:
            for i in location.requirements:
                if i in self.inventory:
                    requirement_fullfilled = True
                else:
                    requirement_fullfilled = False
                    break
            #for i in location.requirements:
            #    need += add_article(i.name)+", "
            need = proper_list_from_dict(location.requirements)
            if requirement_fullfilled:
                self.location = location
                self.moved = True
                feedback = "using {} you enter the {}".format(need, location.name)
                self.moved = True
            else:
                feedback = "you are unable to go there without {}".format(need)
        return self.location, feedback


    def take(self, item):
        self.moved = False
        if len(self.inventory) <= self.inventory_max:
            if item in self.location.items:
                self.inventory[item] = self.location.items[item]
                del self.location.items[item]
                return "you took the {}".format(item)
            else:
                return "you can't take that"
        else:
            return "you don't have enough space, you will have to drop something"
     

    def drop(self, item):
        self.moved = False
        if item in self.inventory:
            self.location.items[item] = self.inventory[item]
            del self.inventory[item]
            return "you droped the {}".format(item)
        else:
            return "you don't have one of those"

    def look(self, noun = None, inoun = None):
        self.moved = False
        if noun != None:
            if noun in self.inventory:
                feedback = self.inventory[noun].description
            elif noun in self.location.items:
                feedback = self.location.items[noun].description
        else:
            feedback = self.location.description+"\n"
            #for key, obj in self.location.items.items():
            #    feedback += "there is {}\n".format(add_article(obj.name))
            if self.location.items:
                feedback += "There is " + proper_list_from_dict(self.location.items)
        return feedback 

    def check_inventory(self):
        self.moved = False
        feedback = "you have...  " + proper_list_from_dict(self.inventory)

        #for k, v in self.inventory.items():
        #    item = add_article(v.name)
        #    feedback += item+", "
        return feedback

    def give_help(self):
        self.moved = False
        feedback = "Here are some commands I understand: \n"
        for i in self.verbs:
            feedback += i+"\n" 
        return feedback


    def go(self, direction):
        to_location =  self.set_location(self.location.connection[directions[direction]])
        self.location = to_location[0]
        return  to_location[1]

    def script(self):
        string_script = input(">>> ")
        print("Abraa Kadabraaa")
        eval(string_script)
        return "ALAKAZAM!"

###########################################################
# Locations.... Rooms and map creation
#
###########################################################
class Location():
    def __init__(self, name, description):
        self.items =  {} 
        self.requirements = {} 
        self.connection = {}
        self.name = name
        self.description = description
        self.fresh_location = True

    def new_connection(self, listDirections, connected_location):
        # make connection to next room
        for direction in listDirections:
            self.connection[direction] = connected_location
            # reverse connection back
            if direction % 2 > 0:
                connected_location.connection[direction+1] = self
            elif direction % 2 == 0:
                connected_location.connection[direction-1] = self
            else:
                print("error, something went wrong with connection method")
        
    def add_requirement(self, objItem):
        self.requirements[objItem.name] = objItem

    def add_item(self, item):
        self.items[item.name] = item

###########################################################
# Game Items
#
###########################################################
class Item():
    def __init__(self, name, description, fixed = False, state = False):
        self.name = name
        self.description = description 
        self.fixed = fixed 
        self.state = state 
        self.damage = 0
    
    def do_thing(self):
        action = None
        return action
