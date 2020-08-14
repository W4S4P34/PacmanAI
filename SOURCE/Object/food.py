import handle_input as input
# import game_settings as settings
import game_flags as flags
import pygame as pg


class Food(pg.sprite.Sprite):
    # Constructor
    def __init__(self, pos=None):
        # Call the parent class (Sprite) constructor
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = input.load_image(flags.FOOD_TYPE, flags.FOOD)
        if pos:
            self.pos = reversed(pos)
            self.screenview_pos = tuple([ele * 32 for ele in list(self.pos)] + [32, 32])
