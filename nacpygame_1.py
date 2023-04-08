from collections import namedtuple

import pygame


UIrect = namedtuple("UIrect", "x, y, w, h, func")


class NaCUI(object):

    def __init__(self):

        pygame.init()
        pygame.display.set_caption("CodeDrome NaC")

        self.win = pygame.display.set_mode((600,800))
        self.run = True
        self.graphics = self.__init_graphics()
        self.uirects = self.__init_rects()
        self.clock = pygame.time.Clock()        
        self.level = "average" # temporary variable

        self.__draw_game_window()

        self.__event_loop()


    def __init_graphics(self):

        graphics = {"background": pygame.image.load('graphics/blackboard_600x800.jpg'),
                    "grid": pygame.image.load('graphics/grid.png'),
                    "nought": pygame.image.load('graphics/nought.png'),
                    "cross": pygame.image.load('graphics/cross.png'),
                    "levels": pygame.image.load('graphics/levels.png'),
                    "radio_on": pygame.image.load('graphics/radio_on.png'),
                    "start": pygame.image.load('graphics/start.png'),
                    "new": pygame.image.load('graphics/new.png')}

        return graphics


    def __init_rects(self):

        """
        Top left coordinates, size and function
        for each area we wish to handle mouse clicks for
        """

        rects = [UIrect(0,   0,   200, 200, lambda: print("1")), 
                 UIrect(200, 0,   200, 200, lambda: print("2")),
                 UIrect(400, 0,   200, 200, lambda: print("3")),
                 UIrect(0,   200, 200, 200, lambda: print("4")),
                 UIrect(200, 200, 200, 200, lambda: print("5")),
                 UIrect(400, 200, 200, 200, lambda: print("6")),
                 UIrect(0,   400, 200, 200, lambda: print("7")),
                 UIrect(200, 400, 200, 200, lambda: print("8")),
                 UIrect(400, 400, 200, 200, lambda: print("9")),
                 UIrect(28,  612, 246, 76,  lambda: print("new")),
                 UIrect(28,  710, 246, 76,  lambda: print("start")),
                 UIrect(322, 616, 44,  44,  lambda: self.__level_changed("idiot")),
                 UIrect(322, 682, 44,  44,  lambda: self.__level_changed("average")),
                 UIrect(322, 744, 44,  44,  lambda: self.__level_changed("genius"))]

        return rects


    def __point_in_rect(self, pos, rect):

        """
        Check whether a coordinate is within a rectangle
        """

        x2 = rect.x + rect.w
        y2 = rect.y +rect.h

        in_rect = (rect.x <= pos[0] < x2 and
                   rect.y <= pos[1] < y2)

        return in_rect


    def __click_to_func(self, pos):

        """
        Iterates rectangles and calls corresponding function
        for any which have been clicked
        """

        for rect in self.uirects:

            if(self.__point_in_rect(pos, rect)):

                rect.func()


    def __handle_left_mousebuttondown(self, pos):

        self.__click_to_func(pos)


    def __level_changed(self, new_level):

        self.level = new_level

        self.__draw_game_window()


    def __draw_game_window(self):

        self.win.blit(self.graphics["background"], (0,0))
        self.win.blit(self.graphics["grid"], (0,0))
        self.win.blit(self.graphics["levels"], (300,600))

        if self.level == "idiot":
            self.win.blit(self.graphics["radio_on"], (330,622))
        elif self.level == "average":
            self.win.blit(self.graphics["radio_on"], (332,686))
        else: # "genius"
            self.win.blit(self.graphics["radio_on"], (334,748))

        self.win.blit(self.graphics["start"], (0,700))
        self.win.blit(self.graphics["new"], (0,600))

        # these 2 lines are not part of the final game
        # and are just here to demo the nought and cross graphics
        self.win.blit(self.graphics["nought"], (200,0))
        self.win.blit(self.graphics["cross"], (400,400))

        pygame.display.update()


    def __event_loop(self):

        """
        Checks event queue every 50ms
        for QUIT or MOUSEBUTTONDOWN
        """

        while self.run:

            self.clock.tick(50)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    self.run = False
                    pygame.quit()

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 1:
                        self.__handle_left_mousebuttondown(event.pos)
            
                        self.__draw_game_window()


game = NaCUI()