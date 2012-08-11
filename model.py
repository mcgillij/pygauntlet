'''
Created on Jul 25, 2012

@author: mcgillij
'''
import pyglet
import weakref
from status import status
from cocos.euclid import Point2
from cocos.sprite import Sprite
from random import choice

TW = 32

class Model(pyglet.event.EventDispatcher):
    def __init__(self):
        super(Model, self).__init__()
        self.choice = None
        self.cpu_choice = None
        status.reset()
        
        self.player_choices = [Rock(), Paper(), Shotgun()]
        count = 0
        for c in self.player_choices:
            c.position = (100 + count, 100 )
            count += 50
        
        #set test level
        #status.level = something-level

    def set_controller(self, controller):
        self.controller = weakref.ref( controller )

    def start( self ):
        self.set_next_level()
        
    def set_next_level( self ):
        self.controller().resume_controller()
        self.init()  # re-init the object
        # do stuff to load new level
        self.dispatch_event("on_new_level")

    def init(self):
        # set base conditions so we can load a new level
        self.choice = None
        self.cpu_choice = None

    def did_i_win(self):
        if choice:
            if self.choice.value == "Rock":
                if self.cpu_choice.value == "Rock":
                    #draw
                    return False
                elif self.cpu_choice.value == "Paper":
                    # rock loses to paper
                    return False
                elif self.cpu_choice.value == "Shotgun":
                    # rock wins vs shotgun
                    return True
            elif self.choice.value == "Paper":
                if self.cpu_choice.value == "Rock":
                    # paper wins vs rock
                    return True
                elif self.cpu_choice.value == "Paper":
                    # draw
                    return False
                elif self.cpu_choice.value == "Shotgun":
                    # lose vs shotgun
                    return False
            elif self.choice.value == "Shotgun":
                if self.cpu_choice.value == "Rock":
                    # loss vs rock
                    return False
                elif self.cpu_choice.value == "Paper":
                    # win vs paper
                    return True
                elif self.cpu_choice.value == "Shotgun":
                    # draw
                    return False
            else:
                #should not get here
                print "Got somewhere's bad"
        else:
            print "No choice set"
        return False

    def set_choice(self, picked):
        #l = [Rock(), Paper(), Shotgun()]
        self.choice = picked
        self.cpu_choice = choice([Rock(), Paper(), Shotgun()])
        self.cpu_choice.position = (20, 150)
        self.dispatch_event('on_RPS_select')

    def on_RPS_select(self):
        print self.choice.value
        print self.cpu_choice.value
        if self.choice.value == self.cpu_choice.value:
            # tie
            print "tie"
            self.controller().pause_controller()
            self.dispatch_event('on_tie')
        elif self.did_i_win():
            self.controller().pause_controller()
            self.dispatch_event('on_win')
        else:
            self.controller().pause_controller()
            self.dispatch_event('on_game_over')

Model.register_event_type('on_level_complete')
Model.register_event_type('on_new_level')
Model.register_event_type('on_game_over')
Model.register_event_type('on_win')
Model.register_event_type('on_tie')
Model.register_event_type('on_RPS_select')

# add other event types / clicks as events here

class Rock(Sprite):
    def __init__(self):
        super(Rock, self).__init__('rock.png')
        self.value = "Rock"
        

class Paper(Sprite):
    def __init__(self):
        super(Paper, self).__init__('paper.png')
        self.value = "Paper"


class Shotgun(Sprite):
    def __init__(self):
        super(Shotgun, self).__init__('shotgun.png')
        self.value = "Shotgun"

if __name__ == '__main__':
    pass