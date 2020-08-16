import handle_input as input
import game_flags as flags
import pygame as pg


class MonsterEasy(pg.sprite.Sprite):
    # Constructor
    def __init__(self, pos=(-1, -1)):
        # Call the parent class (Sprite) constructor
        pg.sprite.Sprite.__init__(self)
        size = (32, 32)
        self.pos = pos
        position = tuple([ele * 32 for ele in reversed(self.pos)])
        self.rect = pg.Rect(position, size)

        self.images = []
        for monster_img in flags.MONSTER_RED:
            img, _ = input.load_image(flags.CHARACTER_TYPE, monster_img)
            self.images.append(img)

        self.index = 0
        self.image = self.images[self.index]

        self.animation_time = 0.1
        self.current_time = 0

        self.animation_frames = 8
        self.current_frame = 0

    def update_time_dependent(self, dt):
        """
        Updates the image of Sprite approximately every 0.1 second.

        Args:
            dt: Time elapsed between each frame.
        """
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

    def update_frame_dependent(self):
        """
        Updates the image of Sprite every 6 frame (approximately every 0.1 second if frame rate is 60).
        """
        self.current_frame += 1
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

    def update(self, dt):
        """This is the method that's being called when 'all_sprites.update(dt)' is called."""
        # Switch between the two update methods by commenting/uncommenting.
        self.update_time_dependent(dt)
        # self.update_frame_dependent()
