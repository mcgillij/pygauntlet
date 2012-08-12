from cocos.layer import Layer
import pyglet
from cocos.director import director
#from status import status
import bulletml
from model import Mob
import random
class Controller( Layer ):
    is_event_handler = True
    def __init__(self, model):
        super(Controller, self).__init__()
        self.paused = False
        self.model = model
        self.elapsed = 0
        self.mouse_pos = self.model.cursor.position

    def on_key_press(self, k, m):
        if k == pyglet.window.key.SPACE:
            self.paused ^= True
            if self.paused:
                self.model.dispatch_event("on_pause")
            else:
                self.model.dispatch_event("on_resume")
        if self.paused:
            return False

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
        vx, vy = director.get_virtual_coordinates(x, y)
        self.mouse_pos = (vx, vy)
        self.model.player.shooting = True

    def on_mouse_motion(self, x, y, dx, dy):
        vx, vy = director.get_virtual_coordinates(x, y)
        self.mouse_pos = (vx, vy)
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        vx, vy = director.get_virtual_coordinates(x, y)
        self.mouse_pos = (vx, vy)
        if buttons & pyglet.window.mouse.LEFT:
            self.model.player.shooting = True

    def on_mouse_release(self, x, y, button, modifiers):
        vx, vy = director.get_virtual_coordinates(x, y)
        self.mouse_pos = (vx, vy)
        self.model.player.shooting = False
        """ call the shoot function in the direction of the mouse 
        cursor originating from the players location """

    def pause_controller(self):
        self.paused = True
        self.unschedule(self.step)

    def resume_controller(self):
        self.paused = False
        self.schedule(self.step)

    def step(self, dt):
        self.model.cursor.update(self.mouse_pos[0], self.mouse_pos[1])
        self.elapsed += dt
        update_speed = 0.01
        if self.elapsed > update_speed:
            self.elapsed = 0
            self.model.player.move()
            self.model.player_target.x, self.model.player_target.y = (self.model.player.x /2, self.model.player.y /2)
            
            for m in self.model.mobs[:]:
                if m.offscreen:
                    self.model.remove(m)
                else:
                    m.move(self.model.player.x, self.model.player.y)
                    source = bulletml.Bullet.FromDocument(m.doc, x=m.x/2, y=m.y/2, target=self.model.player_target, rank=0.5, speed=5)
                    source.vanished = True
                    self.model.mob_active_bullets.add(source)

        if self.model.player.shooting:
            self.model.player.target.x, self.model.player.target.y = self.mouse_pos[0]/2, self.mouse_pos[1]/2
            self.model.player.target.px, self.model.player.target.py = self.model.player.target.x, self.model.player.target.y 
            source = bulletml.Bullet.FromDocument(self.model.player.doc, x=self.model.player.x/2, y=self.model.player.y/2, target=self.model.player.target, rank=0.5, speed=10)
            source.vanished = True
            self.model.player.active_bullets.add(source)
        w,h = director.get_window_size()
        p_active = list(self.model.player.active_bullets)
        for obj in p_active:
            new = obj.step()
            self.model.player.active_bullets.update(new)
            if (obj.finished 
                or not (0 < obj.x < w)
                or not (0 < obj.y < h)):
                self.model.player.active_bullets.remove(obj)

        m_active = list(self.model.mob_active_bullets)
        for obj in m_active:
            new = obj.step()
            self.model.mob_active_bullets.update(new)
            if (obj.finished 
                or not (0 < obj.x < w)
                or not (0 < obj.y < h)):
                self.model.mob_active_bullets.remove(obj)

        self.model.mob_spawn_counter += 1
        if self.model.mob_spawn_counter == self.model.mob_spawn_rate:
            self.model.mob_spawn_counter = 0
            m = Mob()
            m.position = (random.randint(0, w), h)
            self.model.mobs.append(m)

    def draw(self):
        pass