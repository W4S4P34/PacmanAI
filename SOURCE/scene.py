import handle_input as input
import maze_drawer as drawer
import game_flags as flags
import game_settings as settings
from Object import pacman
from Object import food
import pygame as pg
import os


class SceneBase:
    def __init__(self):
        self.next = self

    def ProcessInput(self, events, pressed_keys):
        print("Did not override this in the child class")

    def Update(self):
        print("Did not override this in the child class")

    def Render(self, screen):
        print("Did not override this in the child class")

    def SwitchToScene(self, next_scene):
        self.next = next_scene

    def Terminate(self):
        self.SwitchToScene(None)


class TitleScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        # INTRO
        # Button
        self.is_over_play_button = False
        self.play_button, self.play_button_rect = input.load_image(flags.MISC_TYPE, flags.BUTTONBG)
        self.play_button_rect = self.play_button_rect.move(245, 250)
        # Text
        pg.font.init()
        path = os.path.join(settings.PATH, 'ASSET', 'Fonts', 'Fipps-Regular.otf')
        self.title_font = pg.font.Font(path, 30)
        self.title_text = self.title_font.render("PACMAN: We will survive!", 1, (255, 255, 255))
        self.title_text_rect = self.title_text.get_rect()
        self.play_font = pg.font.Font(path, 15)
        self.play_text = self.play_font.render("Play", 1, (255, 255, 255))
        self.play_text_rect = self.play_text.get_rect()
        # SETTINGS
        # Button
        self.is_over_lvl1_button = False
        self.is_over_lvl2_button = False
        self.is_over_lvl3_button = False
        self.is_over_lvl4_button = False
        self.level_1_button, self.level_1_button_rect = input.load_image(flags.MISC_TYPE, flags.BUTTONBG)
        self.level_1_button_rect = self.level_1_button_rect.move(145, 250)
        self.level_2_button, self.level_2_button_rect = input.load_image(flags.MISC_TYPE, flags.BUTTONBG)
        self.level_2_button_rect = self.level_2_button_rect.move(345, 250)
        self.level_3_button, self.level_3_button_rect = input.load_image(flags.MISC_TYPE, flags.BUTTONBG)
        self.level_3_button_rect = self.level_3_button_rect.move(145, 300)
        self.level_4_button, self.level_4_button_rect = input.load_image(flags.MISC_TYPE, flags.BUTTONBG)
        self.level_4_button_rect = self.level_4_button_rect.move(345, 300)
        # Text
        self.lvl1_text = self.play_font.render("Level 1", 1, (255, 255, 255))
        self.lvl1_text_rect = self.lvl1_text.get_rect()
        self.lvl2_text = self.play_font.render("Level 2", 1, (255, 255, 255))
        self.lvl2_text_rect = self.lvl2_text.get_rect()
        self.lvl3_text = self.play_font.render("Level 3", 1, (255, 255, 255))
        self.lvl3_text_rect = self.lvl3_text.get_rect()
        self.lvl4_text = self.play_font.render("Level 4", 1, (255, 255, 255))
        self.lvl4_text_rect = self.lvl4_text.get_rect()
        # State
        self.state = flags.INTRO

    def ProcessInput(self, events, pressed_keys):
        if self.state == flags.INTRO:
            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.play_button_rect.collidepoint(pg.mouse.get_pos()):
                        self.state = flags.SETTINGS
                        self.is_over_play_button = False
        elif self.state == flags.SETTINGS:
            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.level_1_button_rect.collidepoint(pg.mouse.get_pos()):
                        self.SwitchToScene(LevelOne())
                        self.is_over_lvl1_button = False
                    elif self.level_2_button_rect.collidepoint(pg.mouse.get_pos()):
                        self.SwitchToScene(LevelTwo())
                        self.is_over_lvl2_button = False
                    elif self.level_3_button_rect.collidepoint(pg.mouse.get_pos()):
                        self.SwitchToScene(LevelThree())
                        self.is_over_lvl3_button = False
                    elif self.level_4_button_rect.collidepoint(pg.mouse.get_pos()):
                        self.SwitchToScene(LevelFour())
                        self.is_over_lvl4_button = False

    def Update(self):
        pass

    def Render(self, screen):
        if self.state == flags.INTRO:
            # Add background
            background, background_rect = input.load_image(flags.MISC_TYPE, flags.BG)
            screen.blit(background, background_rect)

            # Add button
            # Checks if mouse position is over the button
            if self.play_button_rect.collidepoint(pg.mouse.get_pos()):
                if not self.is_over_play_button:
                    self.is_over_play_button = True
                    self.play_button.fill((25, 25, 25, 0), special_flags=pg.BLEND_RGBA_SUB)
            else:
                self.is_over_play_button = False
                self.play_button, _ = input.load_image(flags.MISC_TYPE, flags.BUTTONBG)

            # Add text to button
            self.title_text_rect.centerx = screen.get_rect().centerx
            self.play_text_rect.center = self.play_button_rect.center
            screen.blit(self.title_text, self.title_text_rect)
            screen.blit(self.play_button, self.play_button_rect)
            screen.blit(self.play_text, self.play_text_rect)
        elif self.state == flags.SETTINGS:
            # Add background
            background, background_rect = input.load_image(flags.MISC_TYPE, flags.BG)
            screen.blit(background, background_rect)

            # Add button
            # Checks if mouse position is over the button
            if self.level_1_button_rect.collidepoint(pg.mouse.get_pos()):
                if not self.is_over_lvl1_button:
                    self.is_over_lvl1_button = True
                    self.level_1_button.fill((25, 25, 25, 0), special_flags=pg.BLEND_RGBA_SUB)
            else:
                self.is_over_lvl1_button = False
                self.level_1_button, _ = input.load_image(flags.MISC_TYPE, flags.BUTTONBG)

            # Checks if mouse position is over the button
            if self.level_2_button_rect.collidepoint(pg.mouse.get_pos()):
                if not self.is_over_lvl2_button:
                    self.is_over_lvl2_button = True
                    self.level_2_button.fill((25, 25, 25, 0), special_flags=pg.BLEND_RGBA_SUB)
            else:
                self.is_over_lvl2_button = False
                self.level_2_button, _ = input.load_image(flags.MISC_TYPE, flags.BUTTONBG)

            # Checks if mouse position is over the button
            if self.level_3_button_rect.collidepoint(pg.mouse.get_pos()):
                if not self.is_over_lvl3_button:
                    self.is_over_lvl3_button = True
                    self.level_3_button.fill((25, 25, 25, 0), special_flags=pg.BLEND_RGBA_SUB)
            else:
                self.is_over_lvl3_button = False
                self.level_3_button, _ = input.load_image(flags.MISC_TYPE, flags.BUTTONBG)

            # Checks if mouse position is over the button
            if self.level_4_button_rect.collidepoint(pg.mouse.get_pos()):
                if not self.is_over_lvl4_button:
                    self.is_over_lvl4_button = True
                    self.level_4_button.fill((25, 25, 25, 0), special_flags=pg.BLEND_RGBA_SUB)
            else:
                self.is_over_lvl4_button = False
                self.level_4_button, _ = input.load_image(flags.MISC_TYPE, flags.BUTTONBG)

            # Add text to button
            screen.blit(self.title_text, self.title_text_rect)
            screen.blit(self.level_1_button, self.level_1_button_rect)
            screen.blit(self.level_2_button, self.level_2_button_rect)
            screen.blit(self.level_3_button, self.level_3_button_rect)
            screen.blit(self.level_4_button, self.level_4_button_rect)
            self.lvl1_text_rect.center = self.level_1_button_rect.center
            screen.blit(self.lvl1_text, self.lvl1_text_rect)
            self.lvl2_text_rect.center = self.level_2_button_rect.center
            screen.blit(self.lvl2_text, self.lvl2_text_rect)
            self.lvl3_text_rect.center = self.level_3_button_rect.center
            screen.blit(self.lvl3_text, self.lvl3_text_rect)
            self.lvl4_text_rect.center = self.level_4_button_rect.center
            screen.blit(self.lvl4_text, self.lvl4_text_rect)


class LevelOne(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        # Select map
        self.background, self.background_rect = input.load_image(flags.MISC_TYPE, flags.LVLBG)
        # Level
        self.level = flags.LVL1
        self.map = None
        # Gameplay
        self.maze = None
        self.size = None
        self.pacman = pacman.Pacman()
        self.food = food.Food()
        self.adjacents = None
        self.path = None
        # State
        self.state = flags.MAPSELECT
        # Text
        path = os.path.join(settings.PATH, 'ASSET', 'Fonts', 'Fipps-Regular.otf')
        self.map_font = pg.font.Font(path, 20)
        self.map1_text = self.map_font.render("Map 1", 1, (0, 0, 0))
        self.map1_text_rect = self.map1_text.get_rect()
        self.map2_text = self.map_font.render("Map 2", 1, (0, 0, 0))
        self.map2_text_rect = self.map2_text.get_rect()
        # Button
        self.is_over_map1_button = False
        self.is_over_map2_button = False
        self.map_1_button, self.map_1_button_rect = input.load_image(flags.MISC_TYPE, flags.MAPBG)
        self.map_1_button_rect = self.map_1_button_rect.move(125, 50)
        self.map_2_button, self.map_2_button_rect = input.load_image(flags.MISC_TYPE, flags.MAPBG)
        self.map_2_button_rect = self.map_2_button_rect.move(365, 50)
        # Maze Drawer
        self.drawer = drawer.MazeDrawer()

    def ProcessInput(self, events, pressed_keys):
        if self.state == flags.MAPSELECT:
            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.map_1_button_rect.collidepoint(pg.mouse.get_pos()):
                        self.state = flags.PLAYING
                        self.map = flags.MAP1
                        self.size, self.maze, pacmanpos = input.read_file(self.level, self.map)
                        self.adjacents, foodpos = input.handle_adjacent(self.maze, self.size)
                        self.pacman = pacman.Pacman(pacmanpos)
                        self.food = food.Food(foodpos)
                        self.is_over_map1_button = False
                    elif self.map_2_button_rect.collidepoint(pg.mouse.get_pos()):
                        self.state = flags.PLAYING
                        self.map = flags.MAP2
                        self.size, self.maze, pacmanpos = input.read_file(self.level, self.map)
                        self.adjacents, foodpos = input.handle_adjacent(self.maze, self.size)
                        self.pacman = pacman.Pacman(pacmanpos)
                        self.food = food.Food(foodpos)
                        self.is_over_map2_button = False

    def Update(self):
        pass

    def Render(self, screen):
        if self.state == flags.MAPSELECT:
            screen.blit(self.background, self.background_rect)

            if self.map_1_button_rect.collidepoint(pg.mouse.get_pos()):
                if not self.is_over_map1_button:
                    self.is_over_map1_button = True
                    self.map_1_button.fill((25, 25, 25, 0), special_flags=pg.BLEND_RGBA_SUB)
            else:
                self.is_over_map1_button = False
                self.map_1_button, _ = input.load_image(flags.MISC_TYPE, flags.MAPBG)

            # Checks if mouse position is over the button
            if self.map_2_button_rect.collidepoint(pg.mouse.get_pos()):
                if not self.is_over_map2_button:
                    self.is_over_map2_button = True
                    self.map_2_button.fill((25, 25, 25, 0), special_flags=pg.BLEND_RGBA_SUB)
            else:
                self.is_over_map2_button = False
                self.map_2_button, _ = input.load_image(flags.MISC_TYPE, flags.MAPBG)

            screen.blit(self.map_1_button, self.map_1_button_rect)
            screen.blit(self.map_2_button, self.map_2_button_rect)
            self.map1_text_rect.center = self.map_1_button_rect.center
            screen.blit(self.map1_text, self.map1_text_rect)
            self.map2_text_rect.center = self.map_2_button_rect.center
            screen.blit(self.map2_text, self.map2_text_rect)

        elif self.state == flags.PLAYING:
            width, height = self.size
            width *= 32
            height = (height * 32) + 64
            pg.display.set_mode((width, height))
            self.drawer.maze, self.drawer.size = self.maze, self.size
            self.drawer.setup_maze()
            screen.blit(self.drawer.background, self.drawer.background_rect)
            screen.blit(self.pacman.image, self.pacman.screenview_pos)
            screen.blit(self.food.image, self.food.screenview_pos)


class LevelTwo(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self):
        pass

    def Render(self, screen):
        # The game scene is just a blank blue screen
        screen.fill((0, 0, 255))


class LevelThree(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self):
        pass

    def Render(self, screen):
        # The game scene is just a blank blue screen
        screen.fill((0, 0, 255))


class LevelFour(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self):
        pass

    def Render(self, screen):
        # The game scene is just a blank blue screen
        screen.fill((0, 0, 255))
