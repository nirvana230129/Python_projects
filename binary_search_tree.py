from tkinter import Tk, Canvas, Entry, Button, messagebox
from time import sleep


class Node:
    def __init__(self, canvas, x, y, value, radius=20, height=0, parent=None, left_child=None, left_child_line=None,
                 right_child_line=None, right_child=None):
        self.x = x
        self.y = y
        self.radius = radius

        self.id = canvas.create_oval(x - radius,
                                     y - radius,
                                     x + radius,
                                     y + radius,
                                     fill='cyan',
                                     outline='blue',
                                     width=radius // 10)
        self.text_id = canvas.create_text(x, y, text=str(value), fill='blue',
                                          font=f'Verdana {[15, 15, 15, 15, 15, 12, 9][min(6, len(str(value)))]}')

        self.value = value
        self.height = height

        self.parent = parent

        self.left_child = left_child
        self.left_child_line = left_child_line

        self.right_child = right_child
        self.right_child_line = right_child_line


class BinarySearchTree:
    def __init__(self, canvas):
        self.root = None
        self.canvas: Canvas = canvas
        self.plus_y = 130
        self.selected = None

    def move_node(self, node1: Node, node2: Node, temp_col_ol: str, temp_w: int, normal_col: tuple, selected_col: tuple,
                  return_color=True):
        temporal = self.canvas.create_oval(node2.x - node1.radius + temp_w / 2,
                                           node2.y - node1.radius + temp_w / 2,
                                           node2.x + node1.radius - temp_w / 2,
                                           node2.y + node1.radius - temp_w / 2,
                                           outline=temp_col_ol,
                                           width=temp_w)
        if return_color:
            self.canvas.itemconfig(node1.id, fill=normal_col[0], outline=normal_col[1])
        self.canvas.update()

        difference_x = node2.x - node1.x
        difference_y = node2.y - node1.y
        distance = (difference_x ** 2 + difference_y ** 2) ** 0.5

        cnt = int(0.536 * distance)

        x = []
        y = []

        for i in range(1, cnt + 1):
            x.append(node1.x + difference_x / cnt * i)
            y.append(node1.y + difference_y / cnt * i)

        for i in range(cnt):
            self.canvas.coords(temporal,
                               x[i] - node2.radius,
                               y[i] - node2.radius,
                               x[i] + node2.radius,
                               y[i] + node2.radius)
            self.canvas.update()
            sleep(0.005)

        self.canvas.itemconfig(node2.id, fill=selected_col[0], outline=selected_col[1])
        self.canvas.delete(temporal)
        self.canvas.update()

    def create_line(self, node: Node, height, coef):
        line_id = self.canvas.create_line(node.x, node.y, node.x + coef * (350 / 2 ** height), node.y + self.plus_y,
                                          width=3, fill='black')
        self.canvas.lower(line_id)
        return line_id

    def raise_subtree(self, node: Node):
        ...

    def search(self, value):
        if self.root is not None:
            return self._search(value, self.root)
        return None

    def _search(self, value, cur_node: Node):
        if cur_node is None:
            return False
        if cur_node.value == value:
            return True
        if cur_node.value > value:
            return self._search(value, cur_node.left_child)
        return self._search(value, cur_node.right_child)

    def insert(self, value):
        if self.root is None:
            self.root = Node(self.canvas, 715, 50, value)
        else:
            self._insert(value, self.root)

    def _insert(self, value, cur_node: Node, height=0):
        if height >= 5:
            messagebox.showinfo("####", 'The fucking tree is already too long! what the fuck do you want from him?')
            return
        dif = 350 / 2 ** height
        if value < cur_node.value:
            if cur_node.left_child is None:
                cur_node.left_child_line = self.create_line(cur_node, height, -1)
                cur_node.left_child = Node(self.canvas, cur_node.x - dif,
                                           cur_node.y + self.plus_y, value,
                                           height=height, parent=cur_node)
            else:
                self._insert(value, cur_node.left_child, height + 1)
        elif value > cur_node.value:
            if cur_node.right_child is None:
                cur_node.right_child_line = self.create_line(cur_node, height, 1)
                cur_node.right_child = Node(self.canvas, cur_node.x + dif,
                                            cur_node.y + self.plus_y, value,
                                            height=height, parent=cur_node)
            else:
                self._insert(value, cur_node.right_child, height + 1)
        else:
            messagebox.showinfo("####", 'This fucking knot is already in the fucking tree, asshole!')

    def search_with_drawing(self, value):
        if self.selected is not None:
            self.canvas.itemconfig(self.selected.id, fill='cyan', outline='blue')
        if self.root is not None:
            self.canvas.itemconfig(self.root.id, fill='orange', outline='red')
            self._search_with_drawing(value, self.root)
        else:
            messagebox.showinfo("####", 'Are you a dumbass? The tree is empty!')

    def _search_with_drawing(self, value, cur_node: Node):
        if cur_node is None:
            messagebox.showinfo("####", 'The element is not in the tree.')
            return False

        if cur_node.value == self.root.value:
            self.canvas.itemconfig(cur_node.id, fill='orange', outline='red')
            self.canvas.update()
            sleep(0.3)
        else:
            sleep(0.3)
            self.move_node(cur_node.parent, cur_node, 'red', 4, ('cyan', 'blue'), ('orange', 'red'))

        if value == cur_node.value:
            self.canvas.itemconfig(cur_node.id, fill='darkorchid', outline='navy')
            self.selected = cur_node
            messagebox.showinfo("####", 'The element is in the tree.')
            return True
        elif value < cur_node.value:
            search_left = self._search_with_drawing(value, cur_node.left_child)
            if not search_left:
                self.canvas.itemconfig(cur_node.id, fill='cyan', outline='blue')
        else:
            search_right = self._search_with_drawing(value, cur_node.right_child)
            if not search_right:
                self.canvas.itemconfig(cur_node.id, fill='cyan', outline='blue')

    def delete(self, value):
        if self.selected is not None:
            self.canvas.itemconfig(self.selected.id, fill='cyan', outline='blue')
        if self.root is not None:
            if self.search(value):
                self.canvas.itemconfig(self.root.id, fill='orange', outline='red')
                self._delete(value, self.root)
        else:
            messagebox.showinfo("####", 'Are you a dumbass? The tree is empty!')

    def _delete(self, value, cur_node: Node):
        if cur_node.value == self.root.value:
            self.canvas.itemconfig(cur_node.id, fill='orange', outline='red')
            self.canvas.update()
            sleep(0.3)
        else:
            sleep(0.7)
            self.move_node(cur_node.parent, cur_node, 'red', 4, ('cyan', 'blue'), ('orange', 'red'))

        if value == cur_node.value:
            self.canvas.itemconfig(cur_node.id, fill='red', outline='darkred')
            sleep(0.6)
            self.canvas.update()

            if cur_node.left_child is not None:
                new_node: Node = cur_node.left_child
                sleep(0.3)
                self.move_node(cur_node, new_node, 'darkred', 4, ('cyan', 'blue'), ('orange', 'red'), False)
                while new_node.right_child is not None:
                    sleep(0.3)
                    self.move_node(new_node, new_node.right_child, 'darkred', 4, ('cyan', 'blue'), ('orange', 'red'))
                    new_node: Node = new_node.right_child

                if new_node.left_child is not None:
                    ...
            elif cur_node.right_child is not None:
                new_node = cur_node.right_child
                self.move_node(cur_node, new_node, 'darkred', 4, ('cyan', 'blue'), ('orange', 'red'), False)
            else:
                ...

        elif value < cur_node.value:
            self._delete(value, cur_node.left_child)
        else:
            self._delete(value, cur_node.right_child)


class Window:
    def __init__(self, name='Binary Search Tree'):
        self.tk = Tk()
        self.tk.title(name)
        self.tk.geometry('1430x750')
        self.tk.resizable(False, False)

        self.canvas: Canvas = Canvas(self.tk, width=1430, height=750)
        self.canvas.pack()

        self.binary_tree = BinarySearchTree(self.canvas)

        self.add_node_entry = Entry(self.tk, width=5)
        self.add_node_entry.place(x=1280, y=15)
        self.add_node_button = Button(self.tk, text='Add', command=lambda: self.add_node())
        self.add_node_button.place(x=1340, y=15)

        self.search_node_entry = Entry(self.tk, width=5)
        self.search_node_entry.place(x=1280, y=50)
        self.search_node_button = Button(self.tk, text='Search', command=lambda: self.search_node())
        self.search_node_button.place(x=1340, y=50)

        self.delete_node_entry = Entry(self.tk, width=5)
        self.delete_node_entry.place(x=1280, y=85)
        self.delete_node_button = Button(self.tk, text='Delete', command=lambda: self.delete_node())
        self.delete_node_button.place(x=1340, y=85)

    def add_node(self):
        new = self.add_node_entry.get()
        for i in new:
            if i not in '0123456789.-+':
                messagebox.showinfo("####", "It's not the number you fucking idiot!")
                break
        else:
            if new.count('.') > 1 or '+' in new[1:] or '-' in new[1:] or not new:
                messagebox.showinfo("####", "It's not the number you fucking idiot!")
            elif new.count('.') == 0:
                self.binary_tree.insert(int(new))
            elif new.count('.') == 1:
                new = float(new)
                self.binary_tree.insert(int(new) if int(new) == new else new)

    def search_node(self):
        searching = self.search_node_entry.get()
        for i in searching:
            if i not in '0123456789.-+':
                messagebox.showinfo("####", "It's not the number you fucking idiot!")
                break
        else:
            if searching.count('.') > 1 or '+' in searching[1:] or '-' in searching[1:] or not searching:
                messagebox.showinfo("####", "It's not the number you fucking idiot!")
            elif searching.count('.') == 0:
                self.binary_tree.search_with_drawing(int(searching))
            elif searching.count('.') == 1:
                searching = float(searching)
                self.binary_tree.search_with_drawing(int(searching) if int(searching) == searching else searching)

    def delete_node(self):
        self.delete_node_entry.get()
        messagebox.showinfo("Dear User!", "You don't have to do this! I'm serious! You do not have to!")


w = Window()
w.tk.mainloop()
