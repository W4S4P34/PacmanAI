# import handle_input as input
# import game_settings as settings
# import game_flags as flags
import pygame as pg


class Text(pg.sprite.Sprite):
    # Constructor
    def __init__(self, text, font, color):
        # Call the parent class (Sprite) constructor
        pg.sprite.Sprite.__init__(self)
        self.map_font = font
        self.text = self.map_font.render(text, 1, color)
        self.text_rect = self.text.get_rect()
