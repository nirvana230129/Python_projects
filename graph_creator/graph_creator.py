from tkinter import Tk, Canvas


class BallsManager:
    def __init__(self, canvas):
        self.canvas = canvas
        self.balls = []
        self.selected_ball = None

    def ball_create(self, x, y):
        """
        Создает мяч (экземпляр класса Ball) с центром в точке с координатами (х, y)
        """
        for ball in self.balls:
            if ((ball.x - x) ** 2 + (ball.y - y) ** 2) ** 0.5 < 2 * ball.radius + 5:
                break
        else:
            ball = Ball(canvas, x, y)
            self.balls.append(ball)

            if not lines_manager.matrix:
                lines_manager.matrix = [[0]]
            else:
                for i in range(len(lines_manager.matrix)):
                    lines_manager.matrix[i].append(0)
                lines_manager.matrix.append([0] * len(lines_manager.matrix[-1]))
            lines_manager.update_matrix()

    def ball_drag(self):
        """
        Двигает мяч и связанные с ним линии
        """
        ball_x = None
        for ball in self.balls:
            x = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()
            y = self.canvas.winfo_pointery() - self.canvas.winfo_rooty()

            if ((ball.x - x) ** 2 + (ball.y - y) ** 2) ** 0.5 <= ball.radius:
                for ball_near in self.balls:
                    if ball_near.id == ball.id:
                        continue
                    if ((ball_near.x - x) ** 2 + (ball_near.y - y) ** 2) ** 0.5 < 2 * ball_near.radius + 5:
                        break
                else:
                    ball_x = ball
                    ball.x = x
                    ball.y = y
                    self.canvas.coords(ball.id,
                                       x - ball.radius,
                                       y - ball.radius,
                                       x + ball.radius,
                                       y + ball.radius)
                    self.canvas.coords(ball.text, x, y)
                    break

        if ball_x is not None:
            for i in range(len(lines_manager.ways)):
                way = lines_manager.ways[i]
                line = lines_manager.lines[i]
                if ball_x.index == way[0]:
                    self.canvas.coords(line.id,
                                       ball_x.x,
                                       ball_x.y,
                                       line.x1,
                                       line.y1)
                    line.x0 = ball_x.x
                    line.y0 = ball_x.y

                elif ball_x.index == way[1]:
                    self.canvas.coords(line.id,
                                       line.x0,
                                       line.y0,
                                       ball_x.x,
                                       ball_x.y)
                    line.x1 = ball_x.x
                    line.y1 = ball_x.y

    def select_ball(self, x, y):
        """
        Выбирает мяч в котором лежит точка с координатами (х, y)
        """
        for ball in self.balls:
            if ((ball.x - x) ** 2 + (ball.y - y) ** 2) ** 0.5 < ball.radius:
                self.selected_ball = ball
                self.canvas.itemconfig(ball.id, fill='cyan', outline='blue')
                break

    def delete_ball(self):
        """
        Удаляет выбранный мяч и все линии, которые к нему идут
        """
        if self.selected_ball is not None:
            for ball in self.balls:
                if ball.id == self.selected_ball.id:
                    lines_manager.matrix.pop(ball.index)
                    for i in lines_manager.matrix:
                        i.pop(ball.index)
                    lines_manager.update_matrix()

                    for i in range(len(lines_manager.lines) - 1, -1, -1):
                        if ball.index in lines_manager.ways[i]:
                            lines_manager.ways.pop(i)
                            canvas.delete(lines_manager.lines[i].id)
                            lines_manager.lines.pop(i)

                    for i in range(len(lines_manager.ways)):
                        if lines_manager.ways[i][0] > ball.index:
                            lines_manager.ways[i][0] -= 1
                        if lines_manager.ways[i][1] > ball.index:
                            lines_manager.ways[i][1] -= 1

                    ind = self.balls.index(ball)
                    self.canvas.delete(self.balls[ind].text)
                    self.canvas.delete(self.balls[ind].id)
                    self.balls.pop(ind)
                    self.selected_ball = None

                    for i in range(ind, len(self.balls)):
                        self.balls[i].index -= 1
                        self.canvas.itemconfig(self.balls[i].text, text=str(self.balls[i].index))
                    break


class Ball:
    def __init__(self, canvas, x, y, radius=50, fill_color='orange', outline_color='red'):
        self.canvas = canvas

        self.x = x
        self.y = y
        self.radius = radius

        self.fill_color = fill_color
        self.outline_color = outline_color

        self.index = len(balls_manager.balls)
        self.id = self.canvas.create_oval(self.x - self.radius,
                                          self.y - self.radius,
                                          self.x + self.radius,
                                          self.y + self.radius,
                                          fill=self.fill_color,
                                          outline=self.outline_color,
                                          width=self.radius // 10)
        self.time_selected = 0

        self.text = canvas.create_text(x, y, text=str(len(balls_manager.balls)), font="Verdana 25")


class LinesManager:
    def __init__(self, canvas, file_name='matrix.txt'):
        self.canvas = canvas

        self.lines = []
        self.ways = []
        self.matrix = []

        self.file_name = file_name
        file = open(self.file_name, 'w')
        file.close()

    def line_create(self, x0, y0, x1, y1, index1, index2):
        """
        Создает линию между точками с координатами (х0, у0), (х1, у1)
        """
        way = [index1, index2]
        if way not in self.ways and way[::-1] not in self.ways:
            self.lines.append(Line(self.canvas, x0, y0, x1, y1))
            self.ways.append(way)
            self.matrix[index1][index2] = 1
            self.matrix[index2][index1] = 1
        self.update_matrix()

    def update_matrix(self):
        """
        Строит матрицу по созданному графу, сохраняет последнюю ее версию в файле 'matrix.txt'
        """
        file = open(self.file_name, 'w')
        for i in self.matrix:
            file.write(' '.join(list(map(str, i))) + '\n')
        file.close()


class Line:
    def __init__(self, canvas, x0, y0, x1, y1, fill_color='black', width=3):
        self.canvas = canvas

        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

        self.fill_color = fill_color
        self.width = width

        self.id = self.canvas.create_line(self.x0,
                                          self.y0,
                                          self.x1,
                                          self.y1,
                                          fill=self.fill_color,
                                          width=self.width)
        self.canvas.lower(self.id)

        # Поставить на задний фон


def click(x, y):
    """
    Обрабатывает клик: либо выбирает мяч, либо строит линию между новым и уже выбранным, либо строит новый мяч
    """
    for ball in balls_manager.balls:
        if ((ball.x - x) ** 2 + (ball.y - y) ** 2) ** 0.5 < ball.radius:
            if balls_manager.selected_ball is None:
                balls_manager.select_ball(x, y)
            else:
                if ball == balls_manager.selected_ball:
                    canvas.itemconfig(ball.id, fill=ball.fill_color, outline=ball.outline_color)
                    balls_manager.selected_ball = None
                    continue

                lines_manager.line_create(balls_manager.selected_ball.x,
                                          balls_manager.selected_ball.y,
                                          ball.x,
                                          ball.y,
                                          balls_manager.selected_ball.index,
                                          ball.index)

                canvas.itemconfig(balls_manager.selected_ball.id,
                                  fill=balls_manager.selected_ball.fill_color,
                                  outline=balls_manager.selected_ball.outline_color)

                balls_manager.selected_ball = None
            break

    else:
        balls_manager.ball_create(x, y)


# создание поля
tk = Tk()
tk.title('graph')
tk.resizable(False, False)
canvas = Canvas(tk, width=1200, height=700)
canvas.pack()

balls_manager = BallsManager(canvas)
lines_manager = LinesManager(canvas)

# нажатия на клавиши
tk.bind("<Double-Button-1>", lambda event: click(event.x, event.y))
tk.bind("<B1-Motion>", lambda event: balls_manager.ball_drag())
tk.bind("<d>", lambda event: balls_manager.delete_ball())

tk.mainloop()
