from tkinter import *
from time import sleep


# создание синего поля и заполнение массива id
def create_field(row, col, delay, w):
    array = []
    for i in range(row):
        array.append([])
        for j in range(col):
            array[i].append(canvas.create_rectangle(w + j * w,
                                                    w + i * w,
                                                    w + (j + 1) * w,
                                                    w + (i + 1) * w,
                                                    fill='blue'))
            sleep(delay)
            tk.update()
    return array


def f1(row, col, id_array, delay):
    for i in range(row):
        for j in range(col):
            canvas.itemconfig(id_array[i][j], fill='orange')
            sleep(delay)
            tk.update()


def f2(row, col, id_array, delay):
    i = 0
    while i < row:
        for j in range(col):
            canvas.itemconfig(id_array[i][j], fill='purple')
            sleep(delay)
            tk.update()
        i += 1

        if i == row:
            break

        for j in range(col - 1, -1, -1):
            canvas.itemconfig(id_array[i][j], fill='purple')
            sleep(delay)
            tk.update()
        i += 1


def f3(row, col, id_array, delay):
    i = row - 1
    while i >= 0:
        if i == row:
            break
        for j in range(col - 1, -1, -1):
            canvas.itemconfig(id_array[i][j], fill='red')
            sleep(delay)
            tk.update()
        i -= 1

        if i < 0:
            break

        for j in range(col):
            canvas.itemconfig(id_array[i][j], fill='red')
            sleep(delay)
            tk.update()
        i -= 1


def f4(row, col, id_array, delay):
    j = 0
    while j < col:
        for i in range(row):
            canvas.itemconfig(id_array[i][j], fill='green')
            sleep(delay)
            tk.update()
        j += 1

        if j == col:
            break

        for i in range(row - 1, -1, -1):
            canvas.itemconfig(id_array[i][j], fill='green')
            sleep(delay)
            tk.update()
        j += 1


def f5(row, col, id_array, delay):
    j = col - 1
    while j >= 0:
        for i in range(row - 1, -1, -1):
            canvas.itemconfig(id_array[i][j], fill='pink')
            sleep(delay)
            tk.update()
        j -= 1

        if j < 0:
            break

        for i in range(row):
            canvas.itemconfig(id_array[i][j], fill='pink')
            sleep(delay)
            tk.update()
        j -= 1


# размеры поля из квадратиков
r, c, w = 10, 10, 20
delay = 0.01

# создание окна
tk = Tk()
tk.title('Квадратики')
tk.geometry('250x350+600+200')
canvas = Canvas(tk, width=500, height=500)
canvas.pack()

id_ar = create_field(r, c, delay, w)

# создание кнопок
btn = Button(tk, text='f1', command=lambda: f1(r, c, id_ar, delay))
btn.place(x=35, y=250)
btn2 = Button(tk, text='f2', command=lambda: f2(r, c, id_ar, delay))
btn2.place(x=97, y=250)
btn3 = Button(tk, text='f3', command=lambda: f3(r, c, id_ar, delay))
btn3.place(x=160, y=250)
btn4 = Button(tk, text='f4', command=lambda: f4(r, c, id_ar, delay))
btn4.place(x=66, y=285)
btn5 = Button(tk, text='f5', command=lambda: f5(r, c, id_ar, delay))
btn5.place(x=128, y=285)

tk.mainloop()
