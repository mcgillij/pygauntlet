from cocos.layer import Layer, ColorLayer
from cocos.text import Label
import pyglet
from pyglet.gl import glPushMatrix, glPopMatrix
from cocos.director import director
from cocos.actions import Accelerate, MoveBy, Delay, Hide, CallFunc
from status import status
import hiscore
class BackgroundLayer(Layer):
    def __init__(self):
        super(BackgroundLayer, self).__init__()
        self.img = pyglet.resource.image('background.png')
    def draw(self):
        glPushMatrix()
        self.transform()
        self.img.blit(0, 0)
        glPopMatrix()

class ScoreLayer(Layer):
    def __init__(self):
        width, height = director.get_window_size()
        super(ScoreLayer, self).__init__()
        self.add(ColorLayer(32, 32, 32, 32, width=width, height=height), z=-1)
        self.position = (0, height-48)
        self.score = Label('Score:', font_size=36,
                           font_name='Times New Roman',
                           color=(255,255,255,255),
                           anchor_x='left',
                           anchor_y='bottom')
        self.score.position = (0, 0)
        self.add(self.score)
        #self.level = Label('Level:', font_size=36,
        #                 font_name = 'Times New Roman',
         #                color = (255, 255, 255, 255),
         #                anchor_x = 'left',
         #                anchor_y = 'bottom')
        #self.add(self.level)

    def draw(self):
        super(ScoreLayer, self).draw()
        self.score.element.text = 'Score:%d' % status.score
        
        #level = status.level_index or 0
        #self.level.element.text = 'Level:%d', level
        
class MessageLayer(Layer):
    def show_message(self, message, callback=None):
        width, height = director.get_window_size()
        self.message = Label(message, 
                             font_size=52,
                             font_name='Times New Roman',
                             anchor_x='center',
                             anchor_y='center')
        self.message.position = (width/2.0, height)
        self.add(self.message)
        
        actions = Accelerate(MoveBy( (0,-height/2.0), duration=0.5)) + \
                    Delay(1) +  \
                    Accelerate(MoveBy( (0,-height/2.0), duration=0.5)) + \
                    Hide()

        if callback:
            actions += CallFunc( callback )

        self.message.do( actions )

class HUD(Layer):
    def __init__(self):
        super(HUD, self).__init__()
        self.add(ScoreLayer())
        self.add(MessageLayer(), name='message')

    def show_message(self, message, callback = None):
        self.get('message').show_message(message, callback)

class HiScoresLayer(ColorLayer):
    FONT_SIZE = 30
    is_event_handler = True
    def __init__(self):
        width, height = director.get_window_size()
        super(HiScoresLayer, self).__init__(32, 32, 32, 16, width=width, height=height-86)
        self.font_title = {}
        self.font_title['font_name'] = 'Times New Roman'
        self.font_title['font_size'] = 72
        self.font_title['color'] = (204, 164, 164, 255)
        self.font_title['anchor_x'] = 'center'
        self.font_title['anchor_y'] = 'top'
        title = Label('Scores!', **self.font_title)
        title.position = (width/2.0, height)
        self.add(title, z=1)
        self.table = None

    def on_enter(self):
        super(HiScoresLayer, self).on_enter()
        scores = hiscore.hiscore.get()

        if self.table:
            self.remove_old()

        self.table =[]
        for idx,s in enumerate(scores):

            pos= Label( '%d:' % (idx+1), font_name='Times New Roman',
                        font_size=self.FONT_SIZE,
                        anchor_y='top',
                        anchor_x='left',
                        color=(255,255,255,255) )

            name = Label( s[1], font_name='Times New Roman',
                        font_size=self.FONT_SIZE,
                        anchor_y='top',
                        anchor_x='left',
                        color=(255,255,255,255) )

            score = Label( str(s[0]), font_name='Times New Roman',
                        font_size=self.FONT_SIZE,
                        anchor_y='top',
                        anchor_x='right',
                        color=(255,255,255,255) )

            self.table.append( (pos,name,score) )

        self.process_table()
    def remove_old( self ):
        for item in self.table:
            pos,name,score = item
            self.remove(pos)
            self.remove(name)
            self.remove(score)
        self.table = None

    def process_table( self ):
        w,h = director.get_window_size()

        for idx,item in enumerate(self.table):
            pos,name,score = item

            posy = h - 100 - ( (self.FONT_SIZE+15) * idx )

            pos.position=( 5, posy)
            name.position=( 48, posy)
            score.position=( w-150, posy )

            self.add( pos, z=2 )
            self.add( name, z=2 )
            self.add( score, z=2 )

    def on_key_press(self, k, m):
        if k in (pyglet.window.key.ENTER, pyglet.window.key.ESCAPE, pyglet.window.key.SPACE):
            self.parent.switch_to(0)
            return True

    def on_mouse_release(self, x, y, b, m):
        self.parent.switch_to(0)
        return True
