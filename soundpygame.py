import pygame
import pyglet
import os
SOUND = True
MUSIC = True
pygame.mixer.init()
pygame.init()
pygame.mixer.music.load(os.path.join('assets', 'theme.ogg'))

sound_vol = 0.5

def set_music(name):
    pygame.mixer.music.play(-1)

def music_volume(vol):
    pass 

def queue_music(name):
    pass

def play_music():
    pygame.mixer.music.play(-1)

def stop_music():
    pygame.mixer.music.stop()

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