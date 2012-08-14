import pyglet
from pyglet.gl import glPushMatrix, glPopMatrix
from cocos.layer import Layer, ColorLayer
from cocos.director import director
from cocos.actions import StopGrid
from gameover import GameOver
import soundex

class View(Layer):
    def __init__(self, model, hud):
        super(View, self).__init__()
        width, height = director.get_window_size()
        #setup the view stuff here
        color_layer = ColorLayer( 112, 66, 20, 50, width = width, height=height )
        self.add(color_layer, z=-1)
        self.model = model
        #self.add(self.model.player, z=2)
        self.hud = hud
        self.bullet_batch = None
        self.model.push_handlers( # win / gameover / various in game effects
                                  self.on_level_complete,
                                  self.on_new_level,
                                  self.on_game_over,
                                  self.on_win,
                                  self.on_pause,
                                  self.on_resume,
                                  self.on_shoot,
                                  self.on_explode
                                  )
        self.hud.show_message( 'Get ready', self.model.start())

    def on_pause(self):
        self.hud.show_message('Paused!')
        self.model.controller().pause_controller()
        director.window.set_mouse_visible(True) 

    def on_resume(self):
        self.hud.show_message('Resuming')
        self.model.controller().resume_controller()
        director.window.set_mouse_visible(False)

    def on_enter(self):
        super(View, self).on_enter()
        director.window.set_mouse_visible(False) # hide the mouse with the direct pyglet.window call
        soundex.set_music('theme.ogg')
        soundex.play_music()
        #do sound stuff

    def on_exit(self):
        super(View, self).on_exit()
        director.window.set_mouse_visible(True)
        soundex.stop_music()
        #stop sound

    def on_level_complete(self):
        #sound stuffs can be done here.
        self.hud.show_message('Level complete', self.model.set_next_level)
        return True

    def on_new_level(self):
        #play new level sound
        self.stop()
        self.do(StopGrid())
        self.rotation = 0
        self.scale = 1
        return True

    def on_game_over(self):
        self.model.controller().pause_controller()
        self.parent.add(GameOver(win=False), z=10)
        return True

    def on_win(self):
        self.parent.add(GameOver(win=True), z=10)
        return True
    def on_explode(self):
        soundex.play('Hit_Hurt10.wav')
    def on_shoot(self):
        soundex.play('Laser_Shoot.wav')
        return True

    def update_bullet_batch(self):
        pyglet.gl.glPointSize(4.0)
        self.bullet_batch = pyglet.graphics.Batch()
        vert_l = []
        c = []
        for obj in self.model.player.active_bullets:
            try:
                x, y = obj.x, obj.y
            except AttributeError:
                pass
            else:
                if not obj.vanished:
                    x *= 2
                    y *= 2
                    x -= 1
                    y -= 1
                    vert_l.append(x)
                    vert_l.append(y)
                    c.append(166)
                    c.append(48)
                    c.append(48)

        self.bullet_batch.add(len(vert_l)/2, pyglet.gl.GL_POINTS, None, ('v2f\static', vert_l ) , ('c3B\static', c))

        vert_l = []
        c = []
        for obj in self.model.mob_active_bullets:
            try:
                x, y = obj.x, obj.y
            except AttributeError:
                pass
            else:
                if not obj.vanished:
                    x *= 2
                    y *= 2
                    x -= 1
                    y -= 1
                    vert_l.append(x)
                    vert_l.append(y)
                    c.append(255)
                    c.append(0)
                    c.append(255)
        self.bullet_batch.add(len(vert_l)/2, pyglet.gl.GL_POINTS, None, ('v2f\static', vert_l ) , ('c3B\static', c))

    def draw(self):
        self.update_bullet_batch()
        glPushMatrix()
        self.transform()
        for m in self.model.mobs:
            m.draw()
        self.model.player.draw()
        self.model.cursor.draw()
        self.bullet_batch.draw()
        glPopMatrix()