from tkinter import Tk, Canvas
from time import sleep


class TicTacToe:
    def __init__(self, canvas):
        self.canvas: Canvas = canvas
        self.turn = -1
        self.matrix = [['?', '?', '?'],
                       ['?', '?', '?'],
                       ['?', '?', '?']]
        self.is_moving = False
        self.end = False

    def move(self, x, y):
        if self.is_moving:
            return
        self.is_moving = True
        if not self.end and 100 < x < 400 and 100 < y < 400:
            x = (x - 100) // 100
            y = (y - 100) // 100
            if self.matrix[y][x] == '?':
                self.turn = (self.turn + 1) % 2
                if self.turn == 0:
                    self.cross_move(x, y)
                else:
                    self.oval_move(x, y)
        self.is_moving = False

    def cross_move(self, x, y):
        self.matrix[y][x] = 'x'
        self.create_cross(x, y)
        if self.matrix[y][0] == self.matrix[y][1] == self.matrix[y][2]:
            self.win('x', 'g', x, y)
        elif self.matrix[0][x] == self.matrix[1][x] == self.matrix[2][x]:
            self.win('x', 'v', x, y)
        elif self.matrix[0][0] == self.matrix[1][1] == self.matrix[2][2] == 'x':
            self.win('x', 'd1', x, y)
        elif self.matrix[0][2] == self.matrix[1][1] == self.matrix[2][0] == 'x':
            self.win('x', 'd2', x, y)

    def oval_move(self, x, y):
        self.matrix[y][x] = 'o'
        self.create_oval(x, y)
        if self.matrix[y][0] == self.matrix[y][1] == self.matrix[y][2]:
            self.win('o', 'g', x, y)
        elif self.matrix[0][x] == self.matrix[1][x] == self.matrix[2][x]:
            self.win('o', 'v', x, y)
        elif self.matrix[0][0] == self.matrix[1][1] == self.matrix[2][2] == 'o':
            self.win('o', 'd1', x, y)
        elif self.matrix[0][2] == self.matrix[1][1] == self.matrix[2][0] == 'o':
            self.win('o', 'd2', x, y)

    def create_cross(self, x, y):
        x0 = x1 = 150 + x * 100
        y0 = y1 = 150 + y * 100
        line_1 = self.canvas.create_line(x0, y0, x1, y1, width=5, fill='mediumturquoise')
        line_2 = self.canvas.create_line(x0, y1, x1, y0, width=5, fill='mediumturquoise')

        for i in range(80):
            x0 -= 0.35
            y0 -= 0.5
            x1 += 0.35
            y1 += 0.5
            self.canvas.coords(line_1, x0, y0, x1, y1)
            self.canvas.coords(line_2, x0, y1, x1, y0)
            sleep(0.0005)
            self.canvas.update()

    def create_oval(self, x, y):
        x0 = x1 = 150 + x * 100
        y0 = y1 = 150 + y * 100
        oval = self.canvas.create_oval(x0, y0, x1, y1, width=5, outline='mediumturquoise')
        for i in range(80):
            x0 -= 0.5
            y0 -= 0.5
            x1 += 0.5
            y1 += 0.5
            self.canvas.coords(oval, x0, y0, x1, y1)
            sleep(0.0005)
            self.canvas.update()

    def win(self, winner, position, x, y):
        if position == 'g':
            x0 = x1 = 250
            y = 150 + y * 100
            line = self.canvas.create_line(x0, y, x1, y, width=10, fill='mediumturquoise')
            for i in range(340):
                x0 -= 0.5
                x1 += 0.5
                self.canvas.coords(line, x0, y, x1, y)
                sleep(0.0005)
                self.canvas.update()
        elif position == 'v':
            x = 150 + x * 100
            y0 = y1 = 250
            line = self.canvas.create_line(x, y0, x, y1, width=10, fill='mediumturquoise')
            for i in range(340):
                y0 -= 0.5
                y1 += 0.5
                self.canvas.coords(line, x, y0, x, y1)
                sleep(0.0005)
                self.canvas.update()
        elif position == 'd1':
            x0 = x1 = 250
            y0 = y1 = 250
            line = self.canvas.create_line(x0, y0, x1, y1, width=10, fill='mediumturquoise')
            for i in range(340):
                x0 -= 0.5
                y0 -= 0.5
                x1 += 0.5
                y1 += 0.5
                self.canvas.coords(line, x0, y0, x1, y1)
                sleep(0.0005)
                self.canvas.update()
        else:
            x0 = x1 = 250
            y0 = y1 = 250
            line = self.canvas.create_line(x0, y0, x1, y1, width=10, fill='mediumturquoise')
            for i in range(340):
                y0 -= 0.5
                x1 -= 0.5
                x0 += 0.5
                y1 += 0.5
                self.canvas.coords(line, x0, y0, x1, y1)
                sleep(0.0005)
                self.canvas.update()
        self.canvas.create_text(250, 50, text=['Cross', 'Oval']['xo'.index(winner)], fill='mediumturquoise',
                                justify='center', font='verdana 60')
        self.canvas.create_text(250, 450, text='won, congrats!', fill='mediumturquoise', justify='center',
                                font='verdana 40')
        self.end = True


class Window:
    def __init__(self, name='tic-tac-toe'):
        self.tk = Tk()
        self.tk.title(name)
        self.tk.geometry('500x500')
        self.tk.resizable(False, False)

        self.canvas: Canvas = Canvas(self.tk, width=500, height=500, bg='lemonchiffon')
        self.canvas.pack()

        self.create_field()
        self.tic_tac_toe = TicTacToe(self.canvas)

    def create_field(self):
        self.canvas.create_line(100, 200, 400, 200, width=5, fill='mediumturquoise')
        self.canvas.create_line(100, 300, 400, 300, width=5, fill='mediumturquoise')
        self.canvas.create_line(200, 100, 200, 400, width=5, fill='mediumturquoise')
        self.canvas.create_line(300, 100, 300, 400, width=5, fill='mediumturquoise')


w = Window()
w.tk.bind("<Button-1>", lambda event: w.tic_tac_toe.move(event.x, event.y))
w.tk.bind("<E>", lambda event: w.tk.destroy())

w.tk.mainloop()
