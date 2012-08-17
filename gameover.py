import pyglet
from cocos.layer import ColorLayer
from cocos.director import director
from cocos.text import Label
from cocos.actions import Accelerate, Rotate, Reverse, Repeat, Delay
import hiscore
import status

class GameOver(ColorLayer):
    is_event_handler = True
    def __init__( self, win = False):
        super(GameOver,self).__init__( 32,32,32,64)

        w,h = director.get_window_size()

        if win:
            msg = 'YOU WIN'
        else:
            msg = 'GAME OVER'

        label = Label(msg,
                    font_name='Times New Roman',
                    font_size=54,
                    anchor_y='center',
                    anchor_x='center' )
        label.position =  ( w/2.0, h/2.0 )

        self.add( label )

        angle = 5
        duration = 0.05
        accel = 2
        rot = Accelerate(Rotate( angle, duration//2 ), accel)
        rot2 = Accelerate(Rotate( -angle*2, duration), accel)
        effect = rot + (rot2 + Reverse(rot2)) * 4 + Reverse(rot)
        
        label.do( Repeat( Delay(5) + effect ) )

        if hiscore.hiscore.is_in( status.status.score ):
            self.hi_score = True

            label = Label('Enter your name:',
                        font_name='Times New Roman',
                        font_size=36,
                        anchor_y='center',
                        anchor_x='center',
                        color=(204, 164, 164, 255),
                        )
            label.position =  ( w/2.0, h/2.0 )
            label.position = (w//2, 300)
            self.add( label )

            self.name= Label('',
                        font_name='Times New Roman',
                        font_size=36,
                        anchor_y='center',
                        anchor_x='center',
                        color=(204, 164, 164, 255),
                        )
            self.name.position=(w//2,250)
            self.add(self.name)
        else:
            self.hi_score = False

    def on_key_press( self, k, m ):
        if not self.hi_score and (k == pyglet.window.key.ENTER or k == pyglet.window.key.ESCAPE):
            director.pop()
            return True

        if self.hi_score:
            if k == pyglet.window.key.BACKSPACE:
                self.name.element.text = self.name.element.text[0:-1]
                return True
            elif k == pyglet.window.key.ENTER:
                hiscore.hiscore.add( status.status.score,self.name.element.text)
                director.pop()
                return True
        return False

    def on_text( self, t ):
        if not self.hi_score:
            return False

        if t=='\r':
            return True

        self.name.element.text += t