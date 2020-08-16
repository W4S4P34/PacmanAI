import handle_input as input
import game_flags as flags
import game_settings as settings
import scene
import pygame as pg


class Game:
    def __init__(self):
        # Game objects
        """Screen, title and icon"""
        self.screen = pg.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.title = pg.display.set_caption('Pacman - We will survive!')
        pacmanicon, _ = input.load_image(flags.MISC_TYPE, flags.ICO)
        self.icon = pg.display.set_icon(pacmanicon)
        """Clock to manage FPS of the game"""
        self.clock = pg.time.Clock()
        self.deltatime = 0
        """Scenes"""
        self.current_scene = scene.TitleScene(self.screen)

    def on_execute(self, fps):
        pg.init()

        while self.current_scene is not None:
            pressed_keys = pg.key.get_pressed()
            # Event filtering
            filtered_events = []

            for event in pg.event.get():
                quit_attempt = False
                if event.type == pg.QUIT:
                    quit_attempt = True
                elif event.type == pg.KEYDOWN:
                    alt_pressed = pressed_keys[pg.K_LALT] or pressed_keys[pg.K_RALT]
                    if event.key == pg.K_ESCAPE:
                        quit_attempt = True
                    elif event.key == pg.K_F4 and alt_pressed:
                        quit_attempt = True

                if quit_attempt:
                    self.current_scene.Terminate()
                else:
                    filtered_events.append(event)

            self.current_scene.ProcessInput(filtered_events, pressed_keys)
            if self.current_scene == self.current_scene.next:
                self.current_scene.Update(self.deltatime)
            if self.current_scene == self.current_scene.next:
                self.current_scene.Render()
            else:
                self.current_scene = self.current_scene.next

            pg.display.flip()
            self.deltatime = self.clock.tick(60) / 1000


###################################################################
if __name__ == '__main__':
    maingame = Game()
    maingame.on_execute(60)
