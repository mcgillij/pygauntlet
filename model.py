'''
Created on Jul 25, 2012

@author: mcgillij
'''
import pyglet
import weakref
from constants import CHOICES
from status import status
class Model(pyglet.event.EventDispatcher):
    def __init__(self):
        super(Model, self).__init__()
        self.choice = None
        status.reset()
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
    def did_i_win(self):
        from random import choice
        cpu_choice = choice(CHOICES)
        if self.choice.value == "Rock":
            if cpu_choice.value == "Rock":
                #draw
                return False
            elif cpu_choice.value == "Paper":
                # rock loses to paper
                return False
            elif cpu_choice.value == "Shotgun":
                # rock wins vs shotgun
                return True
        elif self.choice.value == "Paper":
            if cpu_choice.value == "Rock":
                # paper wins vs rock
                return True
            elif cpu_choice.value == "Paper":
                # draw
                return False
            elif cpu_choice.value == "Shotgun":
                # lose vs shotgun
                return False
        elif self.choice.value == "Shotgun":
            if cpu_choice.value == "Rock":
                # loss vs rock
                return False
            elif cpu_choice.value == "Paper":
                # win vs paper
                return True
            elif cpu_choice.value == "Shotgun":
                # draw
                return False
        else:
            #should not get here
            print "Got somewhere's bad"
        
    def on_RPS_select(self):
        #self.set_choice()
        if self.did_i_win():
            self.controller().pause_controller()
            self.dispatch_event('on_win')
        else:
            self.controller().pause_controller()
            self.dispatch_event('on_game_over')

Model.register_event_type('on_level_complete')
Model.register_event_type('on_new_level')
Model.register_event_type('on_game_over')
Model.register_event_type('on_win')
Model.register_event_type('on_RPS_select')
# add other event types / clicks as events here

if __name__ == '__main__':
    pass