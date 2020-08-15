import handle_input as input
# import game_settings as settings
import game_flags as flags
import pygame as pg


class Pacman(pg.sprite.Sprite):
    # Constructor
    def __init__(self, pos=None):
        # Call the parent class (Sprite) constructor
        pg.sprite.Sprite.__init__(self)
        size = (32, 32)

        self.pos = pos
        position = tuple([ele * 32 for ele in reversed(self.pos)])

        self.rect = pg.Rect(position, size)
        self.images_right = []
        for char_img in flags.MAIN_CHARACTER_RIGHT:
            img, _ = input.load_image(flags.CHARACTER_TYPE, char_img)
            self.images_right.append(img)

        self.images = self.images_right.copy()

        self.images_left = []
        for char_img in flags.MAIN_CHARACTER_LEFT:
            img, _ = input.load_image(flags.CHARACTER_TYPE, char_img)
            self.images_left.append(img)

        self.images_up = []
        for char_img in flags.MAIN_CHARACTER_UP:
            img, _ = input.load_image(flags.CHARACTER_TYPE, char_img)
            self.images_up.append(img)

        self.images_down = []
        for char_img in flags.MAIN_CHARACTER_DOWN:
            img, _ = input.load_image(flags.CHARACTER_TYPE, char_img)
            self.images_down.append(img)

        self.index = 0
        self.image = self.images[self.index]

        self.x_axis = None
        self.y_axis = None

        self.animation_time = 0.1
        self.current_time = 0

        self.animation_frames = 2
        self.current_frame = 0

    def update_time_dependent(self, dt):
        """
        Updates the image of Sprite approximately every 0.1 second.

        Args:
            dt: Time elapsed between each frame.
        """
        if self.x_axis > 0:
            self.images = self.images_right
        elif self.x_axis < 0:
            self.images = self.images_left

        if self.y_axis > 0:
            self.images = self.images_down
        elif self.y_axis < 0:
            self.images = self.images_up

        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

    def update_frame_dependent(self):
        """
        Updates the image of Sprite every 6 frame (approximately every 0.1 second if frame rate is 60).
        """
        if self.x_axis > 0:
            self.images = self.images_right
        elif self.x_axis < 0:
            self.images = self.images_left

        if self.y_axis > 0:
            self.images = self.images_down
        elif self.y_axis < 0:
            self.images = self.images_up

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

    # Movement
    def move(self, dest, dt):
        self.dest = dest

        dst = reversed(dest)
        src = reversed(self.pos)

        self.x_axis, self.y_axis = tuple([destination - source for source, destination in zip(src, dst)])

        if self.x_axis > 0:
            self.rect = self.rect.move(1, 0)
        elif self.x_axis < 0:
            self.rect = self.rect.move(-1, 0)

        if self.y_axis > 0:
            self.rect = self.rect.move(0, 1)
        elif self.y_axis < 0:
            self.rect = self.rect.move(0, -1)
