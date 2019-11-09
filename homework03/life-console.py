import curses

from life import GameOfLife
from ui import UI


class Console(UI):

    def __init__(self, life: GameOfLife):
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.addstr(0, 0, "+")
        screen.addstr(0, self.life.cols + 1, "+")
        screen.addstr(self.life.rows + 1, 0, "+")
        screen.addstr(self.life.rows + 1, self.life.cols + 1, "+")
        for i in range(1, self.life.cols + 1):
            screen.addstr(0, i, "-")
        for i in range(1, self.life.cols + 1):
            screen.addstr(self.life.rows + 1, i, "-")
        for i in range(1, self.life.rows + 1):
            screen.addstr(i, 0, "|")
        for i in range(1, self.life.rows + 1):
            screen.addstr(i, self.life.cols + 1, "|")




    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 0:
                    screen.addstr(i + 1, j + 1, " ")
                else:
                    screen.addstr(i + 1, j + 1, "*")

    def run(self) -> None:
        screen = curses.initscr()
        screen.clear()
        self.draw_borders(screen)
        screen.refresh()
        while not self.life.is_max_generations_exceeded and self.life.is_changing:
            self.draw_grid(screen)
            screen.refresh()
            self.life.step()
        curses.endwin()
if __name__ == '__main__':
    life = GameOfLife((24, 80), max_generations=50)

    ui = Console(life)
    ui.run()
