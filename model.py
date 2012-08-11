import pyglet
import weakref
from status import status
from cocos.euclid import Point2
from cocos.sprite import Sprite
from random import choice

import bulletml
import math
import os

TW = 32

def distance(a, b):
    return math.sqrt((a.x/2-b.x)**2 + (a.y/2-b.y)**2)

class Model(pyglet.event.EventDispatcher):
    def __init__(self):
        super(Model, self).__init__()
        self.cursor = Cursor()
        self.player = Player()
        self.doc = self.doc = bulletml.BulletML.FromDocument(open(os.path.join('assets', 'double_spinny_pants.xml'), "rU"))
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
        # set base conditions so we can load a new level
        #self.player = Player()
        #self.level = Level()
        pass

Model.register_event_type('on_level_complete')
Model.register_event_type('on_new_level')
Model.register_event_type('on_game_over')
Model.register_event_type('on_win')

# add other event types / clicks as events here

class Player(Sprite):
    def __init__(self):
        super(Player, self).__init__('player.png')
        self.position = (100, 100)
        self.sprinting = False
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        self.attacking = False
        self.speed = 3
        self.active_bullets = set([])
        self.target = bulletml.Bullet()
        self.shooting = False

    def move(self):
        multiplier = 1
        if self.sprinting:
            multiplier = 2
        if self.move_up:
            print "moving up"
            self.y = self.y + self.speed * multiplier
        if self.move_down:
            print "moving down"
            self.y = self.y - self.speed * multiplier
        if self.move_left:
            print "moving left"
            self.x = self.x - self.speed * multiplier
        if self.move_right:
            print "moving right"
            self.x = self.x + self.speed * multiplier

class Cursor(Sprite):
    def __init__(self):
        super(Cursor, self).__init__('shotgun.png')
        self.position = (100, 100)
    def update(self, x, y):
        self.position = (x, y)

class Mob(Sprite):
    def __init__(self):
        super(Mob, self).__init__('mob.png')