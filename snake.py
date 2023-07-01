import time
from tkinter import *
from random import randint, choice


# создание поля и заполнение массива с id квадратов
def create_field(row, col, w):
    array = []
    for i in range(row):
        array.append([])
        for j in range(col):
            array[i].append(canvas.create_rectangle((1 + j) * w,
                                                    (1 + i) * w,
                                                    (j + 2) * w,
                                                    (i + 2) * w,
                                                    fill='lightcyan'))
    return array


# создание змеи
def create_snake(id_array):
    head_x = len(id_array) // 2
    head_y = len(id_array[0]) // 2
    snake = [[head_x, head_y], [head_x, head_y + 1], [head_x, head_y + 2]]
    canvas.itemconfig(id_array[snake[0][1]][snake[0][0]], fill='limegreen')
    for i in range(1, len(snake)):
        canvas.itemconfig(id_array[snake[i][1]][snake[i][0]], fill='green')
    return snake


# создание еды
def create_food(id_array):
    global row, col, snake_array
    food = snake_array[0]
    while food in snake_array:
        food = [randint(0, row - 1), randint(0, col - 1)]
    colors = ['yellow', 'orangered', 'darkmagenta']
    color = choice(colors)
    canvas.itemconfig(id_array[food[1]][food[0]], fill=color)
    return food


# проверка на съедение еды
def eating(id_array):
    global snake_array, food
    if food == snake_array[0]:
        snake_array.append(snake_array[-1])
        canvas.itemconfig(id_array[food[1]][food[0]], fill='limegreen')
        food = create_food(id_array)


# движение
def move(id_array, x, y):
    global snake_array, food
    x_head = snake_array[0][0]
    y_head = snake_array[0][1]
    if y_head == 0 and x == 0 and y == -1:
        death(id_array)
    elif x_head == 0 and x == -1 and y == 0:
        death(id_array)
    elif y_head == len(id_array) - 1 and x == 0 and y == 1:
        death(id_array)
    elif x_head == len(id_array[0]) - 1 and x == 1 and y == 0:
        death(id_array)
    else:
        snake_array.insert(0, [x_head + x, y_head + y])
        canvas.itemconfig(id_array[snake_array[1][1]][snake_array[1][0]], fill='green')
        canvas.itemconfig(id_array[snake_array[len(snake_array) - 1][1]][snake_array[len(snake_array) - 1][0]],
                          fill='lightcyan')
        canvas.itemconfig(id_array[snake_array[0][1]][snake_array[0][0]], fill='limegreen')
        snake_array.pop(-1)
        eating(id_array)
        if snake_array[0] in snake_array[1:]:
            death(id_array)


def death(id_array):
    global row, col, w, move, after_death
    w2 = (w * row / 15)
    #          1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
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

    canvas.create_rectangle(0,
                            0,
                            w + (15 + 1) * w2,
                            w + (15 + 1) * w2,
                            fill='black')
    for i in range(15):
        for j in range(15):
            if colors[i][j] == 1:
                canvas.create_rectangle(w + j * w2,
                                        w + i * w2,
                                        w + (j + 1) * w2,
                                        w + (i + 1) * w2,
                                        fill='red')
            time.sleep(0.01)
            tk.update()
    for i in range(col):
        for j in range(row):
            canvas.delete(id_array[i][j])

    move = after_death


def after_death(*kwargs):
    pass


# размеры поля из квадратиков
row = 12
col = 12
w = 20

# создание окна
tk = Tk()
tk.title('Змейка')
tk.resizable(False, False)
canvas = Canvas(tk, width=(row + 2) * w, height=(col + 2) * w)
canvas.pack()

id_array = create_field(row, col, w)
snake_array = create_snake(id_array)
food = create_food(id_array)

# клавиши
tk.bind('<w>', lambda event: move(id_array, 0, -1))
tk.bind('<a>', lambda event: move(id_array, -1, 0))
tk.bind('<s>', lambda event: move(id_array, 0, 1))
tk.bind('<d>', lambda event: move(id_array, 1, 0))

tk.mainloop()
