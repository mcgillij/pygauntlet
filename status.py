'''
Created on Jul 25, 2012

@author: mcgillij
'''
__all__ = ['status']
class Status(object):
    def __init__(self):
        self.score = 0
        self.level = None
        self.level_index = None

    def reset(self):
        self.score = 0
        self.level = None
        self.level_index = None
status = Status()

if __name__ == '__main__':
    pass