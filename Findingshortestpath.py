# Imports
import queue
import random


def print_grid(g):
    """
    Function to print the grid

    Args:
        g (2D array): The grid which will be printed
    """
    for arr in g:
        print()
        print(*arr, sep="    ")
    print()


def grid_generator(grid_size, n_carrots, n_holes):
    """
    Generates the grid

    Args:
        grid_size (int): It is the length and the width of the grid
        n_carrots (int): The number of carrots
        n_holes (int): The number of holes

    Returns:
        grid (2D list): The grid
        x_r: The x cord of rabbit
        y_r: The y cord of rabbit
    """
    # Check if the entered values match the guidlines
    # while True:
    #     # If the user entered 0 carrots
    #     if n_carrots < 2:
    #         print("Please enter 2 or more carrots")
    #         n_carrots = int(input("Enter number of carrots: "))
    #     # If the user entered 0 holes
    #     elif n_holes < 2:
    #         print("Please enter 2 or more holes")
    #         n_holes = int(input("Enter number of holes: "))
    #     # If It matches the guidlines
    #     elif n_carrots + n_holes < grid_size * grid_size and grid_size >= 10:
    #         break
    #     # If the grid_size is too small
    #     elif grid_size < 10:
    #         print("The grid size is too small please enter minimum of 10")
    #         grid_size = int(input("Enter grid size: "))
    #     # If the carrots and the holes don't fit in the given grid
    #     elif n_carrots + n_holes >= grid_size * grid_size:
    #         print(
    #             "There are too many carrots and holes for the given board. Please reduce the number of carrots and number of holes"
    #         )
    #         n_carrots = int(input("Enter number of carrots: "))
    #         n_holes = int(input("Enter number of holes: "))

    grid = []  # The grid
    x_c = []  # x cords of carrots
    y_c = []  # y cords of carrots
    x_h = []  # x cords of holes
    y_h = []  # y cords of holes
    x_r = random.randint(0, grid_size - 1)  # x cord of rabbit
    y_r = random.randint(0, grid_size - 1)  # y cord of rabbit

    # Generates the random x and y cords of carrots
    for i in range(n_carrots):
        x_c.append(random.randint(0, grid_size - 1))
        y_c.append(random.randint(0, grid_size - 1))

    # Generates the random x and y cords of holes
    for i in range(n_holes):
        x_h.append(random.randint(0, grid_size - 1))
        y_h.append(random.randint(0, grid_size - 1))

    # Makes the grid a 2D list
    for i in range(grid_size):
        grid.append([])

    # Adds all the pathway stones
    for i in range(grid_size):
        for j in range(grid_size):
            grid[i].append("-")

    # Adds the rabbit
    grid[y_r][x_r] = "r"

    # Adds the carrots
    for i in range(n_carrots):
        while True:
            # if the the random position there is already a carrot or a rabbit
            if grid[y_c[i]][x_c[i]] == "c" or grid[y_c[i]][x_c[i]] == "r":
                # Generates a new random x and y cords
                x_c[i] = random.randint(0, grid_size - 1)
                y_c[i] = random.randint(0, grid_size - 1)
            else:
                break

        grid[y_c[i]][x_c[i]] = "c"

    # Adds the holes
    for i in range(n_holes):
        while True:
            # if the the random position there is already a carrot, a rabbit or a hole
            if (
                grid[y_h[i]][x_h[i]] == "c"
                or grid[y_h[i]][x_h[i]] == "O"
                or grid[y_h[i]][x_h[i]] == "r"
            ):
                # Generates a new random x and y cords
                x_h[i] = random.randint(0, grid_size - 1)
                y_h[i] = random.randint(0, grid_size - 1)
            else:
                break

        grid[y_h[i]][x_h[i]] = "O"

    # Once done it returns all the required values so that it can be used outside the function
    return grid, x_r, y_r, x_h, y_h, x_c, y_c


def valid(grid, moves, start_x, start_y, ele, find, grid_size):
    for move in moves:
        x = False
        if move == "U":
            start_y -= 1
        elif move == "D":
            start_y += 1
        elif move == "L":
            start_x -= 1
        elif move == "R":
            start_x += 1
        elif move == "W":
            if (
                start_y > 1
                and grid[start_y - 1][start_x] == "O"
                and grid[start_y - 2][start_x] != "O"
                and grid[start_y - 2][start_x] != "c"
            ):
                x = True
                start_y -= 2
            else:
                return False
        elif move == "S":
            if (
                start_y < grid_size - 2
                and grid[start_y + 1][start_x] == "O"
                and grid[start_y + 2][start_x] != "O"
                and grid[start_y + 2][start_x] != "c"
            ):
                x = True
                start_y += 2
            else:
                return False
        elif move == "A":
            if (
                start_x > 1
                and grid[start_y][start_x - 1] == "O"
                and grid[start_y][start_x - 2] != "O"
                and grid[start_y][start_x - 2] != "c"
            ):
                x = True
                start_x -= 2
            else:
                return False
        elif move == "D":
            if (
                start_x < grid_size - 2
                and grid[start_y][start_x + 1] == "O"
                and grid[start_y][start_x + 2] != "O"
                and grid[start_y][start_x + 2] != "c"
            ):
                x = True
                start_x += 2
            else:
                return False

        if not (0 <= start_y < grid_size and 0 <= start_x < grid_size):
            return False
        elif not x and grid[start_y][start_x] == "O":
            return False
    return True


def find_end(grid, moves, start_x, start_y):
    for move in moves:
        if move == "U":
            if grid[start_y - 1][start_x] == "c":
                return True
            start_y -= 1
        elif move == "D":
            if grid[start_y + 1][start_x] == "c":
                return True
            start_y += 1
        elif move == "L":
            if grid[start_y][start_x - 1] == "c":
                return True
            start_x -= 1
        elif move == "R":
            if grid[start_y][start_x + 1] == "c":
                return True
            start_x += 1
        elif move == "W":
            start_y -= 2
        elif move == "S":
            start_y += 2
        elif move == "A":
            start_x -= 2
        elif move == "D":
            start_x += 2
    return False


def bfs(grid, n_c, start_x, start_y, ele, find, grid_size):
    path = queue.Queue()
    path.put("")
    add = ""
    visited = []
    while not find_end(grid, add, start_x, start_y):
        add = path.get()
        for j in ["U", "D", "L", "R", "W", "S", "A", "D"]:
            put = add + j
            v = valid(grid, put, start_x, start_y, ele, find, grid_size)
            if v and not put in visited:
                path.put(put)
                visited.append(put)
    return add


grid_size = int(input("Enter grid size: "))  # The length and width of the grid
n_c = int(input("Enter number of carrots: "))  # Number of carrots
n_h = int(input("Enter number of holes: "))  # Number of holes
grid, x_r, y_r, x_h, y_h, x_c, y_c = grid_generator(
    grid_size, n_c, n_h
)  # Calls the grid_generator function and gets all the required values
print_grid(grid)
found_c = bfs(grid, n_c, x_r, y_r, "r", "c", grid_size)

print(found_c)
