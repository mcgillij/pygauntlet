'''
Created on Jul 25, 2012

@author: mcgillij
'''
import pyglet
from constants import TW
from cocos.euclid import Point2
class RPS(object):
    def __init__(self):
        super(RPS, self).__init__()
        self.pos = Point2(100, 100)
        self.rot = 0
        self.image = None
        self.value = None

    def draw(self):
        self.image.blit(self.pos.x * TW , self.pos.y * TW)

    def get(self):
        return self.value

class Rock(RPS):
    def __init__(self):
        self.value = "Rock"
        self.image = pyglet.resource.image('rock.png')
        super(Rock, self).__init__()

class Paper(RPS):
    def __init__(self):
        self.value = "Paper"
        self.image = pyglet.resource.image('paper.png')
        super(Paper, self).__init__()

class Shotgun(RPS):
    def __init__(self):
        self.value = "Shotgun"
        self.image = pyglet.resource.image('shotgun.png')
        super(Shotgun, self).__init__()

if __name__ == '__main__':
    pass