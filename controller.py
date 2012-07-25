'''
Created on Jul 25, 2012

@author: mcgillij
'''
from cocos.layer import Layer
import pyglet
from status import status
class Controller( Layer ):
    is_event_handler = True
    def __init__(self, model):
        super(Controller, self).__init__()
        self.used_key = False
        self.paused = True
        self.model = model
        self.elapsed = 0
        
    def on_key_press(self, k, m):
        if self.paused:
            return False
        if self.used_key:
            return False
        self.used_key = True
        return True
        
        # add some keyboard bindings here
        if k == pyglet.window.key.SPACE:
            print "You pressed Space"
    def pause_controller(self):
        self.paused = True
        self.unschedule(self.step)
    def resume_controller(self):
        self.paused = False
        self.schedule(self.step)
    def step(self, dt):
        self.elapsed += dt
        # add stuff with timesteps here
    def draw(self):
        self.used_key = False

if __name__ == '__main__':
    pass