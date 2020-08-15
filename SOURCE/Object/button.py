import handle_input as input
# import game_settings as settings
import game_flags as flags
import pygame as pg


class Button(pg.sprite.Sprite):
    # Constructor
    def __init__(self, image_flag=None):
        # Call the parent class (Sprite) constructor
        pg.sprite.Sprite.__init__(self)
        self.image_flag = image_flag
        self.image, self.rect = input.load_image(flags.MISC_TYPE, self.image_flag)
        self.is_over = False

    def switch(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            if not self.is_over:
                self.is_over = True
                self.image.fill((25, 25, 25, 0), special_flags=pg.BLEND_RGBA_SUB)
        else:
            self.is_over = False
            self.image, _ = input.load_image(flags.MISC_TYPE, self.image_flag)
