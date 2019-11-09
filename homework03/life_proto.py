
import random
import pygame

from pygame.locals import *
from typing import List, Tuple


class GameOfLife:

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed


    def draw_lines(self) -> None:
        # @see: http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))


    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.draw_lines()
            self.create_grid()
            self.draw_grid()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False):
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        self.a = []
        for i in range(self.cell_width):
            b = []
            for j in range(self.cell_height):
                if randomize == False:
                    b += [0]
                else:
                    b += [random.randint(0, 1)]
            self.a += [b]

        return self.a

    def draw_grid(self):
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.

        """
        for i in range(self.cell_width):
            for j in range(self.cell_height):
                if self.a[i][j] == 0:
                    pygame.draw.rect(self.screen, pygame.Color('white'), ((self.cell_size * i ),(self.cell_size * j), self.cell_size,self.cell_size ))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('green'), ((self.cell_size * i ), (self.cell_size * j), self.cell_size,self.cell_size ))
        self.draw_lines()

    def get_neighbours(self, cell):
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        neighbours = []
        neighbours1 = []
        neighbours1 += [[cell[0], cell[1] + 1]] + [[cell[0] + 1, cell[1] + 1]] + [[cell[0] + 1, cell[1]]]
        neighbours1 += [[cell[0], cell[1] - 1]] + [[cell[0] - 1, cell[1] - 1]] + [[cell[0] - 1, cell[1]]]
        neighbours1 += [[cell[0] - 1, cell[1] + 1]] + [[cell[0] + 1, cell[1] - 1]]
        for i in range(8):
            if neighbours1[i][0] >= 1 and neighbours1[i][0] < self.rows and neighbours1[i][1] >= 1 and neighbours1[i][1] < self.cols:
                a = neighbours1[i][0]
                b = neighbours1[i][1]
                if self.curr_generation[a][b] == 1:
                    neighbours += [neighbours1[i]]

        return neighbours

    def get_next_generation(self) :
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        for i in range(len(self.curr_generation)):
            for j in range(len(self.curr_generation[i])):
                f = (i, j)
                if self.curr_generation[i][j] == 0:
                    if len(self.get_neighbours(f)) == 3:
                        self.curr_generation[i][j] = 1
                elif len(self.get_neighbours(f)) == 3 or len(self.get_neighbours(f)) == 2:
                    self.curr_generation[i][j] = 1
                else:
                    self.curr_generation[i][j] = 0
        return self.curr_generation

if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
    game.run()