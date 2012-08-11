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
        if k == pyglet.window.key.W:
            # move the player up
            self.model.player.move_up = True
        if k == pyglet.window.key.S:
            #move the player down
            self.model.player.move_down = True
        if k == pyglet.window.key.A:
            #move the player left
            self.model.player.move_left = True
        if k == pyglet.window.key.D:
            #move the player right
            self.model.player.move_right = True
        if k == pyglet.window.key.LSHIFT:
            # running
            self.model.player.sprinting = True
        if self.paused:
            return False
        if self.used_key:
            return False
        self.used_key = True
        return True

    def on_key_release(self, k, m):
        if k == pyglet.window.key.W:
            # move the player up
            self.model.player.move_up = False
        if k == pyglet.window.key.S:
            #move the player down
            self.model.player.move_down = False
        if k == pyglet.window.key.A:
            #move the player left
            self.model.player.move_left = False
        if k == pyglet.window.key.D:
            #move the player right
            self.model.player.move_right = False
        if k == pyglet.window.key.LSHIFT:
            # running
            self.model.player.sprinting = False

    def on_mouse_press(self, x, y, button, modifiers):
        self.model.player.shooting = True
        vx, vy = director.get_virtual_coordinates(x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        """ call the shoot function in the direction of the mouse 
        cursor originating from the players location """
        vx, vy = director.get_virtual_coordinates(x, y)
        self.model.player.shooting = False

    def pause_controller(self):
        self.paused = True
        self.unschedule(self.step)

    def resume_controller(self):
        self.paused = False
        self.schedule(self.step)

    def step(self, dt):
        self.elapsed += dt
        #print self.elapsed
        update_speed = 0.01
        if self.elapsed > update_speed:
            self.elapsed = 0
            self.model.move_player()
        # add stuff with timesteps here

    def draw(self):
        self.used_key = False