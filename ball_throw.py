# все формулы взяты с сайта
# https://misis.ru/files/-/e8e7e2daf7d1c145e77830ff2c4361ba/Основные_кинематические_параметры_Уварова.pdf


from tkinter import Tk, Canvas, Label, Scale, Button
from math import sin, cos, atan, radians, degrees
import time


class SevenSegmentDisplay:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = 1100
        self.y = 10
        self.time = 0
        self.id_array = []
        self.width = 5
        self.length = 20
        self.color_on = 'darkblue'
        self.color_off = 'skyblue'
        self.color_outline = 'cyan'
        self.create_all()

    def start_time(self):
        """
        Устанавливает стартовое время (00:00)
        """
        self.select_digit(0, 0)
        self.select_digit(0, 1)
        self.select_digit(0, 2)

    def print_time(self):
        """
        Получает на вход время и отображает его на таймере
        """
        t = round(self.time, 2)
        t = str(t)

        while len(t[t.index('.'):]) != 3:
            t += '0'
        while len(t[:t.index('.')]) != 2:
            t = '0' + t

        s0, s1, ms0, ms1 = map(int, (t[0], t[1], t[3], t[4]))
        self.select_digit(s0, 0)
        self.select_digit(s1, 1)
        self.select_digit(ms0, 2)

    def create_all(self):
        """
        Создает все индикаторы и двоеточие по рассчитанным координатам
        """
        off = self.color_off
        outline = self.color_outline

        self.create_one(self.x, self.y)
        indent = self.length + 2 * self.width
        self.create_one(self.x + indent, self.y)

        self.canvas.create_rectangle(self.x + 2 * indent, self.y + self.length // 2, self.x + 2 * indent + self.width,
                                     self.y + self.length // 2 + self.width, fill=off, outline=outline)
        self.canvas.create_rectangle(self.x + 2 * indent, self.y + self.length // 2 + self.length,
                                     self.x + 2 * indent + self.width,
                                     self.y + self.length // 2 + self.width + self.length, fill=off, outline=outline)

        self.create_one(self.x + 2 * self.width + 2 * indent, self.y)
        self.start_time()

    def create_one(self, x_start, y_start):
        """
        Создает один индикатор
        """
        off = self.color_off
        outline = self.color_outline

        length = self.length
        width = self.width

        id_array = []

        x1 = x_start
        x2 = x1 + width // 2
        x3 = x2 + width // 2
        x4 = x1 + length
        x5 = x4 + width // 2
        x6 = x5 + width // 2

        y1 = y_start
        y2 = y1 + width // 2
        y3 = y2 + width // 2
        y4 = y1 + length
        y5 = y4 + width // 2
        y6 = y5 + width // 2
        y7 = y4 + length
        y8 = y7 + width // 2
        y9 = y8 + width // 2

        id_array.append(self.canvas.create_polygon((x2, y2), (x3, y3), (x3, y4), (x2, y5), (x1, y4), (x1, y3),
                                                   fill=off, outline=outline))
        id_array.append(self.canvas.create_polygon((x2, y2), (x3, y1), (x4, y1), (x5, y2), (x4, y3), (x3, y3),
                                                   fill=off, outline=outline))
        id_array.append(self.canvas.create_polygon((x5, y2), (x6, y3), (x6, y4), (x5, y5), (x4, y4), (x4, y3),
                                                   fill=off, outline=outline))
        id_array.append(self.canvas.create_polygon((x2, y5), (x3, y4), (x4, y4), (x5, y5), (x4, y6), (x3, y6),
                                                   fill=off, outline=outline))
        id_array.append(self.canvas.create_polygon((x2, y5), (x3, y6), (x3, y7), (x2, y8), (x1, y7), (x1, y6),
                                                   fill=off, outline=outline))
        id_array.append(self.canvas.create_polygon((x2, y8), (x3, y7), (x4, y7), (x5, y8), (x4, y9), (x3, y9),
                                                   fill=off, outline=outline))
        id_array.append(self.canvas.create_polygon((x5, y5), (x6, y6), (x6, y7), (x5, y8), (x4, y7), (x4, y6),
                                                   fill=off, outline=outline))

        self.id_array.append(id_array)

    def select_digit(self, digit, segment):
        """
        Отрисовывает цифру digit на индикаторе № segment
        """
        on = self.color_on
        off = self.color_off
        if digit == 0:
            self.canvas.itemconfig(self.id_array[segment][0], fill=on)
            self.canvas.itemconfig(self.id_array[segment][1], fill=on)
            self.canvas.itemconfig(self.id_array[segment][2], fill=on)
            self.canvas.itemconfig(self.id_array[segment][3], fill=off)
            self.canvas.itemconfig(self.id_array[segment][4], fill=on)
            self.canvas.itemconfig(self.id_array[segment][5], fill=on)
            self.canvas.itemconfig(self.id_array[segment][6], fill=on)
        elif digit == 1:
            self.canvas.itemconfig(self.id_array[segment][0], fill=off)
            self.canvas.itemconfig(self.id_array[segment][1], fill=off)
            self.canvas.itemconfig(self.id_array[segment][2], fill=on)
            self.canvas.itemconfig(self.id_array[segment][3], fill=off)
            self.canvas.itemconfig(self.id_array[segment][4], fill=off)
            self.canvas.itemconfig(self.id_array[segment][5], fill=off)
            self.canvas.itemconfig(self.id_array[segment][6], fill=on)
        elif digit == 2:
            self.canvas.itemconfig(self.id_array[segment][0], fill=off)
            self.canvas.itemconfig(self.id_array[segment][1], fill=on)
            self.canvas.itemconfig(self.id_array[segment][2], fill=on)
            self.canvas.itemconfig(self.id_array[segment][3], fill=on)
            self.canvas.itemconfig(self.id_array[segment][4], fill=on)
            self.canvas.itemconfig(self.id_array[segment][5], fill=on)
            self.canvas.itemconfig(self.id_array[segment][6], fill=off)
        elif digit == 3:
            self.canvas.itemconfig(self.id_array[segment][0], fill=off)
            self.canvas.itemconfig(self.id_array[segment][1], fill=on)
            self.canvas.itemconfig(self.id_array[segment][2], fill=on)
            self.canvas.itemconfig(self.id_array[segment][3], fill=on)
            self.canvas.itemconfig(self.id_array[segment][4], fill=off)
            self.canvas.itemconfig(self.id_array[segment][5], fill=on)
            self.canvas.itemconfig(self.id_array[segment][6], fill=on)
        elif digit == 4:
            self.canvas.itemconfig(self.id_array[segment][0], fill=on)
            self.canvas.itemconfig(self.id_array[segment][1], fill=off)
            self.canvas.itemconfig(self.id_array[segment][2], fill=on)
            self.canvas.itemconfig(self.id_array[segment][3], fill=on)
            self.canvas.itemconfig(self.id_array[segment][4], fill=off)
            self.canvas.itemconfig(self.id_array[segment][5], fill=off)
            self.canvas.itemconfig(self.id_array[segment][6], fill=on)
        elif digit == 5:
            self.canvas.itemconfig(self.id_array[segment][0], fill=on)
            self.canvas.itemconfig(self.id_array[segment][1], fill=on)
            self.canvas.itemconfig(self.id_array[segment][2], fill=off)
            self.canvas.itemconfig(self.id_array[segment][3], fill=on)
            self.canvas.itemconfig(self.id_array[segment][4], fill=off)
            self.canvas.itemconfig(self.id_array[segment][5], fill=on)
            self.canvas.itemconfig(self.id_array[segment][6], fill=on)
        elif digit == 6:
            self.canvas.itemconfig(self.id_array[segment][0], fill=on)
            self.canvas.itemconfig(self.id_array[segment][1], fill=on)
            self.canvas.itemconfig(self.id_array[segment][2], fill=off)
            self.canvas.itemconfig(self.id_array[segment][3], fill=on)
            self.canvas.itemconfig(self.id_array[segment][4], fill=on)
            self.canvas.itemconfig(self.id_array[segment][5], fill=on)
            self.canvas.itemconfig(self.id_array[segment][6], fill=on)
        elif digit == 7:
            self.canvas.itemconfig(self.id_array[segment][0], fill=off)
            self.canvas.itemconfig(self.id_array[segment][1], fill=on)
            self.canvas.itemconfig(self.id_array[segment][2], fill=on)
            self.canvas.itemconfig(self.id_array[segment][3], fill=off)
            self.canvas.itemconfig(self.id_array[segment][4], fill=off)
            self.canvas.itemconfig(self.id_array[segment][5], fill=off)
            self.canvas.itemconfig(self.id_array[segment][6], fill=on)
        elif digit == 8:
            self.canvas.itemconfig(self.id_array[segment][0], fill=on)
            self.canvas.itemconfig(self.id_array[segment][1], fill=on)
            self.canvas.itemconfig(self.id_array[segment][2], fill=on)
            self.canvas.itemconfig(self.id_array[segment][3], fill=on)
            self.canvas.itemconfig(self.id_array[segment][4], fill=on)
            self.canvas.itemconfig(self.id_array[segment][5], fill=on)
            self.canvas.itemconfig(self.id_array[segment][6], fill=on)
        elif digit == 9:
            self.canvas.itemconfig(self.id_array[segment][0], fill=on)
            self.canvas.itemconfig(self.id_array[segment][1], fill=on)
            self.canvas.itemconfig(self.id_array[segment][2], fill=on)
            self.canvas.itemconfig(self.id_array[segment][3], fill=on)
            self.canvas.itemconfig(self.id_array[segment][4], fill=off)
            self.canvas.itemconfig(self.id_array[segment][5], fill=on)
            self.canvas.itemconfig(self.id_array[segment][6], fill=on)
        tk.update()


class Platform:
    def __init__(self, canvas, ball):
        self.canvas = canvas
        self.ball = ball
        self.x0 = self.ball.x_center - self.ball.radius
        self.y0 = self.ball.y_center + self.ball.radius
        self.x1 = self.ball.x_center + self.ball.radius
        self.y1 = 700
        self.obj = self.canvas.create_rectangle(self.x0, self.y0, self.x1, 700, fill='cyan', outline='blue')

    def move(self, x0, y0):
        """
        Поднимает или опускает платформу
        """
        self.canvas.coords(self.obj, x0, y0, self.x1, self.y1)
        self.x0 = x0
        self.y0 = y0


class Trajectory:
    def __init__(self, canvas, x_center, y_center):
        self.canvas = canvas
        self.x_center = x_center
        self.y_center = y_center
        self.angle = 45
        self.start_velocity = 70
        self.gravitation = 10
        self.coords_array = []
        self.id_array = []
        self.radius = 5

        self.start()

    def start(self):
        """
        Строит траекторию полета, перед этим удалив предыдущую
        """
        self.canvas.delete('trajectory')
        if not 0 <= self.angle <= 90:
            return

        height = 575 - self.y_center
        time = 0

        last_x = 0
        last_y = 0
        x = 0
        y = 0
        while 575 >= y:
            last_x, x = x, 75 + int(self.start_velocity * time * cos(radians(self.angle)))
            last_y, y = y, 575 - height - int(
                self.start_velocity * time * sin(radians(self.angle)) - ((self.gravitation * time ** 2) / 2))
            if y <= 575:
                self.id_array.append(
                    self.canvas.create_oval(x - self.radius, y - self.radius, x + self.radius, y + self.radius,
                                            fill='yellow', outline='black', width=2, tag='trajectory'))
            time += 1

        x = int((575 - last_y) / (y - last_y) * (x - last_x)) + last_x
        y = 575
        self.id_array.append(
            self.canvas.create_oval(x - self.radius, y - self.radius, x + self.radius, y + self.radius, fill='orange',
                                    outline='black', width=2, tag='trajectory'))


class Vector:
    def __init__(self, canvas, x0, y0, x1, y1, ball):
        self.canvas = canvas
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.start_velocity = 0
        self.angle = 45
        self.ball = ball
        self.get_angle_and_start_velocity()
        self.obj = None

        self.create_vector()

    def create_vector(self):
        """
        Создает стрелку
        """
        self.obj = canvas.create_line(self.x0, self.y0, self.x1, self.y1, width=3, fill='blue', arrow='last',
                                      arrowshape=(10, 20, 10))

    def move_vector(self, x0, y0, x1, y1):
        """
        Меняет координаты стрелки на (x0, y0), (x1, y1)
        """
        if self.obj is None:
            return

        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

        self.canvas.coords(self.obj, x0, y0, x1, y1)
        self.get_angle_and_start_velocity()

        self.ball.trajectory.angle = self.angle
        self.ball.trajectory.start_velocity = self.start_velocity
        self.ball.trajectory.start()

        fix_display()

    def drag(self):
        """
        Позволяет оттягивать стрелку мышью
        """
        mouse_x = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()
        mouse_y = self.canvas.winfo_pointery() - self.canvas.winfo_rooty()
        if self.x1 - 25 <= mouse_x <= self.x1 + 25 and self.y1 - 25 <= mouse_y <= self.y1 + 25:
            self.move_vector(self.x0, self.y0, mouse_x, mouse_y)

    def back(self, x1, y1):
        """
        Возвращает стрелку в начальное положение(угол 45, скорость 70)
        """
        self.move_vector(self.x0, self.y0, x1, y1)

    def cleaning(self):
        """
        Удаление стрелки
        """
        if self.obj is not None:
            self.canvas.delete(self.obj)
            self.obj = None

    def get_angle_and_start_velocity(self):
        """
        Вычисляет угол и начальную скорость по стрелке
        """
        a = self.y0 - self.y1
        b = self.x1 - self.x0
        if b < 0 or a < 0:
            self.angle = -1
            self.start_velocity = -1
        elif b == 0:
            self.angle = 90
        else:
            self.angle = int(degrees(atan(radians(degrees(a / b)))))
            self.start_velocity = int((a ** 2 + b ** 2) ** 0.5)


class Ball:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x_center = 75
        self.y_center = 575
        self.radius = 25
        self.angle = 45
        self.start_velocity = 70
        self.gravitation = 10
        self.velocity = 0
        self.vector_x = None
        self.vector_y = None
        self.obj = self.canvas.create_oval(self.x_center - self.radius,
                                           self.y_center - self.radius,
                                           self.x_center + self.radius,
                                           self.y_center + self.radius,
                                           fill='red', outline='black', width=2)
        self.timer = SevenSegmentDisplay(canvas)
        self.vector = Vector(self.canvas, self.x_center, self.y_center, self.x_center + 2 * self.radius,
                             self.y_center - 2 * self.radius, self)
        self.trajectory = Trajectory(self.canvas, self.x_center, self.y_center)
        self.platform = Platform(canvas, self)

    def vectors(self, velocity_x=1, velocity_y=1):
        """
        Двигает векторы self.vector_x и self.vector_y. Если их нет, рисует их
        """
        if self.vector_x is None:
            self.vector_x = self.canvas.create_line(self.x_center, self.y_center, self.x_center + velocity_x * 2,
                                                    self.y_center, width=3, fill='green', arrow='last',
                                                    arrowshape="10 20 10")
        else:
            self.canvas.coords(self.vector_x,
                               self.x_center, self.y_center, self.x_center + velocity_x * 2, self.y_center)

        if self.vector_y is None:
            self.vector_y = self.canvas.create_line(self.x_center, self.y_center, self.x_center,
                                                    self.y_center - velocity_y, width=3, fill='orange', arrow='last',
                                                    arrowshape="10 20 10")
        else:
            self.canvas.coords(self.vector_y, self.x_center, self.y_center, self.x_center, self.y_center - velocity_y)

    def move_oval(self, x=1, y=-1, delay=0.1):
        """
        Двигает мяч на х по горизонтали и на у по вертикали, после делает задержку на delay сек
        """
        self.canvas.move(self.obj, x, y)

        self.x_center += x
        self.y_center += y

        time.sleep(delay)
        tk.update()

    def start(self, start_velocity, angle):
        """
        Осуществляет бросок мяча
        """
        self.angle = angle
        self.start_velocity = start_velocity

        if not 0 <= self.angle <= 90:
            return

        self.vector.cleaning()
        y_now = 575 - self.y_center

        start_velocity_x = (self.start_velocity * cos(radians(self.angle)))

        time = 0
        y_current = 0

        velocity_x = 0
        velocity_y = 0

        while y_now + y_current >= 0:
            last_x, velocity_x = velocity_x, int(start_velocity_x * cos(radians(self.angle)))
            last_y, velocity_y = velocity_y, int(start_velocity_x * sin(radians(self.angle)) - self.gravitation * time)

            x_current = int(self.start_velocity * time * cos(radians(self.angle)))
            y_current = int(
                self.start_velocity * time * sin(radians(self.angle)) - ((self.gravitation * time ** 2) / 2))

            if 575 - y_current - y_now > 575:
                y = 575 - y_now - y_current
                x = 75 + int((575 - last_y) / (y - last_y) * (x_current - last_x)) + last_x
                self.move_oval(x - self.x_center, 575 - self.y_center)

            else:
                self.move_oval(x_current - self.x_center + 75, 575 - self.y_center - y_current - y_now)

            time += 0.1
            self.velocity = int((velocity_x ** 2 * velocity_y ** 2) ** 0.5)

            self.timer.time = time
            self.timer.print_time()

            self.vectors(velocity_x, velocity_y)
            fix_display()
        self.velocity = 0
        fix_display()

    def restart(self):
        """
        Передвигает мяч на стартовое положение
        """
        self.vector.cleaning()
        self.move_oval(75 - self.x_center, 575 - self.y_center)
        self.vectors(0, 0)
        self.vector.create_vector()
        self.vector.move_vector(self.x_center, self.y_center,
                                self.x_center + 2 * self.radius,
                                self.y_center - 2 * self.radius)
        self.trajectory.y_center = self.y_center
        self.trajectory.start()

        self.platform.move(self.x_center - self.radius, self.y_center + self.radius)

        self.timer.start_time()
        fix_display()


def get_height():
    """
    Считывает высоту с бегунка
    """
    height = height_bar.get()
    new = 550 - (ball.y_center - ball.radius) - height
    ball.move_oval(0, new)

    ball.vector.move_vector(ball.x_center, ball.y_center, ball.vector.x1, ball.vector.y1 + new)

    ball.trajectory.y_center = ball.y_center
    ball.trajectory.start()

    ball.platform.move(ball.x_center - ball.radius, ball.y_center + ball.radius)

    fix_display()


def get_gravitation():
    """
    Считывает ускорение свободного падения с бегунка
    """
    gravitation = gravitation_bar.get()
    ball.gravitation = gravitation
    ball.trajectory.gravitation = gravitation
    ball.trajectory.start()
    fix_display()


def fix_display():
    """
    Обновляет все показатели на экране
    """
    x_label.config(text="X: " + str(ball.x_center - 75))
    y_label.config(text="Y: " + str(575 - ball.y_center))
    angle_label.config(text="Угол: " + str(ball.vector.angle))
    start_velocity_label.config(text="Н. скорость: " + str(ball.vector.start_velocity))
    acceleration_label.config(text="Ускорение: " + str(ball.gravitation))
    velocity_label.config(text="Текущ. скорость: " + str(ball.velocity))


def _exit():
    """
    Закрывает приложение
    """
    tk.destroy()


# создание поля
tk = Tk()
tk.title('ball')
tk.resizable(False, False)
canvas = Canvas(tk, width=1200, height=700)
canvas.pack()

# Создание мяча
ball = Ball(canvas)

# создание бегунка "Ускорение свободного падения"
gravitation_bar = Scale(tk, from_=20, to=5)
gravitation_bar.set(10)
gravitation_bar.place(x=10, y=100)
# кнопка для ускорения свободного падения
btn_gravitation = Button(tk, text='Применить', command=lambda: get_gravitation())
btn_gravitation.place(x=60, y=170)
# надпись "Ускорение свободного падения"
canvas.create_text(110, 140, text="Ускорение\nсвободного\nпадения")

# создание бегунка "Высота"
height_bar = Scale(tk, from_=0, to=200, orient='horizontal')
height_bar.set(0)
height_bar.place(x=200, y=625)
# кнопка для высоты
btn_height = Button(tk, text='Применить', command=lambda: get_height())
btn_height.place(x=255, y=665)
# надпись "Высота"
canvas.create_text(225, 680, text="Высота")

# надпись "Угол"
angle_label = Label(anchor='w', text="Угол: " + str(ball.vector.angle))
angle_label.place(x=5, y=68)

# надпись "Нач. скорость"
start_velocity_label = Label(anchor='w', text="Нач. скорость: " + str(ball.vector.start_velocity))
start_velocity_label.place(x=5, y=8)

# надпись "Текущ. скорость"
velocity_label = Label(anchor='w', text="Текущ. скорость: " + str(ball.velocity))
velocity_label.place(x=5, y=89)

# надпись "Ускорение"
acceleration_label = Label(anchor='w', text="Ускорение: " + str(ball.gravitation))
acceleration_label.place(x=5, y=38)

# надпись "X"
x_label = Label(anchor='w', text="X: " + str(ball.x_center - 75))
x_label.place(x=550, y=10)
# надпись "Y"
y_label = Label(anchor='w', text="Y: " + str(575 - ball.y_center))
y_label.place(x=630, y=10)

# кнопка для старта
btn_start = Button(tk, text='Старт', command=lambda: ball.start(ball.vector.start_velocity, ball.vector.angle))
btn_start.place(x=1110, y=605)

# кнопка для рестарта
btn_restart = Button(tk, text='Рестарт', command=lambda: ball.restart())
btn_restart.place(x=1110, y=635)

# кнопка для выхода
btn_exit = Button(tk, text='Выход', command=lambda: _exit())
btn_exit.place(x=1110, y=665)

# движение мыши с удерживаемой ЛКМ для оттягивания стрелки
tk.bind("<B1-Motion>", lambda event: ball.vector.drag())

# кнопка для приведения стрелки в стандартное положение
btn_vector = Button(tk, text='Вернуть''\n''стрелку',
                    command=lambda: ball.vector.back(ball.x_center + 2 * ball.radius, ball.y_center - 2 * ball.radius))
btn_vector.place(x=110, y=650)

tk.mainloop()
