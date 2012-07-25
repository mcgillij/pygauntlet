'''
Created on Jul 25, 2012

@author: mcgillij
'''
from cocos.layer import ColorLayer
from cocos.director import director
import pyglet
from cocos.text import Label
from cocos.actions import Accelerate, Rotate, Reverse, Repeat, Delay

class GameOver(ColorLayer):
    is_event_handler = True
    def __init__(self, win = False):
        super(GameOver, self).__init__(32, 32, 32, 64)
        width, height = director.get_window_size()

        if win:
            #play win sound
            msg = 'You win!'
        else:
            #play fail sound
            msg = 'Game Over Man! Game Over!'

        label = Label(msg, font_name='Times New Roman', font_size=54, anchor_x='center', anchor_y='center')
        label.position = (width/2.0, height/2.0)
        self.add(label)
        angle = 5
        duration = 0.05
        accel = 2
        rotation = Accelerate(Rotate(angle, duration//2), accel)
        rotation2 = Accelerate(Rotate(-angle*2, duration), accel)
        effect = rotation + (rotation2 + Reverse(rotation2)) * 4 + Reverse(rotation)
        label.do(Repeat(Delay(5) + effect))
        # do high score stuff here

    def on_key_press(self, k, m):
        if (k == pyglet.window.key.ESCAPE):
            director.pop()
            return True
if __name__ == '__main__':
    pass