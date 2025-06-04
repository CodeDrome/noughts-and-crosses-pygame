from typing import Tuple, NamedTuple

from collections import namedtuple

import pygame

import nac


UIrect = namedtuple("UIrect", "x, y, w, h, func")


class NaCPyGame(object):

    def __init__(self):

        pygame.init()
        pygame.display.set_caption("CodeDrome NaC")
        self.win = pygame.display.set_mode((600,800))

        self.run = True
        self.graphics = self.__init_graphics()
        self.uirects = self.__init_rects()
        self.clock = pygame.time.Clock()

        self.game = nac.NaC(on_change=self.on_game_changed,
                            on_game_over=self.on_game_over)

        self.__draw_game_window()

        self.__event_loop()


    def on_game_changed(self, column:int, row:int, shape:str):

        self.__draw_game_window()

   
    def on_game_over(self, winner:str):

        self.__draw_game_window()


    def __init_graphics(self) -> None:

        '''
        Creates a dictionary of all the 
        images used by the game.
        '''

        graphics = {"background": pygame.image.load('graphics/blackboard_600x800.jpg'),
                    "grid": pygame.image.load('graphics/grid.png'),
                    "nought": pygame.image.load('graphics/nought.png'),
                    "cross": pygame.image.load('graphics/cross.png'),
                    "levels": pygame.image.load('graphics/levels.png'),
                    "radio_on": pygame.image.load('graphics/radio_on.png'),
                    "start": pygame.image.load('graphics/start.png'),
                    "new": pygame.image.load('graphics/new.png'),
                    "youwon": pygame.image.load('graphics/youwon.png'),
                    "youlost": pygame.image.load('graphics/youlost.png'),
                    "nowinner": pygame.image.load('graphics/nowinner.png')}

        return graphics


    def __init_rects(self) -> None:

        """
        Top left coordinates, size and function
        for each area we wish to handle mouse clicks for
        """

        rects = [UIrect(0,   0,   200, 200, lambda: self.game.human_move(1)), 
                 UIrect(200, 0,   200, 200, lambda: self.game.human_move(2)),
                 UIrect(400, 0,   200, 200, lambda: self.game.human_move(3)),
                 UIrect(0,   200, 200, 200, lambda: self.game.human_move(4)),
                 UIrect(200, 200, 200, 200, lambda: self.game.human_move(5)),
                 UIrect(400, 200, 200, 200, lambda: self.game.human_move(6)),
                 UIrect(0,   400, 200, 200, lambda: self.game.human_move(7)),
                 UIrect(200, 400, 200, 200, lambda: self.game.human_move(8)),
                 UIrect(400, 400, 200, 200, lambda: self.game.human_move(9)),

                 UIrect(28,  612, 246, 76,  lambda: self.game.new_game()),

                 UIrect(28,  710, 246, 76,  lambda: self.game.computer_move()),

                 UIrect(322, 616, 44,  44,  lambda: self.__level_changed(nac.NaC.Levels.IDIOT)),

                 UIrect(322, 682, 44,  44,  lambda: self.__level_changed(nac.NaC.Levels.AVERAGE)),

                 UIrect(322, 744, 44,  44,  lambda: self.__level_changed(nac.NaC.Levels.GENIUS))]

        return rects


    def __point_in_rect(self, pos:Tuple, rect:NamedTuple) -> None:

        """
        Check whether a coordinate is within a rectangle
        """

        x2 = rect.x + rect.w
        y2 = rect.y +rect.h

        in_rect = (rect.x <= pos[0] < x2 and
                   rect.y <= pos[1] < y2)

        return in_rect


    def __click_to_func(self, pos:Tuple) -> None:

        """
        Iterates rectangles and calls corresponding function
        for any which have been clicked
        """

        for rect in self.uirects:

            if(self.__point_in_rect(pos, rect)):

                rect.func()


    def __handle_left_mousebuttondown(self, pos:Tuple) -> None:

        self.__click_to_func(pos)


    def __level_changed(self, new_level):

        self.game.level = new_level

        self.__draw_game_window()


    def __draw_game_window(self) -> None:

        '''
        Draws the entire window after each change.
        For faster and more action-packed games
        there are ways to streamline this process.
        '''

        self.win.blit(self.graphics["background"], (0,0))
        self.win.blit(self.graphics["grid"], (0,0))
        self.win.blit(self.graphics["levels"], (300,600))

        if self.game.level == nac.NaC.Levels.IDIOT:
            self.win.blit(self.graphics["radio_on"], (330,622))
        elif self.game.level == nac.NaC.Levels.AVERAGE:
            self.win.blit(self.graphics["radio_on"], (332,686))
        else: # "genius"
            self.win.blit(self.graphics["radio_on"], (334,748))

        self.win.blit(self.graphics["start"], (0,700))
        self.win.blit(self.graphics["new"], (0,600))

        x = 0
        y = 0
        for row in range(0,3):
            for column in range(0,3):
                if self.game._squares[row][column] == "X":
                    self.win.blit(self.graphics["cross"], (x,y))
                elif self.game._squares[row][column] == "O":
                    self.win.blit(self.graphics["nought"], (x,y))
                x += 200
            y += 200
            x = 0

        if self.game.winner == " ":
            self.win.blit(self.graphics["nowinner"], (0,100))
        elif self.game.winner == "X":
            self.win.blit(self.graphics["youwon"], (0,100))
        elif self.game.winner == "O":
            self.win.blit(self.graphics["youlost"], (0,100))
        
        pygame.display.update()


    def __event_loop(self) -> None:

        """
        Checks event queue every 50ms
        for QUIT or left MOUSEBUTTONDOWN
        """

        while self.run:

            self.clock.tick(50)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    self.run = False
                    pygame.quit()
                    break

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 1:

                        self.__handle_left_mousebuttondown(event.pos)


game = NaCPyGame()