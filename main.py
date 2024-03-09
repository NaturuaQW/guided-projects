from tkinter import Tk, BOTH, Canvas
import random



class Window:
    def __init__ (self, width, height):
        self.root = Tk()
        self.root.title("Test")
        self.canvas = Canvas(self.root, width=width, height=height, bg='white')
        self.canvas.pack()
        self.win = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)
    
    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def animate(self, time):
        self.root.after(time, self.redraw())

    def wait_for_close(self):
        self.win = True

        while self.win is True:
            self.redraw()

    def close(self):
        self.win = False
        
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
    def __init__(self, _x1, _y1, _x2, _y2, _win, i=0, j=0):
        self.x1 = _x1
        self.y1 = _y1
        self.x2 = _x2
        self.y2 = _y2
        self.coord = (i, j)
        self.win = _win
        self.visited = False

        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True

    def draw(self):
        pt1 = Point(self.x1, self.y1)
        pt2 = Point(self.x2, self.y1)
        pt3 = Point(self.x1, self.y2)
        pt4 = Point(self.x2, self.y2)



        l = Line(pt1, pt3)
        r = Line(pt2, pt4)
        t = Line(pt1, pt2)
        b = Line(pt3, pt4)
        

        if self.has_left_wall is True:
            self.win.draw_line(l, 'black')
        else:
            self.win.draw_line(l, 'white')
        if self.has_right_wall is True:
            self.win.draw_line(r, 'black')
        else:
            self.win.draw_line(r, 'white')
        if self.has_top_wall is True:
            self.win.draw_line(t, 'black')
        else:
            self.win.draw_line(t, 'white')
        if self.has_bottom_wall is True:
            self.win.draw_line(b, 'black')
        else:
            self.win.draw_line(b, 'white')

    def draw_move(self, to_cell, undo=False):
        cur_middle_coords = Point((self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2)
        new_middle_coords = Point((to_cell.x1 + to_cell.x2) // 2, (to_cell.y1 + to_cell.y2) // 2)
        if undo is False:
            self.win.draw_line(Line(cur_middle_coords, new_middle_coords), 'red')
        else:
            self.win.draw_line(Line(cur_middle_coords, new_middle_coords), 'white')



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
        self._break_walls_r()
        self.count_visited()
        self._reset_cells_visited()
        self.solve((0, 0))
        
        

    def create_cells(self):
        self.cells = {}
        for j in range(0, self.num_cols):
            for i in range(0, self.num_rows):
                self.cells[(i, j)] = (Cell(self.x1 + i * self.cell_size_x, 
                                        self.y1 + j * self.cell_size_y, 
                                        self.x1 + (i + 1) * self.cell_size_x, 
                                        self.y1 + (j + 1) * self.cell_size_y, 
                                        self.win, 
                                        i, 
                                        j))

        for coord, cell in self.cells.items():
            if coord == (0, 0):
                cell.has_top_wall = False

            if coord == (self.num_rows - 1, self.num_cols - 1):
                cell.has_bottom_wall =False

            cell.draw()
            self.win.animate(10)

    def _break_walls_r(self):
        current_cell = (0, 0)
        target_cell = (self.num_rows - 1, self.num_cols - 1)
        visited_cells = []
        while True:
            self.cells[current_cell].visited = True
            if current_cell not in visited_cells:
                visited_cells.append(current_cell)
            directions = {}
            directions['top'] = (current_cell[0], current_cell[1] - 1)
            directions['bottom'] = (current_cell[0], current_cell[1] + 1)
            directions['left'] = (current_cell[0] - 1, current_cell[1])
            directions['right'] = (current_cell[0] + 1, current_cell[1])
            
            not_visited = []
            for dir, coord in directions.items():
                if coord in self.cells:
                    if self.cells[coord].visited is False:
                        not_visited.append(dir)

            if not not_visited:
                if self.count_visited() == (self.num_cols * self.num_rows):
                    break
                current_cell = visited_cells[random.randint(0, len(visited_cells) - 1)]

            else:
                move_to = not_visited[random.randint(0, len(not_visited) - 1)]
                to_remove = 'has_' + move_to + "_wall"
                setattr(self.cells[current_cell], to_remove, False)

                current_cell = directions[move_to]

                if move_to == 'top':
                    move_to = 'bottom'
                    to_remove = 'has_' + move_to + "_wall"
                    setattr(self.cells[current_cell], to_remove, False)
                elif move_to == 'bottom':
                    move_to = 'top'
                    to_remove = 'has_' + move_to + "_wall"
                    setattr(self.cells[current_cell], to_remove, False)
                elif move_to == 'right':
                    move_to = 'left'
                    to_remove = 'has_' + move_to + "_wall"
                    setattr(self.cells[current_cell], to_remove, False)
                elif move_to == 'left':
                    move_to = 'right'
                    to_remove = 'has_' + move_to + "_wall"
                    setattr(self.cells[current_cell], to_remove, False)

        for coord, cell in self.cells.items():
            cell.draw()
            self.win.animate(10)

    def count_visited(self):
        counter = 0
        for coord, cell in self.cells.items():
            if cell.visited is True:
                counter += 1
        print(counter)
        return counter

    def _reset_cells_visited(self):
        for coord, cell in self.cells.items():
            cell.visited = False
        self.count_visited()

    def solve(self, current_coord):
        self.win.animate(10)
        self.cells[current_coord].visited = True
        target_cell = (self.num_rows - 1, self.num_cols - 1)
        if target_cell == current_coord:
            return True
        directions = {}
        directions['top'] = (current_coord[0], current_coord[1] - 1)
        directions['bottom'] = (current_coord[0], current_coord[1] + 1)
        directions['left'] = (current_coord[0] - 1, current_coord[1])
        directions['right'] = (current_coord[0] + 1, current_coord[1])
        for dir, coord in directions.items():
            cur_dir = 'has_' + dir + "_wall"
            
            if coord[0] >= 0 and coord[1] >= 0:    
                if getattr(self.cells[current_coord], cur_dir) is False and self.cells[coord].visited is False:
                    
                    self.cells[current_coord].draw_move(self.cells[coord])
                    if self.solve(coord) is True:
                        return True
                    else:
                        self.cells[current_coord].draw_move(self.cells[coord], True)

        return False




#============= Main ===============

def main():
    win = Window(800, 600)
    x = Maze(5, 5, 20, 15, 30, 30, win)
    

    #print(x.cells)


    win.wait_for_close()


#main()
