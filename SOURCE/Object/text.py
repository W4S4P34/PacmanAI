# import handle_input as input
# import game_settings as settings
# import game_flags as flags
import pygame as pg


class Text(pg.sprite.Sprite):
    # Constructor
    def __init__(self, text, font, color):
        # Call the parent class (Sprite) constructor
        pg.sprite.Sprite.__init__(self)
        self.font = font
        self.color = color
        self.text = self.font.render(text, 1, self.color)
        self.text_rect = self.text.get_rect()

    def update(self, text):
        self.text = self.font.render(text, 1, self.color)
        self.text_rect = self.text.get_rect()
