import handle_input as input
import game_flags as flags
import game_settings as settings
from Object import button
from Object import text
from Object import pacman
from Object import food
from Object import maze_drawer as drawer
from Level_1 import path_finding as find_lvl_1
import pygame as pg
import os


class SceneBase:
    def __init__(self, screen=None):
        self.next = self
        self.screen = screen

    def ProcessInput(self, events, pressed_keys):
        print("Did not override this in the child class")

    def Update(self, deltatime):
        print("Did not override this in the child class")

    def Render(self):
        print("Did not override this in the child class")

    def SwitchToScene(self, next_scene):
        self.next = next_scene

    def Terminate(self):
        self.SwitchToScene(None)


class TitleScene(SceneBase):
    def __init__(self, screen=None):
        SceneBase.__init__(self, screen)
        # Add background
        self.background, self.background_rect = input.load_image(flags.MISC_TYPE, flags.BG)
        self.screen.blit(self.background, self.background_rect, self.background_rect)
        # Buttons
        self.play_button = button.Button(flags.BUTTONBG)
        self.play_button.rect = self.play_button.rect.move(245, 250)
        # Texts
        pg.font.init()
        path = os.path.join(settings.PATH, 'ASSET', 'Fonts', 'Fipps-Regular.otf')

        title_font = pg.font.Font(path, 30)
        self.title = text.Text('PACMAN: We will survive!', title_font, (255, 255, 255))
        self.title.text_rect.centerx = self.screen.get_rect().centerx
        self.screen.blit(self.title.text, self.title.text_rect)

        play_font = pg.font.Font(path, 15)
        self.play_text = text.Text('Play', play_font, (255, 255, 255))
        self.play_text.text_rect.center = self.play_button.rect.center
        # State
        self.state = flags.INTRO

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.play_button.rect.collidepoint(pg.mouse.get_pos()):
                    self.state = flags.LVLSELECT
                    self.SwitchToScene(LevelSettings(self.screen))
                    self.play_button.is_over = False

    def Update(self, deltatime):
        ##################################################################################
        # Collisions
        # Checks if mouse position is over the button
        self.play_button.switch()
        ##################################################################################

    def Render(self):
        self.screen.blit(self.play_button.image, self.play_button.rect)
        self.screen.blit(self.play_text.text, self.play_text.text_rect)


class LevelSettings(SceneBase):
    def __init__(self, screen=None):
        SceneBase.__init__(self, screen)
        # Add background
        self.background, self.background_rect = input.load_image(flags.MISC_TYPE, flags.BG)
        self.screen.blit(self.background, self.background_rect, self.background_rect)
        # SETTINGS
        # Title
        path = os.path.join(settings.PATH, 'ASSET', 'Fonts', 'Fipps-Regular.otf')

        title_font = pg.font.Font(path, 30)
        self.title = text.Text('PACMAN: We will survive!', title_font, (255, 255, 255))
        self.title.text_rect.centerx = self.screen.get_rect().centerx
        self.screen.blit(self.title.text, self.title.text_rect)
        # Buttons
        self.button_list = []
        for _ in range(4):
            self.button_list.append(button.Button(flags.BUTTONBG))

        for idx, bt in enumerate(self.button_list):
            row_idx = idx // 2
            col_idx = idx % 2
            x_coor = 100 + col_idx * (150 + 70 + 70)
            y_coor = 250 + row_idx * (35 + 30)
            bt.rect = bt.rect.move((x_coor, y_coor))
        # Texts
        self.text_list = []
        button_font = pg.font.Font(path, 15)

        for idx in range(len(self.button_list)):
            level = 'Level ' + str(idx + 1)
            self.text_list.append(text.Text(level, button_font, (255, 255, 255)))

        for idx, t in enumerate(self.text_list):
            t.text_rect.center = self.button_list[idx].rect.center
        # State
        self.state = flags.LVLSELECT

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                for idx, bt in enumerate(self.button_list):
                    if bt.rect.collidepoint(pg.mouse.get_pos()):
                        if idx == 0:
                            self.SwitchToScene(MapSettings(self.screen, flags.LVL1))
                            bt.is_over = False
                        elif idx == 1:
                            self.SwitchToScene(MapSettings(self.screen, flags.LVL2))
                            bt.is_over = False
                        elif idx == 2:
                            self.SwitchToScene(MapSettings(self.screen, flags.LVL3))
                            bt.is_over = False
                        elif idx == 3:
                            self.SwitchToScene(MapSettings(self.screen, flags.LVL4))
                            bt.is_over = False

    def Update(self, deltatime):
        ##################################################################################
        # Collisions
        for bt in self.button_list:
            bt.switch()
        ##################################################################################

    def Render(self):
        for bt in self.button_list:
            self.screen.blit(bt.image, bt.rect)
        for t in self.text_list:
            self.screen.blit(t.text, t.text_rect)


class MapSettings(SceneBase):
    def __init__(self, screen=None, level=None):
        SceneBase.__init__(self, screen)
        # Add background
        self.background, self.background_rect = input.load_image(flags.MISC_TYPE, flags.LVLBG)
        self.screen.blit(self.background, self.background_rect, self.background_rect)
        # Attributes
        self.level = level
        self.map = None
        # Button
        """Add to button list"""
        self.button_list = []
        if self.level == flags.LVL1:
            for idx in range(flags.MAPNO1):
                self.button_list.append(button.Button(flags.MAPBG))
        elif self.level == flags.LVL2:
            for idx in range(flags.MAPNO2):
                self.button_list.append(button.Button(flags.MAPBG))
        elif self.level == flags.LVL3:
            for idx in range(flags.MAPNO3):
                self.button_list.append(button.Button(flags.MAPBG))
        elif self.level == flags.LVL4:
            for idx in range(flags.MAPNO4):
                self.button_list.append(button.Button(flags.MAPBG))
        """Modify buttons' rects"""
        for idx, bt in enumerate(self.button_list):
            row_idx = idx // 10
            col_idx = idx % 10
            x_coor = 11 + col_idx * (60 + 1 + 1)
            y_coor = 60 + row_idx * (60 + 1 + 1)
            bt.rect = bt.rect.move((x_coor, y_coor))
        # Text
        path = os.path.join(settings.PATH, 'ASSET', 'Fonts', 'Fipps-Regular.otf')

        title_font = pg.font.Font(path, 30)
        self.title = text.Text('SELECT MAP', title_font, (255, 255, 255))
        self.title.text_rect.centerx = self.screen.get_rect().centerx
        self.screen.blit(self.title.text, self.title.text_rect)

        map_font = pg.font.Font(path, 15)
        self.text_list = []
        if self.level == flags.LVL1:
            for idx in range(flags.MAPNO1):
                map_name = str(idx + 1)
                self.text_list.append(text.Text(map_name, map_font, (255, 255, 255)))
        elif self.level == flags.LVL2:
            for idx in range(flags.MAPNO2):
                map_name = str(idx + 1)
                self.text_list.append(text.Text(map_name, map_font, (255, 255, 255)))
        elif self.level == flags.LVL3:
            for idx in range(flags.MAPNO3):
                map_name = str(idx + 1)
                self.text_list.append(text.Text(map_name, map_font, (255, 255, 255)))
        elif self.level == flags.LVL4:
            for idx in range(flags.MAPNO4):
                map_name = str(idx + 1)
                self.text_list.append(text.Text(map_name, map_font, (255, 255, 255)))

        for idx, t in enumerate(self.text_list):
            t.text_rect.center = self.button_list[idx].rect.center
        # State
        self.state = flags.MAPSELECT

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                for idx, bt in enumerate(self.button_list):
                    if bt.rect.collidepoint(pg.mouse.get_pos()):
                        self.map = 'Map-' + str(idx + 1) + '.txt'
                        if self.level == flags.LVL1:
                            self.SwitchToScene(LevelOne(self.screen, self.level, self.map))
                            bt.is_over = False
                        elif self.level == flags.LVL2:
                            self.SwitchToScene(LevelTwo(self.screen, self.level, self.map))
                            bt.is_over = False
                        elif self.level == flags.LVL3:
                            self.SwitchToScene(LevelThree(self.screen, self.level, self.map))
                            bt.is_over = False
                        elif self.level == flags.LVL4:
                            self.SwitchToScene(LevelFour(self.screen, self.level, self.map))
                            bt.is_over = False

    def Update(self, deltatime):
        ##################################################################################
        # Collisions
        for bt in self.button_list:
            bt.switch()
        ##################################################################################

    def Render(self):
        for bt in self.button_list:
            self.screen.blit(bt.image, bt.rect)
        for t in self.text_list:
            self.screen.blit(t.text, t.text_rect)


class LevelOne(SceneBase):
    def __init__(self, screen=None, level=None, map=None):
        SceneBase.__init__(self, screen)
        # Level
        self.level = level
        self.map = map
        # Handle drawing
        # Get information about the maze
        self.size, self.maze, pacmanpos = input.read_file(self.level, self.map)
        self.adjacents, foodpos = input.handle_adjacent(self.maze, self.size)
        # Resize window
        width, height = self.size
        width *= 32
        height = (height * 32) + 64
        self.screen = pg.display.set_mode((width, height))
        # Maze Drawer
        self.drawer = drawer.MazeDrawer(self.maze, self.size)
        self.background, self.background_rect = self.drawer.setup_maze()
        self.screen.blit(self.background, self.background_rect)
        # Gameplay
        self.pacman = pacman.Pacman(pacmanpos)
        self.pacman_sprite = pg.sprite.Group(self.pacman)
        self.food = food.Food(foodpos)
        self.all_sprites = pg.sprite.Group(self.food)
        self.path = find_lvl_1.A_star(self.maze, self.adjacents,
                                      self.pacman.pos, self.food.pos)

        if self.path and len(self.path) > flags.SCORE:
            self.path = None
        elif self.path and len(self.path) <= flags.SCORE:
            self.dest_node = self.path.pop(0)
        elif not self.path:
            self.dest_node = None
        self.step = 0

        self.score = 0
        self.timer = 0
        self.countdown_timer = 4
        # Objects for each state
        self.ready_flag = False
        # Score #####################
        self.food_icon = food.Food((height // 32, 0))
        self.food_icon.rect.move_ip(20, -48)
        self.all_sprites.add(self.food_icon)

        self.food_icon_censor = pg.Surface((32, 32))
        self.food_icon_censor.fill((0, 0, 0))
        self.food_icon_censor_rect = self.food_icon_censor.get_rect()
        self.food_icon_censor_rect.center = self.food_icon.rect.center
        # ###########################
        self.score_censor = pg.Surface((100, 64))
        self.score_censor.fill((0, 0, 0))
        self.score_censor_rect = self.score_censor.get_rect()
        self.score_censor_rect.left = self.food_icon.rect.right
        self.score_censor_rect.centery = self.food_icon.rect.centery

        path = os.path.join(settings.PATH, 'ASSET', 'Fonts', 'Fipps-Regular.otf')
        font = pg.font.Font(path, 20)
        self.score_text = text.Text(str(self.score), font, (33, 3, 255))
        self.score_text.text_rect.left = self.food_icon.rect.right
        self.score_text.text_rect.centery = self.food_icon.rect.centery
        self.screen.blit(self.score_text.text, self.score_text.text_rect)
        # Time  #####################
        self.time_censor = pg.Surface((100, 64))
        self.time_censor.fill((0, 0, 0))
        self.time_censor_rect = self.time_censor.get_rect()
        self.time_censor_rect.bottom = self.screen.get_rect().bottom
        self.time_censor_rect.centerx = self.screen.get_rect().centerx

        self.time_text = text.Text(str(self.countdown_timer), font, (33, 3, 255))
        self.time_text.text_rect.center = self.time_censor_rect.center
        self.screen.blit(self.time_text.text, self.time_text.text_rect)
        # State
        self.state = flags.HOLD

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self, deltatime):
        # Holding
        if self.state == flags.HOLD:
            self.countdown_timer -= deltatime
            if self.countdown_timer <= 0:
                self.ready_flag = True
                self.countdown_timer = 1.5
                self.state = flags.PLAYING
        # Playing
        elif self.state == flags.PLAYING:
            self.all_sprites.update(deltatime)
            self.countdown_timer -= deltatime
            if self.countdown_timer <= 0:
                self.ready_flag = False
                self.timer += deltatime
                if self.dest_node:
                    if self.pacman.pos == self.dest_node and self.path:
                        self.dest_node = self.path.pop(0)
                        self.step = 0
                    if self.pacman.pos != self.food.pos:
                        self.pacman.move(self.dest_node, deltatime)
                        self.pacman_sprite.update(deltatime)
                        self.step += 1
                        if self.step == 32:
                            self.pacman.pos = self.dest_node
                            self.score -= 1
                    else:
                        self.score += 20
                        self.winning_flag = True
                        self.countdown_timer = 2.5
                        self.state = flags.WINNING
                else:
                    self.surrender_flag = True
                    self.countdown_timer = 2.5
                    self.state = flags.SURRENDER
        # Winning
        elif self.state == flags.WINNING:
            self.countdown_timer -= deltatime
            if self.countdown_timer <= 0:
                self.SwitchToScene(Win(self.screen))
        # Surrender
        elif self.state == flags.SURRENDER:
            self.countdown_timer -= deltatime
            if self.countdown_timer <= 0:
                self.SwitchToScene(Surrender(self.screen))

    def Render(self):
        if self.state == flags.HOLD:
            """Status bar"""
            self.time_text.update(str(int(self.countdown_timer)))
            self.time_text.text_rect.center = self.time_censor_rect.center
            self.screen.blit(self.time_censor, self.time_censor_rect)
            #################################################################
            self.screen.blit(self.score_text.text, self.score_text.text_rect)
            self.screen.blit(self.time_text.text, self.time_text.text_rect)
            """Animation"""
            self.screen.blit(self.food_icon_censor, self.food_icon_censor_rect)
            self.screen.blit(self.background, self.food.rect, self.food.rect)
            self.all_sprites.draw(self.screen)
            self.pacman_sprite.draw(self.screen)
        elif self.state == flags.PLAYING:
            """Status bar"""
            if self.ready_flag:
                self.time_text.update('GO!')
                self.time_text.text_rect.center = self.time_censor_rect.center
                self.screen.blit(self.time_censor, self.time_censor_rect)
                #################################################################
                self.screen.blit(self.score_text.text, self.score_text.text_rect)
                self.screen.blit(self.time_text.text, self.time_text.text_rect)
            else:
                self.score_text.update(str(self.score))
                self.score_text.text_rect.left = self.food_icon.rect.right
                self.score_text.text_rect.centery = self.food_icon.rect.centery
                self.screen.blit(self.score_censor, self.score_censor_rect)
                #################################################################
                self.time_text.update(str(int(self.timer)))
                self.time_text.text_rect.center = self.time_censor_rect.center
                self.screen.blit(self.time_censor, self.time_censor_rect)
                #################################################################
                self.screen.blit(self.score_text.text, self.score_text.text_rect)
                self.screen.blit(self.time_text.text, self.time_text.text_rect)
            """Animation"""
            self.screen.blit(self.background, self.pacman.rect, self.pacman.rect)
            self.screen.blit(self.food_icon_censor, self.food_icon_censor_rect)
            self.screen.blit(self.background, self.food.rect, self.food.rect)
            self.all_sprites.draw(self.screen)
            self.pacman_sprite.draw(self.screen)
        elif self.state == flags.WINNING:
            """Status bar"""
            self.score_text.update(str(self.score))
            self.score_text.text_rect.left = self.food_icon.rect.right
            self.score_text.text_rect.centery = self.food_icon.rect.centery
            self.screen.blit(self.score_censor, self.score_censor_rect)
            #################################################################
            self.time_text.update('WIN!')
            self.time_text.text_rect.center = self.time_censor_rect.center
            self.screen.blit(self.time_censor, self.time_censor_rect)
            #################################################################
            self.screen.blit(self.score_text.text, self.score_text.text_rect)
            self.screen.blit(self.time_text.text, self.time_text.text_rect)
            """Animation"""
            self.screen.blit(self.background, self.pacman.rect, self.pacman.rect)
            self.screen.blit(self.food_icon_censor, self.food_icon_censor_rect)
            self.all_sprites.draw(self.screen)
            self.screen.blit(self.background, self.food.rect, self.food.rect)
            self.pacman_sprite.draw(self.screen)
        elif self.state == flags.SURRENDER:
            """Status bar"""
            self.score_text.update(str(self.score))
            self.score_text.text_rect.left = self.food_icon.rect.right
            self.score_text.text_rect.centery = self.food_icon.rect.centery
            self.screen.blit(self.score_censor, self.score_censor_rect)
            #################################################################
            self.time_text.update('SUR!')
            self.time_text.text_rect.center = self.time_censor_rect.center
            self.screen.blit(self.time_censor, self.time_censor_rect)
            #################################################################
            self.screen.blit(self.score_text.text, self.score_text.text_rect)
            self.screen.blit(self.time_text.text, self.time_text.text_rect)
            """Animation"""
            self.screen.blit(self.background, self.pacman.rect, self.pacman.rect)
            self.screen.blit(self.food_icon_censor, self.food_icon_censor_rect)
            self.screen.blit(self.background, self.food.rect, self.food.rect)
            self.all_sprites.draw(self.screen)
            self.pacman_sprite.draw(self.screen)


class LevelTwo(SceneBase):
    def __init__(self, screen=None, level=None, map=None):
        SceneBase.__init__(self, screen)
        # Level
        self.level = level
        self.map = map
        # Handle drawing
        # Get information about the maze
        self.size, self.maze, pacmanpos = input.read_file(self.level, self.map)
        self.adjacents, foodpos = input.handle_adjacent(self.maze, self.size)
        # Resize window
        width, height = self.size
        width *= 32
        height = (height * 32) + 64
        self.screen = pg.display.set_mode((width, height))
        # Maze Drawer
        self.drawer = drawer.MazeDrawer(self.maze, self.size)
        self.background, self.background_rect = self.drawer.setup_maze()
        self.screen.blit(self.background, self.background_rect)
        # Gameplay
        self.pacman = pacman.Pacman(pacmanpos)
        self.pacman_sprite = pg.sprite.Group(self.pacman)
        self.food = food.Food(foodpos)
        self.all_sprites = pg.sprite.Group(self.food)
        self.path = find_lvl_1.A_star(self.maze, self.adjacents,
                                      self.pacman.pos, self.food.pos)

        if len(self.path) > flags.SCORE:
            self.path = None
        if self.path:
            self.dest_node = self.path.pop(0)
        else:
            self.dest_node = None
        self.step = 0

        self.score = 0
        self.timer = 0
        self.countdown_timer = 4
        # Objects for each state
        self.ready_flag = False
        # Score #####################
        self.food_icon = food.Food((height // 32, 0))
        self.food_icon.rect.move_ip(20, -48)
        self.all_sprites.add(self.food_icon)

        self.food_icon_censor = pg.Surface((32, 32))
        self.food_icon_censor.fill((0, 0, 0))
        self.food_icon_censor_rect = self.food_icon_censor.get_rect()
        self.food_icon_censor_rect.center = self.food_icon.rect.center
        # ###########################
        self.score_censor = pg.Surface((100, 64))
        self.score_censor.fill((0, 0, 0))
        self.score_censor_rect = self.score_censor.get_rect()
        self.score_censor_rect.left = self.food_icon.rect.right
        self.score_censor_rect.centery = self.food_icon.rect.centery

        path = os.path.join(settings.PATH, 'ASSET', 'Fonts', 'Fipps-Regular.otf')
        font = pg.font.Font(path, 20)
        self.score_text = text.Text(str(self.score), font, (33, 3, 255))
        self.score_text.text_rect.left = self.food_icon.rect.right
        self.score_text.text_rect.centery = self.food_icon.rect.centery
        self.screen.blit(self.score_text.text, self.score_text.text_rect)
        # Time  #####################
        self.time_censor = pg.Surface((100, 64))
        self.time_censor.fill((0, 0, 0))
        self.time_censor_rect = self.time_censor.get_rect()
        self.time_censor_rect.bottom = self.screen.get_rect().bottom
        self.time_censor_rect.centerx = self.screen.get_rect().centerx

        self.time_text = text.Text(str(self.countdown_timer), font, (33, 3, 255))
        self.time_text.text_rect.center = self.time_censor_rect.center
        self.screen.blit(self.time_text.text, self.time_text.text_rect)
        # State
        self.state = flags.HOLD

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self, deltatime):
        # Holding
        if self.state == flags.HOLD:
            self.countdown_timer -= deltatime
            if self.countdown_timer <= 0:
                self.ready_flag = True
                self.countdown_timer = 1.5
                self.state = flags.PLAYING
        # Playing
        elif self.state == flags.PLAYING:
            self.all_sprites.update(deltatime)
            self.countdown_timer -= deltatime
            if self.countdown_timer <= 0:
                self.ready_flag = False
                self.timer += deltatime
                if self.dest_node:
                    if self.pacman.pos == self.dest_node and self.path:
                        self.dest_node = self.path.pop(0)
                        self.step = 0
                    if self.pacman.pos != self.food.pos:
                        self.pacman.move(self.dest_node, deltatime)
                        self.pacman_sprite.update(deltatime)
                        self.step += 1
                        if self.step == 32:
                            self.pacman.pos = self.dest_node
                            self.score -= 1
                    else:
                        self.score += 20
                        self.winning_flag = True
                        self.countdown_timer = 2.5
                        self.state = flags.WINNING
                else:
                    self.surrender_flag = True
                    self.countdown_timer = 2.5
                    self.state = flags.SURRENDER
        # Winning
        elif self.state == flags.WINNING:
            self.countdown_timer -= deltatime
            if self.countdown_timer <= 0:
                self.SwitchToScene(Win(self.screen))
        # Surrender
        elif self.state == flags.SURRENDER:
            self.countdown_timer -= deltatime
            if self.countdown_timer <= 0:
                self.SwitchToScene(Surrender(self.screen))

    def Render(self):
        if self.state == flags.HOLD:
            """Status bar"""
            self.time_text.update(str(int(self.countdown_timer)))
            self.time_text.text_rect.center = self.time_censor_rect.center
            self.screen.blit(self.time_censor, self.time_censor_rect)
            #################################################################
            self.screen.blit(self.score_text.text, self.score_text.text_rect)
            self.screen.blit(self.time_text.text, self.time_text.text_rect)
            """Animation"""
            self.screen.blit(self.food_icon_censor, self.food_icon_censor_rect)
            self.screen.blit(self.background, self.food.rect, self.food.rect)
            self.all_sprites.draw(self.screen)
            self.pacman_sprite.draw(self.screen)
        elif self.state == flags.PLAYING:
            """Status bar"""
            if self.ready_flag:
                self.time_text.update('GO!')
                self.time_text.text_rect.center = self.time_censor_rect.center
                self.screen.blit(self.time_censor, self.time_censor_rect)
                #################################################################
                self.screen.blit(self.score_text.text, self.score_text.text_rect)
                self.screen.blit(self.time_text.text, self.time_text.text_rect)
            else:
                self.score_text.update(str(self.score))
                self.score_text.text_rect.left = self.food_icon.rect.right
                self.score_text.text_rect.centery = self.food_icon.rect.centery
                self.screen.blit(self.score_censor, self.score_censor_rect)
                #################################################################
                self.time_text.update(str(int(self.timer)))
                self.time_text.text_rect.center = self.time_censor_rect.center
                self.screen.blit(self.time_censor, self.time_censor_rect)
                #################################################################
                self.screen.blit(self.score_text.text, self.score_text.text_rect)
                self.screen.blit(self.time_text.text, self.time_text.text_rect)
            """Animation"""
            self.screen.blit(self.background, self.pacman.rect, self.pacman.rect)
            self.screen.blit(self.food_icon_censor, self.food_icon_censor_rect)
            self.screen.blit(self.background, self.food.rect, self.food.rect)
            self.all_sprites.draw(self.screen)
            self.pacman_sprite.draw(self.screen)
        elif self.state == flags.WINNING:
            """Status bar"""
            self.score_text.update(str(self.score))
            self.score_text.text_rect.left = self.food_icon.rect.right
            self.score_text.text_rect.centery = self.food_icon.rect.centery
            self.screen.blit(self.score_censor, self.score_censor_rect)
            #################################################################
            self.time_text.update('WIN!')
            self.time_text.text_rect.center = self.time_censor_rect.center
            self.screen.blit(self.time_censor, self.time_censor_rect)
            #################################################################
            self.screen.blit(self.score_text.text, self.score_text.text_rect)
            self.screen.blit(self.time_text.text, self.time_text.text_rect)
            """Animation"""
            self.screen.blit(self.background, self.pacman.rect, self.pacman.rect)
            self.screen.blit(self.food_icon_censor, self.food_icon_censor_rect)
            self.all_sprites.draw(self.screen)
            self.screen.blit(self.background, self.food.rect, self.food.rect)
            self.pacman_sprite.draw(self.screen)
        elif self.state == flags.SURRENDER:
            """Status bar"""
            self.score_text.update(str(self.score))
            self.score_text.text_rect.left = self.food_icon.rect.right
            self.score_text.text_rect.centery = self.food_icon.rect.centery
            self.screen.blit(self.score_censor, self.score_censor_rect)
            #################################################################
            self.time_text.update('SUR!')
            self.time_text.text_rect.center = self.time_censor_rect.center
            self.screen.blit(self.time_censor, self.time_censor_rect)
            #################################################################
            self.screen.blit(self.score_text.text, self.score_text.text_rect)
            self.screen.blit(self.time_text.text, self.time_text.text_rect)
            """Animation"""
            self.screen.blit(self.background, self.pacman.rect, self.pacman.rect)
            self.screen.blit(self.food_icon_censor, self.food_icon_censor_rect)
            self.screen.blit(self.background, self.food.rect, self.food.rect)
            self.all_sprites.draw(self.screen)
            self.pacman_sprite.draw(self.screen)


class LevelThree(SceneBase):
    def __init__(self, screen=None, level=None, map=None):
        SceneBase.__init__(self, screen)

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self, deltatime):
        pass

    def Render(self):
        # The game scene is just a blank blue screen
        self.screen.fill((0, 0, 255))


class LevelFour(SceneBase):
    def __init__(self, screen=None, level=None, map=None):
        SceneBase.__init__(self, screen)

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self, deltatime):
        pass

    def Render(self):
        # The game scene is just a blank blue screen
        self.screen.fill((0, 0, 255))


class Win(SceneBase):
    def __init__(self, screen=None):
        SceneBase.__init__(self, screen)

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self, deltatime):
        pass

    def Render(self):
        # The game scene is just a blank blue screen
        self.screen.fill((0, 0, 255))


class GameOver(SceneBase):
    def __init__(self, screen=None):
        SceneBase.__init__(self, screen)

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self, deltatime):
        pass

    def Render(self):
        # The game scene is just a blank blue screen
        self.screen.fill((0, 0, 255))


class Surrender(SceneBase):
    def __init__(self, screen=None):
        SceneBase.__init__(self, screen)

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self, deltatime):
        pass

    def Render(self):
        # The game scene is just a blank blue screen
        self.screen.fill((0, 0, 255))
