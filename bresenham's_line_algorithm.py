from tkinter import *


def create_field(row, col, w):
    array = []
    for i in range(row):
        array.append([])
        for j in range(col):
            array[i].append(canvas.create_rectangle((j + 1) * w,
                                                    (i + 1) * w,
                                                    (j + 2) * w,
                                                    (i + 2) * w,
                                                    fill='blue'))
            tk.update()
    return array


def print_line(coords, id_array):
    x0, y0 = coords[0]
    x1, y1 = coords[1]
    # горизонтальная прямая
    if y0 == y1:
        y = y0
        for i in range(min(x0, x1), max(x0, x1) + 1):
            canvas.itemconfig(id_array[y][i], fill='tomato')
    # вертикальная прямая
    elif x0 == x1:
        x = x0
        for i in range(min(y0, y1), max(y0, y1) + 1):
            canvas.itemconfig(id_array[i][x], fill='tomato')
    # кривая
    else:
        if x0 > x1:
            x1, x0 = x0, x1
            y1, y0 = y0, y1

        delta_x = 1 if abs(x1 - x0) == 0 else abs(x1 - x0)
        delta_y = abs(y1 - y0)

        error = 0

        up_or_down = y1 - y0
        if up_or_down > 0:
            up_or_down = 1
        elif up_or_down < 0:
            up_or_down = -1
        else:
            up_or_down = 0

        if delta_y <= delta_x:
            delta_error = delta_y / delta_x
            y = y0
            for x in range(x0, x1 + 1):
                canvas.itemconfig(id_array[y][x], fill='tomato')
                error += delta_error
                if error >= 0.5:
                    y += up_or_down
                    error -= 1
        else:
            delta_error = delta_x / delta_y
            if y0 > y1:
                x1, x0 = x0, x1
                y1, y0 = y0, y1
            x = x0
            for y in range(y0, y1 + 1):
                canvas.itemconfig(id_array[y][x], fill='tomato')
                error += delta_error
                if error >= 0.5:
                    x += up_or_down
                    error -= 1
    return []


def left_click(event, id_array):
    global coords
    col_coord = event.x // w - 1
    row_coord = event.y // w - 1
    if 0 <= row_coord < len(id_array) and 0 <= col_coord < len(id_array[0]):
        if not coords:
            for i in range(len(id_array)):
                for j in range(len(id_array[0])):
                    canvas.itemconfig(id_array[i][j], fill='blue')
        coords.append([col_coord, row_coord])
        canvas.itemconfig(id_array[row_coord][col_coord], fill='tomato')
    if len(coords) == 2:
        canvas.itemconfig(id_array[coords[0][1]][coords[0][0]], fill='blue')
        canvas.itemconfig(id_array[coords[1][1]][coords[1][0]], fill='blue')
        coords = print_line(coords, id_array)


# размеры поля из квадратиков
w, row, col = 20, 11, 11

# создание окна
tk = Tk()
tk.title('кодировка')
tk.geometry(f'{w * (row + 2)}x{w * (col + 2)}+600+200')
canvas = Canvas(tk, width=500, height=500)
canvas.pack()

coords = []
id_array = create_field(row, col, w)

# создание кнопок
tk.bind('<Button-1>', lambda event: left_click(event, id_array))
tk.mainloop()
