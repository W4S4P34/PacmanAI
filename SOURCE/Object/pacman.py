import handle_input as input
# import game_settings as settings
import game_flags as flags
import pygame as pg


class Pacman(pg.sprite.Sprite):
    # Constructor
    def __init__(self, pos=None):
        # Call the parent class (Sprite) constructor
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = input.load_image(flags.CHARACTER_TYPE, flags.MAIN_CHARACTER)
        if pos:
            self.pos = reversed(pos)
            self.screenview_pos = tuple([ele * 32 for ele in list(self.pos)] + [32, 32])
        # self.previous_rect = self.rect

        # self.step = 0
        # self.pos = tuple(list(reversed(pos)) + [32, 32])

    # def move(self):
    #     self.previous_rect = self.rect
    #     self.rect = self.rect.move((1, 0))
    #     self.step += 1
    #
    #     cur_x_coor, cur_y_coor, _, _ = self.rect
    #     last_x_coor, last_y_coor, _, _ = self.previous_rect
    #
    #     print(self.rect, self.previous_rect, self.screenview_pos)
    #     self.screenview_pos = tuple([abs(cur_x_coor - last_x_coor) * 32,
    #                                 abs(cur_y_coor - last_y_coor) * 32,
    #                                 32, 32])
    #
    #     if self.step == 32:
    #         self.pos = tuple([abs(cur_x_coor - last_x_coor) / 32, abs(cur_y_coor - last_y_coor) / 32])
    #         self.step = 0
