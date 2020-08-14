try:
    import sys
    # import random
    # import math
    # import os
    # import getopt
    import pygame as pg
    # import socket as sk
    # import pygame.locals as pglocals
    import handle_input as handlein
    import game_settings as gst
    import pacman
    import food
    from path_finding import A_star
except ImportError as err:
    print("Couldn't load module. %s" % (err))
    sys.exit(2)


#######################################################################
class Game:
    def __init__(self):
        # Setup screen configuration
        self.screen = None
        self.tittle = None
        self.background = None
        self.is_running = True

        # Setup game zone
        self.maze = None
        self.flatmaze = None
        self.maze_size = None

        # Setup characters
        self.pacman = None
        self.food = None

        # Path finding
        self.adjacent_nodes = None
        self.path = None

        # Countdown timer
        self.clock = None
        self.timer = 0

    def countdown(self):
        pass

    def find_path(self):
        return A_star(self.maze, self.adjacent_nodes, self.pacman.image.get, food)

    def execute(self):
        pg.init()
        self.initialize()
        # self.path = self.find_path()

        while self.is_running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.is_running = False

            self.timer -= self.dt
            if self.timer <= 0:
                self.timer = 10  # Reset it to 10 or do something else.

            # Countdown timer
            txt = pg.font.Font(None, 50)
            txtsurf = txt.render(str(int(self.timer)), True, [0, 0, 255])
            txtpos = txtsurf.get_rect()

            subsurf_w, subsurf_h = txtsurf.get_size()
            subsurf = pg.Surface((subsurf_w * 3, subsurf_h * 3))
            subsurfpos = subsurf.get_rect()

            txtpos.centerx = self.screen.get_rect().centerx
            subsurfpos.centerx = self.screen.get_rect().centerx

            self.screen.blit(subsurf, subsurfpos)
            self.screen.blit(txtsurf, txtpos)

            # Pacman test animation
            self.screen.blit(self.background, self.pacman.rect, self.pacman.screenview_pos)
            self.pacman.move()

            pg.display.flip()
            self.dt = self.clock.tick(2) / 1000  # / 1000 to convert to seconds.


if __name__ == '__main__':
    game = Game()
    game.execute()
