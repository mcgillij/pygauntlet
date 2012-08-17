import pyglet
from cocos.scene import Scene
from cocos.director import director
from gamelayers import IntroLayer

if __name__ == '__main__':
    pyglet.resource.path.append('assets')
    pyglet.resource.reindex()
    director.init(resizable = True, width=800, height=800)
    scene = Scene()
    scene.add(IntroLayer(), z=1)
    director.run(scene)