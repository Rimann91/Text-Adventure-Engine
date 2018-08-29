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
  superfluous = articles +  ['to']
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
    current_time = "{}:{} {}/{}/{}".format(now.hour, now.minute, now.month, now.day, now.year)
    logFile = open('log.txt', 'a')
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
    
    def parse_command(self, text):
        text = text.lower()
        text = remove_superfluous_input(text)
        text_list = text.split(' ')
        return text

    def update(self, player, current_location):
        # if player moved, describe the room. But only if fresh location.
        # otherwise, only show the name of the room
        if player.moved:
            
            print("\n<| {} |>".format(player.location.name))      # if moved, Display location name
            if current_location.fresh_location:
                print(player.location.description)
                if current_location.items:
                    for k, v in current_location.items.items():
                        print("there is {}".format(add_article(v.name)))
                self.locations[player.location.name]
                current_location.fresh_location = False

    def run(self):
        running = True
        log("="*100 +"\n---START RUNNING---")
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
            command_list = command.split(' ')                   # split the command up
            verb = ""
            item = ""
            understood = False

            if command == "quit":
                running = False

            for word in command_list: # see if command references a player verb

                # determines if the player wants to move locations and attempts to move them
                if word in directions:
                    #self.output = "you go {}".format(command)
                    understood = True
                    if directions[word] in current_location.connection:
                        # update players location
                        to_location =  player.set_location(current_location.connection[directions[word]])
                        current_location = to_location[0]
                        self.output = to_location[1]

                    else:
                        self.output = "you can't go that way"
                        understood = True
                else:
                    player.moved = False

                # determines if the user input containes a verb, attempts to call a method assiciated with that verb
                if word in player.verbs:
                    for v in player.verbs:
                        if word == v:
                            verb = v
                            try:
                                self.output = player.verbs[verb]()
                                understood = True
                            except:
                                break

                # determines if player is attempting to use a verb on an item eg. "drop key", "take knife"
                # attempts to call a method associated with verb and pass in item as parameter
                if word in current_location.items or word in player.inventory: # see if command refrences an item in the location
                        try:
                            self.output = player.verbs[verb](word)
                            understood = True
                        except:
                            self.output = "You can't do that with {}".format(add_article(word))
                            understood = True
                
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
        #self.verbs['go']
        self.verbs['verbs'] = self.give_help
        self.verbs['commands'] = self.give_help
        self.verbs['help'] = self.give_help

    def set_location(self, location):
        need = ""
        feedback = ""
        if not location.requirements:
            self.location = location
            self.moved = True
        elif location.requirements:
            for i in location.requirements:
                if i.name in self.inventory:
                    requirement_fullfilled = True
                else:
                    requirement_fullfilled = False
                    break
            for i in location.requirements:
                need += add_article(i.name)+", "
            if requirement_fullfilled:
                self.location = location
                self.moved = True
                feedback = "using {} you enter the {}".format(need, location.name)
                self.moved = True
            else:
                feedback = "you are unable to go there without {}".format(need)
        return self.location, feedback


    def take(self, item):
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
        if item in self.inventory:
            self.location.items[item] = self.inventory[item]
            del self.inventory[item]
            return "you droped the {}".format(item)
        else:
            return "you don't have one of those"

    def look(self, item = None):
        feedback = self.location.description+"\n"
        for key, obj in self.location.items.items():
            feedback += "there is {}\n".format(add_article(obj.name))
        return feedback 

    def check_inventory(self):
        feedback = "you have...  "
        for k, v in self.inventory.items():
            item = add_article(v.name)
            feedback += item+", "
        return feedback

    def give_help(self):
        feedback = "Here are some commands I understand:"
        for i in self.verbs:
            feedback += i+"\n" 
        return feedback


    def go(self):
        pass

    def looked(self):
        pass


###########################################################
# Locations.... Rooms and map creation
#
###########################################################
class Location():
    def __init__(self, name, description):
        self.items =  {} 
        self.requirements = [] 
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
        self.requirements.extend(objItem)

    def add_item(self, item):
        self.items[item.name] = item

###########################################################
# Game Items
#
###########################################################
class Item():
    def __init__(self, name, description):
        self.name = name
        self.description = description 
        self.fixed = False
        self.damage = 0
