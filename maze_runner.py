from structures.stack.arraystack import ArrayStack
from structures.list.linkedlist import LinkedList
from maze import Maze
from time import sleep
import random
import os

if __name__ == '__main__':
    """ Uses Maze class and ArrayStack class and generates a randomized path """
    # clear console screen
    clear = lambda: os.system('cls')

    # asks user for amount of rows, amount of columns, and the speed at which the maze will generate
    rows = input("How many rows will the maze contain? ")
    columns = input("How many columns will the maze contain? ")
    speed = input("How fast should the maze go? ")

    # initialize stack, list, and maze
    stack = ArrayStack()
    neighbors = LinkedList()
    maze = Maze(int(rows), int(columns))

    # sets window size to appropriate length and width
    os.system('mode con: cols={} lines={}'.format(maze.columns * 4 + 2, maze.rows * 2 + 4))

    # choose initial cell, mark visited, and push onto stack
    cursor = maze.cursor
    stack.push(cursor)

    while not stack.isEmpty():
        neighbors.clear()

        # the current cell/cursor position
        maze.cursor = stack.pop()

        # if the cell in the direction of the currently selected cell exists and if it has not been visited
        if maze.up()[0] >= 0 and not maze.visited(maze.up()):
            neighbors.add(maze.up())
        if maze.down()[0] < maze.rows and not maze.visited(maze.down()):
            neighbors.add(maze.down())
        if maze.left()[1] >= 0 and not maze.visited(maze.left()):
            neighbors.add(maze.left())
        if maze.right()[1] < maze.columns and not maze.visited(maze.right()):
            neighbors.add(maze.right())

        if len(neighbors) > 0:
            # push the current cell back to the stack
            stack.push(maze.cursor)

            # select random neighbor
            neighbor = neighbors[random.randint(0, len(neighbors) - 1)]

            if maze.up() == neighbor:
                maze.move_up()
            elif maze.down() == neighbor:
                maze.move_down()
            elif maze.right() == neighbor:
                maze.move_right()
            elif maze.left() == neighbor:
                maze.move_left()

            stack.push(neighbor)

            # draw the current frame of the maze to the screen and pause for a fraction of a second
            sleep(.01 / float(speed))
            clear()
            print(maze)

    # opens walls for each end of the maze
    maze.cells[0][0].ceil = "+   "
    maze.cells[maze.rows - 1][maze.columns - 1].floor = "+   +"
    maze.cells[maze.rows - 1][maze.columns - 1].center = "   "
    clear()
    print(maze)

    input("\nMaze complete!")
