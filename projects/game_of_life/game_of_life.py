import os
import json
import random
import pygame as pg


with open("config.json") as file:
    config = json.load(file)
BACKGROUND_COLOR = pg.Color(config["background_color"])
VISITED_COLOR = [min(chan+20, 255) for chan in BACKGROUND_COLOR]


# Configirung random interresting initial shapes

heart = [[42, 20], [43, 20], [44, 20], [45, 20], [46, 20], [47, 20], [48, 20], [49, 20], [50, 20], [51, 20], [52, 20], [53, 
20], [54, 20], [55, 20], [56, 20], [43, 21], [44, 21], [45, 21], [46, 21], [47, 21], [48, 21], [49, 21], [50, 21], [51, 21], [52, 21], [53, 21], [54, 21], [55, 21], [44, 22], [45, 22], [46, 22], [47, 22], [48, 22], [49, 22], [50, 22], [51, 22], [52, 22], [53, 22], [54, 22], [45, 23], [46, 23], [47, 23], [48, 23], [49, 23], [50, 23], [51, 23], [52, 23], [53, 23], [46, 24], [47, 24], [48, 24], [49, 24], [50, 24], [51, 24], [52, 24], [47, 25], [48, 25], [49, 25], [50, 25], [51, 25], [48, 26], [49, 26], [50, 26], [43, 19], [44, 19], [45, 19], [46, 19], [47, 19], [43, 18], [44, 
18], [45, 18], [46, 18], [44, 17], [45, 17], [46, 17], [46, 16], [45, 16], [46, 16], [47, 17], [47, 18], [48, 18], [48, 19], [50, 19], [51, 19], [52, 19], [53, 19], [54, 19], [50, 18], [51, 18], [52, 18], [53, 18], [51, 17], [52, 17], [53, 17], [53, 16], [52, 16], [53, 16], [54, 17], [54, 18], [55, 18], [55, 19], [49, 19], [49, 27],
[42, 28], [43, 27], [44, 26],[45, 25], [54, 16], [55, 15], [56, 14], [57, 13], [58, 12], [58,13], [58,14], [57, 12], [56, 12],[55, 12],[54, 13], [58, 14], [58, 15], [57, 16]
]

usb = [[54, 20], [54, 21],[54, 22], [54, 23], [54, 24], [54, 25], [53, 26], [52, 27], [51, 27], [50, 27], [49, 26], [48, 25], [48, 24], [48, 23], [48, 22], [48, 21], [48, 20], [49, 20], [50, 20], [51, 20], [52, 20], [53, 20], [49, 19], [50, 19], [51, 19], [52, 19], [53, 19],
    [53, 18], [53, 17], [53, 16],[53, 15], [49, 18], [49, 17], [49, 16], [49, 15], [50, 15], [51, 15], [52, 15], [50, 17], [52, 17]
    ]
default = [[40,30],
        [40,31],
        [41,30],
        [41,29],
        [42,30]]

Initial_shapes = [default, heart, usb]

config["initial_config"] = random.choice(Initial_shapes)

class Game:

    def __init__(self, max_width, max_height):
        self.cells = {}
        for value in config["initial_config"]:
            coord = tuple(value)
            self.cells[coord] = Cell(coord)

        self.max_width = max_width
        self.max_height = max_height
        print(max_width, self.max_height )
        print(self.cells)

    def reset(self):
        self.cells = {}

    def __setitem__(self, coord, value):
        self.cells[coord] = value

    def __delitem__(self, coord):
        del self.cells[coord]

    def next_generation(self):
        """ method that build the next generation of the game"""
        new_generation = {}
        for i in range(-10, self.max_width+10):
            for j in range(-10, self.max_height+10):
                # first we need all the cell neighbors
                neighboring_cells = self.__neighbors((i,j))
                # we then need to select the active ones
                alive_cells = {}
                for adjacent_cell in neighboring_cells:
                    if adjacent_cell in self.cells:
                        alive_cells[adjacent_cell] = Cell(adjacent_cell)
                # we check if our cell is dead or alive
                if (i,j) in self.cells:
                    # if it's alive then we'll keep it alive if there 2 or 3
                    # neighbor's alive
                    if len(alive_cells) == 3 or len(alive_cells) == 2:
                        new_generation[(i,j)] = Cell((i,j))
                else:
                    # if it's not then we'll make it alive if there is exectly 3
                    # neighbor's alive
                    if len(alive_cells) == 3:
                        new_generation[(i,j)] = Cell((i,j))
        self.cells = new_generation



    def __neighbors(self, cell):
        """ method that retun the list of neighbors of a cell"""
        return {
                (cell[0]-1, cell[1]-1), (cell[0]-1, cell[1]), (cell[0]-1, cell[1]+1),
                (cell[0], cell[1]-1), (cell[0], cell[1]+1),
                (cell[0]+1, cell[1]-1), (cell[0]+1, cell[1]), (cell[0]+1, cell[1]+1),
        }


class Cell:
    size = (config["cell_size_width"], config["cell_size_height"])

    def __init__(self, coords):
        self.color = pg.Color(config["cell_color"])
        self.rect = pg.Rect((coords[0]*Cell.size[0],coords[1]*Cell.size[1]),
                            Cell.size)
        self.rect.inflate_ip(-2, -2)
        self.age = 0

    def draw(self, surface, background):
        color = [min(chan+self.age, 255) for chan in self.color]
        surface.fill(color, self.rect)
        background.fill(VISITED_COLOR, self.rect)


class App:
    """
    Manages control flow for entire program.
    """

    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.background = pg.Surface(self.screen_rect.size).convert()
        self.background.fill(BACKGROUND_COLOR)
        self.fps = 30
        self.clock = pg.time.Clock()
        self.done = False
        self.cell_w = self.screen_rect.w//Cell.size[0]
        self.cell_h = self.screen_rect.h//Cell.size[1]
        self.game = Game(self.cell_w, self.cell_h)
        self.wrapping = True
        self.generating = False

    def reset(self):
        self.game.reset()
        self.background.fill(BACKGROUND_COLOR)

    def event_loop(self):
        """
        Start and stop generation by pressing spacebar.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.generating = not self.generating
                elif event.key == pg.K_BACKSPACE:
                    self.reset()

    def add_delete(self, mouse):
        mouse_pos = pg.mouse.get_pos()
        coords = mouse_pos[0]//Cell.size[0], mouse_pos[1]//Cell.size[1]
        if mouse[0]:
            self.game[coords] = Cell(coords)
        elif mouse[2]:
            try:
                del (self.game[coords])
            except KeyError:
                pass

    def update(self):
        """
        If generating is True, calculate the next generation of living cells.
        """
        mouse = pg.mouse.get_pressed()
        if any(mouse):
            self.add_delete(mouse)
        elif self.generating:
            self.game.next_generation()

    def render(self):
        """
        Clear the screen and render all living cells.
        """
        self.screen.blit(self.background, (0,0))
        for coord, cell in self.game.cells.items():
            cell.draw(self.screen, self.background)
        pg.display.update()

    def main_loop(self):
        """
        Spin.
        """
        while not self.done:
            self.event_loop()
            self.update()
            self.render()
            self.clock.tick(self.fps)

def main():
    """
    Set up our environment; create an App instance; and start our main loop.
    """
    os.environ["SDL_VIDEO_CENTERED"] = "True"
    screen_size = (config["screen_size_width"], config["screen_size_height"])
    pg.init()
    pg.display.set_caption("Game of life")
    pg.display.set_mode(screen_size)
    App().main_loop()
    pg.quit()


if __name__ == "__main__":
    main()