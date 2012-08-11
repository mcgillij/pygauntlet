'''
Created on Jul 25, 2012

@author: mcgillij
'''
from cocos.layer import Layer
import pyglet
from cocos.director import director
#from status import status

class Controller( Layer ):
    is_event_handler = True
    def __init__(self, model):
        super(Controller, self).__init__()
        self.used_key = False
        self.paused = True
        self.model = model
        self.elapsed = 0
        
    def on_key_press(self, k, m):
        # add some keyboard bindings here
        if k == pyglet.window.key.SPACE:
            print "pressed space"
        #if k == pyglet.window.key.ESCAPE:
        #    print "pressed esc trying to switch back"
        #    self.parent.switch_to(0)
        if self.paused:
            return False
        if self.used_key:
            return False
        self.used_key = True
        return True

    def on_mouse_release(self, x, y, button, modifiers):
        vx, vy = director.get_virtual_coordinates(x, y)
        for c in self.model.player_choices:
            rect = c.get_rect()
            print rect
            if c.contains(vx, vy):
                self.model.set_choice(c)
                return

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