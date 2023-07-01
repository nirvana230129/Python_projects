"""
1 рисует поле
2 первый игрок ставит корабли
3 второй игрок ставит корабли
4 игрроки поочериди делают ходы
5 после каждого хода закрашивается клетка в бежевый(мимо), фиолетовый(ранил),
  красный(убил) цвета
6 после уничтожения корабля вокруг него ставятся бежевые клетки
7 после уничтожения всех кораблей одного из игроков выводится надпись "победил игрок 1(2)"
8 далее не воспринимаются никакие действия, кроме закрытия окна
"""

from tkinter import *


# создание синего поля и заполнение массива id-шниками
def create_field(w, rows, cols, indent, color):
    array = []
    for i in range(rows):
        array.append([])
        for j in range(cols):
            array[i].append(canvas.create_rectangle(20+j*w+indent,
                                                    20+i*w,
                                                    20+(j+1)*w+indent,
                                                    20+(i+1)*w,
                                                    fill=color))
            tk.update()
    return array


#
def pick(event, turn, square_side, id_array_l, id_array_r, changeColor:bool):
    """
    Получает на вход: чей ход, сторону клетки, массивы с id левого и правого полей, сьрасывать ли цвет
    В зависсимости от хода подсвечивает нажатую клетку
    """
    global picked_cell, isChange 
    
    isChange = False 
    
    col_coord = event.x//square_side-1  # определяет номер клетки х
    row_coord = event.y//square_side-1  # определяет номер клетки у

    if turn == 1:  # если ход первого игрока
        if 0 <= col_coord < len(id_array_l) and 0 <= row_coord < len(id_array_l[0]):
            # проверка на принадлежность клетки к полю
            print('Pick next')
            print('ход игрока номер 1, клетка попадает на поле игрока 1')
            if changeColor:
                canvas.itemconfig(id_array_l[picked_cell[1]][picked_cell[0]], fill='blue')
                # перекрашивает старую выбранную клетку в цвет поля
            canvas.itemconfig(id_array_l[row_coord][col_coord], fill='cyan')
            # перекрашивает новую выбранную клетку в нужный цвет
            picked_cell = [col_coord, row_coord]  # выбирает новую клетку
            isChange = True 
            print('Выбранная клетка', *picked_cell)
            print('Pick final''\n')
        else:
            print('мимо, ход игрока 1,', 'col', col_coord, 'row', row_coord)

    elif turn == 2:  # если ход второго игрока
        col_coord -= 12  # вычитаем из х 12, тк второе поле правее на 12
        if 0 <= col_coord < len(id_array_l) and 0 <= row_coord < len(id_array_l[0]):
            # проверка на принадлежность клетки к полю
            print('Pick next')
            print('ход игрока номер 2, клетка попадает на поле игрока 2')
            # print('picked_cell', picked_cell)
            if changeColor:
                canvas.itemconfig(id_array_r[picked_cell[1]][picked_cell[0]], fill='orange') 
                # перекрашивает старую выбранную клетку в цвет поля
            canvas.itemconfig(id_array_r[row_coord][col_coord], fill='yellow') 
            # перекрашивает новую выбранную клетку в нужный цвет
            picked_cell = [col_coord, row_coord]  # выбирает новую клетку
            isChange = True 
            print('Выбранная клетка', *picked_cell)
            print('Pick final')
        else:
            print('мимо, ход игрока 2,', 'col', col_coord, 'row', row_coord)


def change_turn():
    global turn, isChange
    if isChange:
        turn += 1
        if turn == 3:
            turn = 1
        print('\n''Смена хода''\n''\n')
        isChange = False 


def ships_creating(id_array_l, id_array_r, square_side):
    global ships_field_l, ships_field_r
    for i in range(20):
        #pick(event, 1, square_side, id_array_l, id_array_r, False)
        ships_field_l[picked_cell[0]][picked_cell[1]] = 1
        

# размеры поля из квадратиков 
row, col = 10, 10
square_side = 20

ships_field_l = [[0]*row for i in range(col)]
ships_field_r = [[0]*row for i in range(col)]

# создание окна
tk = Tk()
tk.title('Морской бой')
tk.resizable(0, 0)
canvas = Canvas(tk, width=(row+2)*square_side*2, height=(col+2)*square_side*2)
canvas.pack()

canvas.create_text(10, 300, fill='black', anchor='w', text="У каждого игрока должны быть \
расставлены 10 кораблей:""\n""4 по 1 клетке;""\n""3 по 2 клетки;""\n""2 по 3 клетки;""\n""\
1 - 4 клетки.""\n""Сначала игрок 1 расставляет свои корабли, потом свои расставляет""\n""\
игрок 2. Далее, ироки по очереди стреляют по полю противника. Если""\n""игрок попадает по \
кораблю, следующий выстрел делает опять он.")

id_array_l = create_field(square_side, row, col, 0, 'blue')
id_array_r = create_field(square_side, row, col, square_side * (row+2), 'orange')

turn = 1

picked_cell = [0, 0]
isChange = False 

# клавиши
tk.bind('<Button-1>', lambda event: pick(event, turn, square_side, id_array_l, id_array_r, True))
tk.bind('<Return>', lambda event: change_turn())

tk.mainloop()
