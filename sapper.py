from tkinter import Tk, Canvas
from typing import List
from random import sample


class Cell:
    def __init__(self, x0, y0, x1, y1, color, canvas: Canvas):
        self.canvas: Canvas = canvas
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.id = self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)
        self.showed = False

        self.num = 0
        self.num_obj = None

        self.bomb = False
        self.bomb_pict = None

        self.flag = False
        self.flag_id = (0, 0)

    def create_bomb(self):
        self.bomb_pict = self.canvas.create_oval(self.x0 + 2, self.y0 + 2, self.x1 - 2, self.y1 - 2, fill='black')

    def create_num(self):
        colors = {0: 'darkblue', 1: 'blue', 2: 'green', 3: 'red', 4: 'purple',
                  5: 'lightcoral', 6: 'peru', 7: 'orange', 8: 'cyan'}
        self.num_obj = self.canvas.create_text((self.x0 + self.x1) / 2, (self.y0 + self.y1) / 2, text=str(self.num),
                                               fill=colors[self.num], font='Verdana 20')
        self.showed = True


class MyButton:
    def __init__(self, canvas, coords: tuple):
        self.canvas: Canvas = canvas
        self.id = canvas.create_rectangle(*coords, fill='pink', outline='darkred', width=5)
        create_flag(canvas, *coords)

        self.is_pressed = False

    def press(self):
        if self.is_pressed is False:
            self.canvas.itemconfig(self.id, outline='green')
            self.is_pressed = True
        else:
            self.canvas.itemconfig(self.id, outline='darkred')
            self.is_pressed = False


class Sapper:
    def __init__(self, canvas, matrix):
        self.canvas: Canvas = canvas
        self.matrix: List[List[Cell]] = matrix

    def move(self, x, y):
        if self.matrix[y][x].showed:
            return
        if self.matrix[y][x].bomb is True:
            self.matrix[y][x].create_bomb()
            return 'stop'

        self.matrix[y][x].create_num()

        if self.matrix[y][x].num == 0:
            for (y, x) in [(y - 1, x - 1), (y - 1, x), (y - 1, x + 1),
                           (y, x - 1), (y, x + 1),
                           (y + 1, x - 1), (y + 1, x), (y + 1, x + 1)]:
                if 0 <= x < len(self.matrix) and 0 <= y < len(self.matrix):
                    if self.matrix[y][x].showed is self.matrix[y][x].bomb is False:
                        self.move(x, y)

    def add_flag(self, x, y, w):
        self.matrix[y][x].flag = True
        self.matrix[y][x].flag_id = create_flag(self.canvas, w * (x + 1), w * (y + 3), w * (x + 2), w * (y + 4))


class Window:
    def __init__(self, name='sapper', side=15, w=40):
        self.tk = Tk()
        self.tk.title(name)
        self.tk.geometry(f'{w * (side + 2)}x{w * (side + 4)}')
        self.tk.resizable(False, False)

        self.canvas: Canvas = Canvas(self.tk, width=w * (side + 2), height=w * (side + 4), bg='lemonchiffon')
        self.canvas.pack()

        self.side = side
        self.w = w

        self.bombs_left = 20
        self.bombs_left_text = self.canvas.create_text(3 * w, w, fill='grey', anchor='nw', font='Verdana 40',
                                                       text=f'Bombs left: {self.bombs_left}')

        self.field: List[List[Cell]] = self.create_field(side)
        self.place_bombs()

        self.sapper = Sapper(self.canvas, self.field)

        self.my_button = MyButton(self.canvas, (w, w, 2 * w, 2 * w))

    def create_field(self, side) -> List[List[Cell]]:
        array = []
        for i in range(side):
            array.append([])
            for j in range(side):
                array[i].append(Cell(self.w + j * self.w,
                                     3 * self.w + i * self.w,
                                     self.w + (j + 1) * self.w,
                                     3 * self.w + (i + 1) * self.w,
                                     'whitesmoke', self.canvas))
        return array

    def place_bombs(self, bombs_count=20):
        bombs: List[List[int, int]] = sample([[i, j] for i in range(self.side) for j in range(self.side)], bombs_count)

        for bomb in bombs:
            self.field[bomb[0]][bomb[1]].bomb = True

        for bomb in bombs:
            for (x, y) in [(bomb[0] - 1, bomb[1] - 1), (bomb[0] - 1, bomb[1]), (bomb[0] - 1, bomb[1] + 1),
                           (bomb[0], bomb[1] - 1), (bomb[0], bomb[1] + 1),
                           (bomb[0] + 1, bomb[1] - 1), (bomb[0] + 1, bomb[1]), (bomb[0] + 1, bomb[1] + 1)]:
                if 0 <= x < self.side and 0 <= y < self.side and self.field[x][y].bomb is False:
                    self.field[x][y].num += 1

    def win_check(self):
        for y in range(self.side):
            for x in range(self.side):
                if self.field[y][x].showed is self.field[y][x].bomb is False:
                    return False
        return True

    def click(self, x, y):
        if self.w <= x <= 2 * self.w and self.w <= y <= 2 * self.w:
            self.my_button.press()
        elif self.w <= x <= (self.side + 1) * self.w and 3 * self.w <= y <= (self.side + 3) * self.w:
            x, y = (x - self.w) // self.w, (y - 3 * self.w) // self.w
            if self.field[y][x].showed is False:
                if self.my_button.is_pressed:
                    if self.field[y][x].flag is True:
                        self.field[y][x].flag = False
                        self.canvas.delete(self.field[y][x].flag_id[0])
                        self.canvas.delete(self.field[y][x].flag_id[1])
                        self.bombs_left += 1
                        self.canvas.itemconfig(self.bombs_left_text, text=f'Bombs left: {self.bombs_left}')
                    elif self.bombs_left > 0:
                        self.sapper.add_flag(x, y, self.w)
                        self.bombs_left -= 1
                        self.canvas.itemconfig(self.bombs_left_text, text=f'Bombs left: {self.bombs_left}')
                else:
                    self.sapper.move(x, y)
                    if self.field[y][x].bomb is True:
                        self.canvas.itemconfig(self.field[y][x].id, fill='red')
                        self.canvas.config(bg='red')
                        self.canvas.itemconfig(self.bombs_left_text, text='YOU LOST', anchor='nw', font='Verdana 60')
                        self.click = lambda *inp: inp
                    elif self.win_check():
                        self.canvas.config(bg='lawngreen')
                        self.canvas.itemconfig(self.bombs_left_text, text='YOU WON', anchor='nw', font='Verdana 60')
                        self.click = lambda *inp: inp


def create_flag(canvas: Canvas, x0, y0, x1, y1):
    line = canvas.create_line(x0 + (x1 - x0) * 0.4, y0 + (y1 - y0) * 0.1,
                              x0 + (x1 - x0) * 0.4, y0 + (y1 - y0) * 0.9,
                              width=5)
    triangle = canvas.create_polygon(x0 + (x1 - x0) * 0.45, y0 + (y1 - y0) * 0.2,
                                     x0 + (x1 - x0) * 0.45, y0 + (y1 - y0) * 0.6,
                                     x0 + (x1 - x0) * 0.8, y0 + (y1 - y0) * 0.4,
                                     fill='lightgreen', outline='lightgreen')
    return line, triangle


window = Window()
window.tk.bind("<Button-1>", lambda event: window.click(event.x, event.y))
window.tk.bind("<E>", lambda event: window.tk.destroy())

window.tk.mainloop()
