from tkinter import Tk, BOTH, Canvas
import random


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("test")
        self.canvas = Canvas(self.__root, width=width, height=height)
        self.canvas.pack()
        self.running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)

    def animate(self, time):
        self.__root.after(time, self.redraw())
        
    def redraw(self):
        self.__root.update()
        self.__root.update_idletasks

    def wait_for_close(self):
        self.running = True
        while self.running is True:
            self.redraw()

    def close(self):
        self.running = False


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    

class Line:
    def __init__(self, pt1, pt2):
        self.pt1 = pt1
        self.pt2 = pt2

    def draw(self, canvas, fill_color):
        canvas.create_line(self.pt1.x, self.pt1.y, self.pt2.x, self.pt2.y, fill=fill_color, width=2)
        canvas.pack()



class Cell:
    def __init__(self, x1, y1, x2, y2, win, visited=False, top=True, btm=True, left=True, right=True):
        self.walls = {'top': top, 'btm': btm, 'left': left, 'right': right}
        self.visited = visited
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.win = win

    def draw(self):
        pt1 = Point(self.x1, self.y1)
        pt2 = Point(self.x2, self.y1)
        pt3 = Point(self.x1, self.y2)
        pt4 = Point(self.x2, self.y2)
        t = Line(pt1, pt2)
        b = Line(pt3, pt4)
        l = Line(pt1, pt3)
        r = Line(pt2, pt4)

        for wall in self.walls:
            if self.walls[wall] is True:
                if wall == 'top':
                    self.win.draw_line(t, 'red')
                if wall == 'btm':
                    self.win.draw_line(b, 'red')
                if wall == 'left':
                    self.win.draw_line(l, 'red')    
                if wall == 'right':
                    self.win.draw_line(r, 'red')

    def draw_move(self, to_cell, undo=False):
        
        cur_middle_coords = Point((self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2)
        new_middle_coords = Point((to_cell.x1 + to_cell.x2) // 2, (to_cell.y1 + to_cell.y2) // 2)
        self.win.draw_line(Line(cur_middle_coords, new_middle_coords), 'black')


class Maze:
    def __init__(self, 
                 x1, 
                 y1, 
                 num_rows, 
                 num_cols, 
                 cell_size_x, 
                 cell_size_y, 
                 win
                 ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.create_cells()


    def create_cells(self):
        self.cells = []
        for i in range(0, self.num_cols):
            for j in range(0, self.num_rows):
                self.cells.append(Cell(self.x1 + j * self.cell_size_x, 
                                        self.y1 + i * self.cell_size_y, 
                                        self.x1 + (j + 1) * self.cell_size_x, 
                                        self.y1 + (i + 1) * self.cell_size_y, 
                                        self.win))
        self.cells[0].walls['top'] = False
        self.cells[-1].walls['btm'] = False
        for cell in self.cells:
            cell.draw()
            self.win.animate(10)
            
    def break_entrance_exit(self):
        self.cells[0].walls['top'] = False
        self.cells[-1].walls['btm'] = False


    def break_walls_r(self, i, j):
        cell = self.cells[i]
        cell.visited = True

        possible_walls = [i - self.num_rows, i + self.num_rows, i - 1, i + 1]

        while True:

            pass


def main():
    win = Window(800, 600)
    Maze(5, 5, 10, 12, 30, 30, win)


    win.wait_for_close()


main()


