class Maze(object):
    # Cell class to be populated into maze array
    class Cell(object):
        def __init__(self, ceil="+---", lwall="|", rwall="", floor="", center=" ? "):
            self.ceil = ceil
            self.lwall = lwall
            self.rwall = rwall
            self.floor = floor
            self.center = center

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.cells = [[self.Cell() for column in range(self.columns + 1)] for row in range(self.rows + 1)]
        self.cursor = [0, 0]
        self.build()
        # Sets [0, 0] as visited
        self.cells[self.cursor[0]][self.cursor[1]].center = "   "

    def __str__(self):
        output = ""
        for row in range(self.rows):
            for line in range(3):
                if line == 0:
                    for column in range(self.columns):
                        output += self.cells[row][column].ceil
                    output += "\n"
                elif line == 1:
                    for column in range(self.columns):
                        output += self.cells[row][column].lwall + self.cells[row][column].center \
                                + self.cells[row][column].rwall
                    output += "\n"
                elif line == 2:
                    for column in range(self.columns):
                        output += self.cells[row][column].floor
        return output

    # Initializes cell matrix to include proper floors, ceilings, and right-walls
    def build(self):
        for row in range(self.rows):
            for column in range(self.columns):
                if column != self.columns - 1:
                    if row == self.rows - 1:
                        self.cells[row][column] = self.Cell(floor="+---")
                else:
                    if row != self.rows - 1:
                        self.cells[row][column] = self.Cell(ceil="+---+", rwall="|")
                    else:
                        self.cells[row][column] = self.Cell(ceil="+---+", floor="+---+", rwall="|")

    # Breaks the wall between the cursor's current position and the parameter cell's position
    # Note: Breaks the wall closest to the destination/parameter cell, and can break multiple walls
    def break_wall(self, cell_pos):
        try:
            # Break the ceiling of the cell below the cell at cell_pos
            # We can only break the ceilings because floors are strictly used for the bottom of the maze
            if cell_pos[0] < self.cursor[0]:
                self.cells[cell_pos[0] + 1][cell_pos[1]].ceil = "+   "
                if cell_pos[1] == self.columns - 1:
                    self.cells[cell_pos[0] + 1][cell_pos[1]].ceil = "+   +"
            # Break the ceiling of the cell at cell_pos
            if cell_pos[0] > self.cursor[0]:
                self.cells[cell_pos[0]][cell_pos[1]].ceil = "+   "
                if cell_pos[1] == self.columns - 1:
                    self.cells[cell_pos[0]][cell_pos[1]].ceil = "+   +"
            # Break the left wall of the cell to the right of the cell at cell_pos
            # We can only break left walls because right walls are strictly used for the rightmost side of the maze
            if cell_pos[1] < self.cursor[1]:
                self.cells[cell_pos[0]][cell_pos[1] + 1].lwall = " "
            # Break the left wall of the cell at cell_pos
            if cell_pos[1] > self.cursor[1]:
                self.cells[cell_pos[0]][cell_pos[1]].lwall = " "
        except TypeError:
            print("ERROR: Invalid coordinate given for break_wall function.")

    # Shifts the cursor to a new [x, y] coordinate position
    # Returns True if the cursor location has been changed and False otherwise
    def shift_cursor(self, new_pos):
        try:
            if self.shift_check(new_pos):
                # Check to make sure new_pos is not out of bounds
                self.cursor = new_pos
                self.cells[self.cursor[0]][self.cursor[1]].center = "   "
        except ValueError:
            print("ERROR: Invalid coordinate given for shift_cursor function.")

    def shift_check(self, new_pos):
        if new_pos[0] < 0 or new_pos[0] > self.rows or new_pos[1] < 0 or new_pos[1] > self.columns:
            return False
        return True

    # Directional functions that return the coordinate position relative to the cursor
    def up(self):
        return [self.cursor[0] - 1, self.cursor[1]]

    def down(self):
        return [self.cursor[0] + 1, self.cursor[1]]

    def left(self):
        return [self.cursor[0], self.cursor[1] - 1]

    def right(self):
        return [self.cursor[0], self.cursor[1] + 1]

    # Convenience functions that break the wall in the chosen direction and shift the cursor without having to declare
    # each on separate lines
    def move_up(self):
        if self.shift_check(self.up()):
            self.break_wall(self.up())
            self.shift_cursor(self.up())

    def move_down(self):
        if self.shift_check(self.down()):
            self.break_wall(self.down())
            self.shift_cursor(self.down())

    def move_left(self):
        if self.shift_check(self.left()):
            self.break_wall(self.left())
            self.shift_cursor(self.left())

    def move_right(self):
        if self.shift_check(self.right()):
            self.break_wall(self.right())
            self.shift_cursor(self.right())

    # Returns true if the given cell position has been visited by the cursor and false otherwise
    def visited(self, cell_pos):
        if self.shift_check(cell_pos) and self.cells[cell_pos[0]][cell_pos[1]].center != " ? ":
            return True
        return False


if __name__ == '__main__':
    newMaze = Maze(6, 8)

    newMaze.move_right()
    print(str(newMaze.cursor))
    if newMaze.cells[-1][0] is not None:
        print("Cell exists at -1, 0")

    print(newMaze)
    print("\nHas cell [0, 0] been visited? " + str(newMaze.visited([0, 0])))
    print("Has cell [5, 5] been visited? " + str(newMaze.visited([5, 5])))
