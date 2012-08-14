import pygame
import pyglet
import os
SOUND = True
MUSIC = True
pygame.mixer.init()
pygame.init()
pygame.mixer.music.load(os.path.join('assets', 'theme.ogg'))

sound_vol = 0.7

def set_music(name):
    pygame.mixer.music.play(-1)

def music_volume(vol):
    pass #music_player.volume=vol

def queue_music(name):
    #global current_music

    #if not have_avbin:
    #    return

#    if name == current_music:
#        return

    #music_player.queue(pyglet.resource.media(name, streaming=True))
    #music_player.eos_action = 'next'
    pass


def play_music():
    pygame.mixer.music.play(-1)

def stop_music():
#    import pdb
#    pdb.set_trace()
    pygame.mixer.music.stop()

#
# SOUND
#
sounds = {}

def load(name, streaming=False):
    if not SOUND:
        return

    if name not in sounds:
        sounds[name] = pyglet.resource.media(name, streaming=streaming)

    return sounds[name]

def play(name):
    if not SOUND:
        return
    load(name)
    a = sounds[name].play().volume = sound_vol

def sound_volume( vol ):
    global sound_vol
    sound_vol = vol
