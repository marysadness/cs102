import pathlib
import random
import copy

from typing import List, Optional, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:
    
    def __init__(
        self,
        size: Tuple[int, int],
        randomize: bool=True,
        max_generations: Optional[float]=float('inf')
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size[0], size[1]
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool=False):
        # Copy from previous assignment
        self.curr_generation = []
        for i in range(self.rows):
            b = []
            for j in range(self.cols):
                if not randomize:
                    b += [0]
                else:
                    b += [random.randint(0, 1)]
            self.curr_generation += [b]
        return self.curr_generation

    def get_neighbours(self, cell: Cell):
        # Copy from previous assignment
        neighbours = []
        neighbours1 = []
        neighbours1 += [[cell[0], cell[1] + 1]] + [[cell[0] + 1, cell[1] + 1]] + [[cell[0] + 1, cell[1]]]
        neighbours1 += [[cell[0], cell[1] - 1]] + [[cell[0] - 1, cell[1] - 1]] + [[cell[0] - 1, cell[1]]]
        neighbours1 += [[cell[0] - 1, cell[1] + 1]] + [[cell[0] + 1, cell[1] - 1]]
        for i in range(8):
            if neighbours1[i][0] >= 0 and neighbours1[i][0] < self.rows and neighbours1[i][1] >= 0 and neighbours1[i][1] < self.cols:
                a = int(neighbours1[i][0])
                b = int(neighbours1[i][1])
                neighbours.append(self.curr_generation[a][b])
        return neighbours

    def get_next_generation(self):
        # Copy from previous assignment
        new_grid = copy.deepcopy(self.curr_generation)
        for i in range(self.rows):
            for j in range(self.cols):
                f = [i, j]
                l = sum(self.get_neighbours(f))
                if new_grid[i][j] == 0:
                    if l == 3:
                        new_grid[i][j] = 1
                elif l == 3 or l == 2:
                    new_grid[i][j] = 1
                else:
                    new_grid[i][j] = 0
        return new_grid

    def step(self):
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = copy.deepcopy(self.curr_generation)
        # Текущее поколение клеток
        self.curr_generation = self.get_next_generation()
        self.generations += 1


    @property
    def is_max_generations_exceeded(self):
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations >= self.max_generations


    @property
    def is_changing(self):
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation



    @staticmethod
    def from_file(filename: pathlib.Path):
        """
        Прочитать состояние клеток из указанного файла.
        """
        f = open(filename)
        grid = []
        row = []
        h = 0
        for line in f:
            row = [int(i) for i in line if i in '01']
            grid.append(row)
            h += 1
        w = len(row)
        game = GameOfLife((h, w), False)
        game.prev_generation = GameOfLife.create_grid(game)
        game.curr_generation = grid
        f.close()
        return game

    def save(self, filename: pathlib.Path):
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        f = open(filename, 'r+')
        f.truncate()
        for i in range(len(self.curr_generation)):
            d = ''.join(map(str, self.curr_generation[i]))
            f.write(d)
            if i != len(self.curr_generation) - 1:
                f.write('\n')
        f.close()

if __name__ == '__main__':
    game = GameOfLife()
    game.run()
