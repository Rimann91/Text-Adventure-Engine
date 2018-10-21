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

# for giving direction feedback to the user
direction_feedback = {
    1: "north",
    2: "south",
    3: "east",
    4: "west",
    5: "up",
    6: "down",
    7: "right",
    8: "left",
    9: "in",
    10: "out",
    11: "forward",
    12: "back",
    13: "north west",
    14: "north east",
    15: "south west",
    16: "south east",
}

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
  superfluous = articles +  ['to', 'using', 'with', 'on', 'at', 'in']
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
    current_time = "{}:{} {}/{}/{} >>> ".format(now.hour, now.minute, now.month, now.day, now.year)
    logFile = open('runtime.log', 'a')
    logFile.write(current_time)
    logFile.write(message+"\n")
    logFile.close()

def pause():
    sleep(config.pause_time)


"""
TODO[x]: Add inoun functionality to existing functions
TODO[]: Make a take all function
TODO[]: Introduce conjuction functionality with 'and'

"""
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
    def __init__(self, name, player):
        Base.__init__(self, name)
        self.player = player
        self.output = ""
        self.event_output = ""
        self.locations = {}
        self.current_location = None 
        self.run_count = 0

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

    #def getNearbyItemNames(self):
    #    nearby_items = []
    #    for item in player.inventory:


    def update(self, player, current_location):
        # if player moved, describe the room. But only if fresh location.
        # otherwise, only show the name of the room
        if player.moved:
            self.player.location = self.current_location
            print("\n<| {} |>".format(self.current_location.name))      # if moved, Display location name
            if self.current_location.fresh_location:
                print(self.player.look())
                self.locations[player.location.name]
                self.current_location.fresh_location = False

    def run(self, command):
        self.output = ""
        self.event_output = ""
        #log("LOOP ITERATION {}".format(self.run_count))

        self.update(self.player, self.current_location)

        #user_input = self.get_user_input()
        user_input = command
        command = self.parse_command(user_input)
        understood = False

        if user_input == "quit" or user_input == 'q':
            running = False
            understood = True
            log("MANUAL EXIT OF GAME LOOP")

        if "inoun" in command:
            verb = command["verb"]
            noun = command["noun"]
            inoun = command["inoun"]
            if verb in self.player.verbs:
                if noun in self.current_location.items or noun in self.player.inventory: # see if command refrences an item in the location
                    if inoun in self.current_location.items or inoun in self.player.inventory: # see if command refrences an item in the location
                        try:
                            self.output = self.player.verbs[verb](verb, noun, inoun)
                            understood = True
                            #print(self.output)
                            return (self.output, self.event_output)
                        except (TypeError, KeyError):
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
            if noun in self.current_location.items or noun in self.player.inventory: # see if command refrences an item in the location
                try:
                    self.output = self.player.verbs[verb](verb, noun)
                    understood = True
                    #print(self.output)
                    return (self.output, self.event_output)
                    #continue
                except (TypeError, KeyError):
                    self.output = "You can't do that with {}".format(add_article(noun))
                    understood = True
            # check if noun is a connection obstacle
            else:
                for k, connection in self.current_location.connection.items():
                    if connection.obstacle != None:
                        if connection.obstacle.name == noun:
                            try:
                                self.output = self.player.verbs[verb](verb, noun)
                                understood = True
                                #print(self.output)
                                return (self.output, self.event_output)
                                #continue
                            except (TypeError, KeyError):
                                self.output = "You can't do that with {}".format(add_article(noun))
                                understood = True

            for i in self.player.location.items:
                objItem = self.player.location.items[i]
                if isinstance(objItem, Container):
                    if objItem.state:
                        if noun in objItem.contents:
                            self.output = self.player.verbs[verb](verb, noun)
                            understood = True
                            #print(self.output)
            self.player.moved = False
            return (self.output, self.event_output)
            #continue
            ###### FOR USE OF THE self.player.go() FUNCTION WHICH CURRENTLY CAUSES SEVERAL BUGS
            #if noun in directions:
            #    if directions[noun] in self.current_location.connection:
            #        try:
            #            self.output = self.player.verbs[verb](noun)
            #            understood = True
            #        except: 
            #            pass
            #    else:
            #        self.output = "you can't go that way"
            #        understood = True
            #else:
            
        elif "verb" in command:
            verb = command["verb"]
            if verb in directions:
                if directions[verb] in self.current_location.connection:
                    #  update self.players location
                    # this should be condensed into the self.player.go() function at somepoint
                    connection = self.current_location.connection[directions[verb]]
                    to_location =  self.player.set_location(self.current_location.connection[directions[verb]].connected_location, directions[verb])
                    self.current_location = to_location[0]
                    self.output = to_location[1]
                    #self.output = self.player.go(verb)
                    understood = True

                else:
                    self.output = "you can't go that way"
                    understood = True
            else:
                self.player.moved = False
                for v in self.player.verbs:
                    if verb == v:
                        try:
                            self.output = self.player.verbs[verb]()
                            understood = True
                            break
                        except (TypeError, KeyError):
                            pass 

        if not understood:
            self.output = "I don't understand"

        #print(self.output)
        self.run_count += 1
        return (self.output, self.event_output)


##########################################################
# Player and Character objects
#
##########################################################
class Actor(object):
    def __init__(self, user_name):
        self.health = 100
        self.inventory = {}
        self.inventory_max = 2
        self.moved = True 
        self.location = None

class Player(Actor):
    def __init__(self, user_name):
        Actor.__init__(self, user_name)
        self.user_name = user_name
        self.saved_progress = None
        self.verbs = {
            #"unlock"
            #"turn"
            "go": self.go,
            "take" : self.take,
            "get": self.take,
            "drop": self.drop,
            "put": self.drop,
            "inventory": self.check_inventory,
            "i": self.check_inventory,
            "look": self.look,
            "open": self.switch_item_state,
            "close": self.switch_item_state,
            "verbs": self.give_help,
            "commands": self.give_help,
            "help": self.give_help,
            "script": self.script,
            "unlock": self.unlock
        }

        #self.verbs['take'] = self.take
        #self.verbs['get'] = self.take
        #self.verbs['drop'] = self.drop
        #self.verbs['put'] = self.drop
        #self.verbs['inventory'] = self.check_inventory
        #self.verbs['i'] = self.check_inventory
        #self.verbs['look'] = self.look
        #self.verbs['open'] = self.switch_item_state
        #self.verbs['close'] = self.switch_item_state
        ##self.verbs['unlock']
        ##self.verbs['turn']
        ##self.verbs['go'] = self.go
        #self.verbs['verbs'] = self.give_help
        #self.verbs['commands'] = self.give_help
        #self.verbs['help'] = self.give_help
        #self.verbs['script'] = self.script

    def set_start_location(self, location):
        self.moved = True
        self.location = location
        return self.location

    def set_location(self, location, direction):
        need = "" 
        feedback = ""
        if self.location.connection[direction].obstacle != None:
            obstacle = self.location.connection[direction].obstacle
            if obstacle.state:
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

                    need = proper_list_from_dict(location.requirements)
                    if requirement_fullfilled:
                        self.location = location
                        self.moved = True
                        feedback = "using {} you enter the {}".format(need, location.name)
                        self.moved = True
                    else:
                        feedback = "you are unable to go there without {}".format(need)
            else:
                feedback = "there is a {} in the way".format(obstacle.name)
        elif location.requirements:
            for i in location.requirements:
                if i in self.inventory:
                    requirement_fullfilled = True
                else:
                    requirement_fullfilled = False
                    break

            need = proper_list_from_dict(location.requirements)
            if requirement_fullfilled:
                self.location = location
                self.moved = True
                feedback = "using {} you enter the {}".format(need, location.name)
                self.moved = True
            else:
                feedback = "you are unable to go there without {}".format(need)
        else:
            self.location = location
            self.moved = True
            feedback = "using {} you enter the {}".format(need, location.name)
            self.moved = True

        return self.location, feedback


    def unlock(self, verb, item):
        feedback = ""
        if item in self.location.items:
            feedback = self.location.items[item].unlock()
        elif item not in self.location.items:
            for k, connection in self.location.connection.items():
                if connection.obstacle != None:
                    if item == connection.obstacle.name:
                        connection.obstacle.unlock()
        return feedback


    def take(self, verb, item):
        """ Takes item from location or from a container """
        self.moved = False
        if len(self.inventory) <= self.inventory_max:
            if item in self.location.items:
                if not self.location.items[item].fixed:
                    self.inventory[item] = self.location.items[item]
                    del self.location.items[item]
                    feedback = "you took the {}".format(item)
                else: 
                    feedback = "hinnnnng... the thing doesn't budge"

            else:
            # if location has an open container, check if container has item
                for i in self.location.items:
                    objItem = self.location.items[i]
                    if isinstance(objItem, Container):
                        if objItem.state:
                            if item in objItem.contents:
                                self.inventory[item] = objItem.contents[item]
                                del objItem.contents[item]
                                feedback = "you took the {} from the {}".format(item, objItem.name)
                                break
                    else:
                        feedback = "you can't take that"
        else:
            feedback =  "you don't have enough space, you will have to drop something"

        return feedback
     

    def drop(self, verb, noun, inoun = None):

        """ Drops an item carried in player.inventory
        Items can be droped into the current location or droped into containers
        """
        objNoun = None
        objInoun = None
        self.moved = False

        if noun in self.inventory:
            objNoun = self.inventory[noun]
            if inoun:
                if inoun in self.location.items:
                    objInoun = self.location.items[inoun]
                elif inoun in self.inventory:
                    objInoun = self.inventory[inoun]
                objInoun.contents[noun] = objNoun
                del self.inventory[noun] 
                feedback = "you droped the {} in the {}".format(noun, inoun)
            else:
                self.location.items[noun] = objNoun 
                del self.inventory[noun] 
            feedback = "you droped the {}".format(noun)
        else:
            feedback = "you don't have one of those"
        return feedback

    def look(self, noun = None, inoun = None):
        feedback = ""
        self.moved = False
        if noun != None:
            if noun in self.inventory:
                feedback = self.inventory[noun].description
            elif noun in self.location.items:
                feedback = self.location.items[noun].description
                if isinstance(self.location.items[noun], Container) and self.location.items[noun].state: # cHECK IF ITEM LOOKED AT IS CONTAINER AND IF IT IS OPEN
                    feedback += ". it contains {}".format(proper_list_from_dict(self.location.items[noun].contents)) # lIST THE CONTENTS OF CONTAINER
        else:
            feedback = self.location.description
        #    if self.location.connection:
        #        feedback += ". There is " + self.location.list_connections()
            if self.location.items:
                feedback += ". There is " + proper_list_from_dict(self.location.items)
        return feedback
    
    def switch_item_state(self, verb, item):
        """ Player method that switches the state of an item
        Used to turn things on or off, open or close, enable disable, etc...
        """
        objItem = None
        feedback = ""

        if item in self.inventory:
            objItem = self.inventory[item]
            if not objItem.locked:
                feedback = "the {} is ".format(objItem.name)
                feedback += objItem.switch_state(verb)
        
        elif item in self.location.items:
            objItem = self.location.items[item]
            if not objItem.locked:
                feedback = "the {} is ".format(objItem.name)
                feedback += objItem.switch_state(verb)

        else:
            for k, v in self.location.connection.items():
                if v.obstacle != None:
                    if item == v.obstacle.name:
                        objItem = v.obstacle
                        if not objItem.locked:
                            feedback = "the {} is ".format(objItem.name)
                            feedback += objItem.switch_state(verb)
                        else:
                            feedback = objItem.locked_response
        
        if feedback == "":
            feedback = "do what?"

        return feedback


    def check_inventory(self):
        """Prints out the contens of Player.inventory"""

        self.moved = False
        feedback = "you have...  " + proper_list_from_dict(self.inventory)
        return feedback

    def give_help(self, verb):
        self.moved = False
        feedback = "Here are some commands I understand: \n"
        for i in self.verbs:
            feedback += i+"\n" 
        return feedback

    def go(self, direction):
        to_location =  self.set_location(self.location.connection[directions[direction]])
        self.location = to_location[0]
        return  to_location[1]

    def script(self, verb):
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

    def add_connection(self, obj_connection):
        # make connection to next room
        for direction in obj_connection.list_directions:
            self.connection[direction] = obj_connection.connected_location
            # reverse connection back
            if direction % 2 > 0:
                obj_connection.connected_location.connection[direction+1] = self
            elif direction % 2 == 0:
                obj_connection.connected_location.connection[direction-1] = self
            else:
                print("WARNING: something went wrong with connection method")
                log("WARNING: something went wrong with connection method")
        
    def add_requirement(self, objItem):
        self.requirements[objItem.name] = objItem

    def add_item(self, item):
        self.items[item.name] = item
    
    #def list_connections(self):
    #    count = len(self.connection)
    #    str_listConnections = ""
    #    if self.connection:
    #        for k, c in self.connection.items():
    #            str_listConnections += " {} to your {}".format(c.description, direction_feedback[c.list_directions[0]])
    #            if count > 1:
    #                str_listConnections += ","
    #            elif count == 1:
    #                str_listConnections +="."
    #            count -= 1
    #    return str_listConnections
            

class Connection():
    def __init__(self, list_directions, this_location, connected_location, description, obstacle = None):
        self.description = description
        self.list_directions = list_directions
        self.connected_location = connected_location
        self.obstacle = obstacle 
        return_directions = []

        # this creates a new connection object for the conected location
        # Although the connections are seperate they will share the same obstacle object 
        for direction in list_directions:
            this_location.connection[direction] = self 
            # reverse connection back
            if direction % 2 > 0:
                #return_direction = connected_location.connection[direction+1] = self
                return_directions.append(direction+1)
            elif direction % 2 == 0:
                #return_direction = connected_location.connection[direction-1] = self
                return_directions.append(direction-1)
            else:
                print("WARNING: something went wrong with connection method")
                log("WARNING: something went wrong with connection method")


        if connected_location.connection:
            if not any(return_directions[i] in list(connected_location.connection) for i in range(len(return_directions))): 
                reverse_connection = Connection(return_directions, self.connected_location, this_location, self.description,  self.obstacle)
        else:
            reverse_connection = Connection(return_directions, self.connected_location, this_location, self.description,  self.obstacle)

        
    
    def has_obstacle(self):
        if not self.obstacle: return True
        else: return False


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
        self.state_switch_feedback = ()  #("on", "off") ("open", "closed")
        self.locked = False
        self.locked_response = ""
        self.unlock_required_item = None
        #self.requirements = {}

        # Callbacks
        self.on_state_true_callback = None
        self.on_state_false_callback = None
        self.on_unlocked_callback = None
        #self.on_locked_callback = None
    
    # Event Callback Setters
    def on_state_true(self, callback):
        self.on_state_true_callback = callback 
    
    def on_state_false(self, callback):
        self.on_state_false_callback = callback

    def on_unlocked(self, callback):
        self.on_unlocked_callback = callback

    #def on_locked(self, callback):
    #    self.on_locked_callback = callback
   
    def set_fixed(self):
        self.fixed = True

    # Item Methods
    def switch_state(self, verb):
        # maybe the indexes need to be switched
        if self.locked == False:
            feedback = ""
            if self.state_switch_feedback:
                true_state = self.state_switch_feedback[0]
                false_state = self.state_switch_feedback[1]
                if verb == true_state:
                    self.state = not self.state
                    feedback = true_state 
                    if self.on_state_true_callback:
                        callback_response = self.on_state_true_callback()
                        #if callback_response:
                        #    feedback = callback_response
                else:
                    self.state = not self.state
                    feedback = false_state 
                    if self.on_state_false_callback:
                        callback_response = self.on_state_false_callback()
                        #if callback_response:
                        #    feedback = callback_response
            else:
                print("WARNING: cannot switch the state of an item without defining a feedback tuple")
                log("WARNING: cannot switch the state of an item without defining a feedback tuple")
        else:
            feedback = self.locked_response
        return feedback

    def unlock(self, verb = None):
        feedback = ""
        if self.locked:
            if self.unlock_required_item == None:
                self.locked = False
                if self.on_unlocked_callback:
                    self.on_unlocked_callback()
            else:
                #check player for requirements
                pass
        else:
            feedback = config.DefaultResponse.nothing_intersting 
        return feedback

class Container(Item):
    def __init__ (self, name, description, fixed = False, state = False):
        Item.__init__(self, name, description, fixed = False, state = False)
        self.contents = {}
    
class Obstacle(Item):
    """ Various obstacels, This object should be passed into location connections for doors etc.."""
    def __init__(self, name, description, fixed = True, state = True):
        Item.__init__(self, name, description, fixed, state)
        self.do_list = False


