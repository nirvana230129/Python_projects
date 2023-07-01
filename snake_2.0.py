from tkinter import *
import random
import time


class Field:
    def __init__(self, tk, column, row, w, color_in, color_out):
        self.tk = tk
        self.column = column
        self.row = row
        self.w = w
        self.color_in = color_in
        self.color_out = color_out

        self.id_array = []

        self.create_canvas()
        self.create()

    def create_canvas(self):
        """
        Создает canvas
        """
        self.canvas = Canvas(self.tk,
                             width=(self.row + 2) * self.w,
                             height=(self.column + 2) * self.w)
        self.canvas.pack()

    def create(self):
        """
        Заполняет id_array и отрисовывает поле
        """
        for i in range(self.row):
            self.id_array.append([])
            for j in range(self.column):
                self.id_array[i].append(self.canvas.create_rectangle((1+j) * self.w,
                                                                     (1+i) * self.w,
                                                                     (j+2) * self.w,
                                                                     (i+2) * self.w,
                                                                     fill=self.color_in,
                                                                     outline=self.color_out))

    def death(self):
        """
        Анимация проигрыша
        """
        w = (self.w * self.row / 15)
        #          1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
        colors = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 0
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 1
                  [0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0],  # 2
                  [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],  # 3
                  [0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],  # 4
                  [0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],  # 5
                  [0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0],  # 6
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 7
                  [0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0],  # 8
                  [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0],  # 9
                  [0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0],  # 10
                  [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0],  # 11
                  [0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0],  # 12
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 13
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]  # 14

        self.canvas.create_rectangle(0,
                                     0,
                                     w + (15 + 1) * w,
                                     w + (15 + 1) * w,
                                     fill='black')
        for i in range(15):
            for j in range(15):
                if colors[i][j] == 1:
                    self.canvas.create_rectangle(w + j * w,
                                                 w + i * w,
                                                 w + (j + 1) * w,
                                                 w + (i + 1) * w,
                                                 fill='red')
                tk.update()
                time.sleep(0.01)
        for i in range(col):
            for j in range(row):
                self.canvas.delete(self.id_array[i][j])


class Snake:
    def __init__(self, field, color_in, color_out, color_head):
        self.field = field

        self.color_in = color_in
        self.color_out = color_out
        self.color_head = color_head

        self.coordinates = self.create_snake()
        self.delta_x = 0
        self.delta_y = -1

        self.is_dead = False

        self.food_manager = None

    def add_food_manager(self, food_manager):
        """
        добавляет параметр food_manager
        """
        self.food_manager = food_manager

    def create_snake(self):
        """
        Создает и отрисовывает змею
        """
        head_x = self.field.column // 2
        head_y = self.field.row // 2
        snake = [[head_x, head_y],
                 [head_x, head_y + 1],
                 [head_x, head_y + 2]]
        self.field.canvas.itemconfig(self.field.id_array[head_y][head_x],
                                     fill=self.color_head,
                                     outline=self.color_out)
        for i in range(1, len(snake)):
            self.field.canvas.itemconfig(self.field.id_array[snake[i][1]][snake[i][0]],
                                         fill=self.color_in,
                                         outline=self.color_out)
        time.sleep(1.5)
        return snake

    def change_direction(self, x, y):
        """
        Изменяет направление движения змеи
        """
        if not((x == -self.delta_x and y == self.delta_y) or (y == -self.delta_y and x == self.delta_x)):
            self.delta_x = x
            self.delta_y = y

    def move(self):
        """
        Двигает змею
        """
        head_x = self.coordinates[0][0]
        head_y = self.coordinates[0][1]
        new_x = head_x + self.delta_x
        new_y = head_y + self.delta_y

        if not (0 <= new_x <= self.field.column - 1) or not (0 <= new_y <= self.field.row - 1) or \
                [new_x, new_y] in self.coordinates:
            time.sleep(1.5)
            self.field.death()
            self.move = self.after_death
        else:
            self.food_manager.add_food()
            flag_eat = False

            if [new_x, new_y] in food_manager.food_coordinates:
                self.food_manager.eating(new_x, new_y)
                flag_eat = True

            self.field.canvas.itemconfig(self.field.id_array[head_y][head_x],
                                         fill=self.color_in,
                                         outline=self.color_out)

            self.coordinates.insert(0, [new_x, new_y])
            self.field.canvas.itemconfig(self.field.id_array[new_y][new_x],
                                         fill=self.color_head,
                                         outline=self.color_out)
            if flag_eat is False:
                old_x, old_y = self.coordinates.pop()
                self.field.canvas.itemconfig(self.field.id_array[old_y][old_x],
                                             fill=self.field.color_in,
                                             outline=self.field.color_out)

    def after_death(self, *a):
        """
        Исключает возможность движения змеи после смерти оной
        """
        self.is_dead = True
        pass


class Food:
    def __init__(self, x, y, color, time_added):
        self.x = x
        self.y = y
        self.color = color
        self.time_added = time_added


class FoodManager:
    def __init__(self, field, snake, colors):
        self.field = field
        self.snake = snake
        self.colors = colors

        self.food_coordinates = []
        self.food_array = []

        self.add_food()

    def add_food(self):
        """
        Создание новой единицы еды и ее отрисовка
        """
        if not self.food_coordinates or time.time() >= self.food_array[-1].time_added + 0.0005:
            x = random.randint(0, self.field.column - 1)
            y = random.randint(0, self.field.row - 1)
            while [x, y] in self.food_coordinates + self.snake.coordinates:
                x = random.randint(0, self.field.column - 1)
                y = random.randint(0, self.field.row - 1)

            color = random.choice(self.colors)

            self.food_coordinates.append([x, y])

            self.food_array.append(Food(x, y, color, time.time()))

            self.field.canvas.itemconfig(self.field.id_array[y][x], fill=color)

    def eating(self, x, y):
        """
        Съедание еды
        """
        self.food_coordinates.remove([x, y])
        self.field.canvas.itemconfig(self.field.id_array[y][x],
                                     fill=self.field.color_in,
                                     outline=self.field.color_out)


# Создание окна
tk = Tk()
tk.title('змейка')
#tk.resizable(False, False)


# Размеры окна
row = 25
col = 25
w = 20

# Создание всех объектов
field = Field(tk, col, row, w, 'lightcyan', 'darkblue')
snake = Snake(field, 'green', 'darkgreen', 'limegreen')
food_manager = FoodManager(field, snake, ['yellow', 'orangered', 'darkmagenta'])
snake.food_manager = food_manager

# Клавиши
tk.bind('<w>', lambda event: snake.change_direction(0, -1))
tk.bind('<a>', lambda event: snake.change_direction(-1, 0))
tk.bind('<s>', lambda event: snake.change_direction(0, 1))
tk.bind('<d>', lambda event: snake.change_direction(1, 0))

# Старт движения
while snake.is_dead is False:
    time.sleep(0.1)
    tk.update()
    snake.move()

tk.mainloop()
