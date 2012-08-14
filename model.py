import os
import weakref
from random import choice
import bulletml
import pyglet
from cocos.euclid import Point2
from cocos.sprite import Sprite
from cocos.director import director
from status import status

class Model(pyglet.event.EventDispatcher):
    def __init__(self):
        super(Model, self).__init__()
        self.cursor = Cursor()
        self.player = Player()
        self.mobs = []
        self.tardis = None
        self.mob_active_bullets = set([])
        self.mob_spawn_rate = 50
        self.mob_spawn_counter = 0
        #self.level = Level()
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
        #set base conditions so we can load a new level
        #self.player = Player()
        #self.level = Level()
        status.reset()

Model.register_event_type('on_level_complete')
Model.register_event_type('on_new_level')
Model.register_event_type('on_game_over')
Model.register_event_type('on_win')
Model.register_event_type('on_pause')
Model.register_event_type('on_resume')
Model.register_event_type('on_shoot')
Model.register_event_type('on_explode')
Model.register_event_type('on_deploy_tardis')
# add other event types / clicks as events here

class Player(Sprite):
    def __init__(self):
        ani = pyglet.image.load_animation(os.path.join('assets', 'player.gif'))
        super(Player, self).__init__(ani)
        self.position = (100, 100)
        self.sprinting = False
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        self.speed = 3
        self.active_bullets = set([])
        self.target = bulletml.Bullet()
        self.shooting = False
        self.doc = bulletml.BulletML.FromDocument(open(os.path.join('assets', 'double_spinny_pants.xml'), "rU"))
        #self.doc = bulletml.BulletML.FromDocument(open(os.path.join('assets', 'towards.xml'), "rU"))

    def move(self):
        multiplier = 1
        if self.sprinting:
            multiplier = 2
        if self.move_up:
            #print "moving up"
            self.y = self.y + self.speed * multiplier
        if self.move_down:
            #print "moving down"
            self.y = self.y - self.speed * multiplier
        if self.move_left:
            #print "moving left"
            self.x = self.x - self.speed * multiplier
        if self.move_right:
            #print "moving right"
            self.x = self.x + self.speed * multiplier

class Cursor(Sprite):
    def __init__(self):
        super(Cursor, self).__init__('crosshair.png')
        self.position = (100, 100)
    def update(self, x, y):
        self.position = (x, y)

class Mob(Sprite):
    def __init__(self):
        super(Mob, self).__init__('mob.png')
        #self.position = (200, 200)
        self.offscreen = False
        self.speed = 3
        self.active_bullets = set([])
        self.value = 100
        self.doc = bulletml.BulletML.FromDocument(open(os.path.join('assets', 'fan.xml'), "rU"))

    def move(self, px, py):
        w, h = director.get_window_size()
        if self.x < 0 or self.y < 0 or self.x > w or self.y > h:
            self.offscreen = True
        if self.x > px:
            self.x = self.x - self.speed
        if self.x < px: 
            self.x = self.x + self.speed
        if self.y > py:
            self.y = self.y - self.speed
        if self.y < py: 
            self.y = self.y + self.speed

class Mob2(Sprite):
    def __init__(self):
        super(Mob2, self).__init__('mob2.png')
        #self.position = (200, 200)
        self.offscreen = False
        self.speed = 2
        self.value = 250
        self.active_bullets = set([])
        self.doc = bulletml.BulletML.FromDocument(open(os.path.join('assets', 'towards.xml'), "rU"))

    def move(self, px, py):
        w, h = director.get_window_size()
        if self.x < 0 or self.y < 0 or self.x > w or self.y > h:
            self.offscreen = True
        if self.x > px:
            self.x = self.x - self.speed
        if self.x < px: 
            self.x = self.x + self.speed
        #if self.y > py:
        #   self.y = self.y - self.speed
        #if self.y < py: 
        #    self.y = self.y + self.speed

class Mob3(Sprite):
    def __init__(self):
        super(Mob3, self).__init__('mob3.png')
        #self.position = (200, 200)
        self.offscreen = False
        self.speed = 2
        self.value = 500
        self.active_bullets = set([])
        self.doc = bulletml.BulletML.FromDocument(open(os.path.join('assets', 'circle.xml'), "rU"))

    def move(self, px, py):
        w, h = director.get_window_size()
        if self.x < 0 or self.y < 0 or self.x > w or self.y > h:
            self.offscreen = True
        if self.x > px:
            self.x = self.x - self.speed
        if self.x < px: 
            self.x = self.x + self.speed
        if self.y > py:
            self.y = self.y - self.speed
        if self.y < py: 
            self.y = self.y + self.speed

class TARDIS(Sprite):
    def __init__(self):
        super(TARDIS, self).__init__('tardis.png')
        #self.position = (200, 200)
        self.offscreen = False
        self.speed = 2
        self.value = 1000

    def move(self):
        w, h = director.get_window_size()
        if self.x < 0 or self.y < 0 or self.x > w or self.y > h:
            self.offscreen = True
        self.y = self.y - self.speed