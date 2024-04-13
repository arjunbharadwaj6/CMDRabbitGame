# Imports
import os
import random

# Need to be installed it is used to capture the users input like arrow keys
# It can be installed using pip install keyboard
import keyboard


def clear_screen():
    """
    Function to clear the screen
    """
    # For Windows
    if os.name == "nt":
        os.system("cls")
    # For Linux/MacOS
    else:
        os.system("clear")


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


# printing function to avoid repetition
def print_cj():
    print("You can't jump given the circumstance.")


def print_nath():
    print("Since you are not adjacent to a hole you can't place the carrot.")


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
    while True:
        # If the user entered 0 carrots
        if n_carrots < 2:
            print("Please enter 2 or more carrots or the game can never end")
            n_carrots = int(input("Enter number of carrots: "))
        # If the user entered 0 holes
        elif n_holes < 2:
            print("Please enter 2 or more holes or the game can never end")
            n_holes = int(input("Enter number of holes: "))
        # If It matches the guidlines
        elif n_carrots + n_holes < grid_size * grid_size and grid_size >= 10:
            break
        # If the grid_size is too small
        elif grid_size < 10:
            print("The grid size is too small please enter minimum of 10")
            grid_size = int(input("Enter grid size: "))
        # If the carrots and the holes don't fit in the given grid
        elif n_carrots + n_holes >= grid_size * grid_size:
            print(
                "There are too many carrots and holes for the given board. Please reduce the number of carrots and number of holes"
            )
            n_carrots = int(input("Enter number of carrots: "))
            n_holes = int(input("Enter number of holes: "))

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


grid_size = int(input("Enter grid size: "))  # The length and width of the grid
n_c = int(input("Enter number of carrots: "))  # Number of carrots
n_h = int(input("Enter number of holes: "))  # Number of holes
grid, x_r, y_r, x_h, y_h, x_c, y_c = grid_generator(
    grid_size, n_c, n_h
)  # Calls the grid_generator function and gets all the required values

picked = False  # This is a boolean that is false if the rabbit has not picked a carrot and true if the rabbit has picked the carrot
game_over = False

print_grid(grid)
print("Use arrow keys or wasd to move")
print("Use the 'j' key to jump and the 'p' key to pick up the carrot.")
print(
    "You can only pick up one carrot. You can place the picked up carrot in a hole by using the key 'p'."
)
print("Press 'q' to exit the game at any point")


def movement(event):
    """
    This function defines the movement of the rabbit

    Args:
        event (string): The key which is pressed
    """
    global x_r, y_r, grid_size, game_over, picked  # These variable are global so that i can access their value inside the function

    # Clears the screen
    clear_screen()

    grid[y_r][x_r] = "-"
    # If the up or the w key has been pressed
    if event.name == "q":
        game_over = True
    elif event.name == "up" or event.name == "w":
        if y_r == 0:  # edge of the board
            print("You can't go up. You are at the edge of the board.")
        elif grid[y_r - 1][x_r] == "c":  # there is a carrot above
            print("You can't go up as there is a carrot.")
        elif grid[y_r - 1][x_r] == "O":  # there is a hole above
            print("You can't go up as there is a hole. Use 'J' to jump.")
        else:  # if it is none of them that means that the rabbit can go up
            # rabbits current position becomes a path way stone
            y_r -= 1  # rabbits y cord decreases by 1

    # Works in the same way as when the up or w key is pressed
    elif event.name == "down" or event.name == "s":
        if y_r == grid_size - 1:
            print("You can't go down. You are at the edge of the board.")
        elif grid[y_r + 1][x_r] == "c":
            print("You can't go down as there is a carrot.")
        elif grid[y_r + 1][x_r] == "O":
            print("You can't go down as there is a hole. Use 'J' to jump.")
        else:
            y_r += 1

    # Works in the same way as when the up or w key is pressed
    elif event.name == "left" or event.name == "a":
        if x_r == 0:
            print("You can't go left. You are at the edge of the board.")
        elif grid[y_r][x_r - 1] == "c":
            print("You can't go left as there is a carrot.")
        elif grid[y_r][x_r - 1] == "O":
            print("You can't go left as there is a hole. Use 'J' to jump.")
        else:
            x_r -= 1

    # Works in the same way as when the up or w key is pressed
    elif event.name == "right" or event.name == "d":
        if x_r == grid_size - 1:
            print("You can't go right. You are at the edge of the board.")
        elif grid[y_r][x_r + 1] == "c":
            print("You can't go right as there is a carrot.")
        elif grid[y_r][x_r + 1] == "O":
            print("You can't go right as there is a hole. Use 'J' to jump.")
        else:
            x_r += 1

    # If the j key is pressed the rabbit has to jump
    elif event.name == "j":
        # Checking is it able to jump up
        if (
            y_r > 1
            and grid[y_r - 1][x_r] == "O"
            and (grid[y_r - 2][x_r] != "O" and grid[y_r - 2][x_r] != "c")
        ):
            y_r -= 2
        # Checking is it able to jump down
        elif (
            y_r < grid_size - 2
            and grid[y_r + 1][x_r] == "O"
            and (grid[y_r + 2][x_r] != "O" and grid[y_r + 2][x_r] != "c")
        ):
            y_r += 2
        # Checking is it able to jump to the left
        elif (
            x_r > 1
            and grid[y_r][x_r - 1] == "O"
            and (grid[y_r][x_r - 2] != "O" and grid[y_r][x_r - 2] != "c")
        ):
            x_r -= 2
        # Checking is it able to jump to the right
        elif (
            x_r < grid_size - 2
            and grid[y_r][x_r + 1] == "O"
            and (grid[y_r][x_r + 2] != "O" and grid[y_r][x_r + 2] != "c")
        ):
            x_r += 2

    # If the p key is pressed it has to either pick up a carrot or place it
    elif event.name == "p":
        # If the rabbit has not picked up the carrot
        if not picked:
            picked = True
            # If there is a carrot above the rabbit
            if y_r == 0:
                if grid[y_r + 1][x_r] == "c":
                    y_r += 1
                elif grid[y_r][x_r - 1] == "c":
                    x_r -= 1
                elif grid[y_r][x_r + 1] == "c":
                    x_r += 1
            # If there is a carrot below the rabbit
            elif y_r == grid_size - 1:
                if grid[y_r - 1][x_r] == "c":
                    y_r -= 1
                elif grid[y_r][x_r - 1] == "c":
                    x_r -= 1
                elif grid[y_r][x_r + 1] == "c":
                    x_r += 1
            # If there is a carrot to the left of the rabbit
            elif x_r == 0:
                if grid[y_r + 1][x_r] == "c":
                    y_r += 1
                elif grid[y_r - 1][x_r] == "c":
                    y_r -= 1
                elif grid[y_r][x_r + 1] == "c":
                    x_r += 1
            # If there is a carrot to the right of the rabbit
            elif x_r == grid_size - 1:
                if grid[y_r + 1][x_r] == "c":
                    y_r += 1
                elif grid[y_r][x_r - 1] == "c":
                    x_r -= 1
                elif grid[y_r - 1][x_r] == "c":
                    y_r -= 1
            else:  # If there is no carrot adjacent to the carrot
                if grid[y_r + 1][x_r] == "c":
                    y_r += 1
                elif grid[y_r - 1][x_r] == "c":
                    y_r -= 1
                elif grid[y_r][x_r + 1] == "c":
                    x_r += 1
                elif grid[y_r][x_r - 1] == "c":
                    x_r -= 1
                else:
                    print("Since you are not adjacent to a carrot you can't pick it up")
                    picked = False
        # If the carrot has already been picked and it has to be placed in a hole
        else:
            # If the rabbit is at the top of the board
            if y_r == 0:
                # If there is a hole adjacent to the rabbit
                if (
                    grid[y_r + 1][x_r] == "O"
                    or grid[y_r][x_r - 1] == "O"
                    or grid[y_r][x_r + 1] == "O"
                ):
                    print("Game Over!!!!")
                    game_over = True
                else:
                    print_nath()
            # If the rabbit is at the top of the board
            elif y_r == grid_size - 1:
                # If there is a hole adjacent to the rabbit
                if (
                    grid[y_r - 1][x_r] == "O"
                    or grid[y_r][x_r - 1] == "O"
                    or grid[y_r][x_r + 1] == "O"
                ):
                    print("Game Over!!!!")
                    game_over = True
                else:
                    print_nath()
            # If the rabbit is at the left edge of the board
            elif x_r == 0:
                # If there is a hole adjacent to the rabbit
                if (
                    grid[y_r - 1][x_r] == "O"
                    or grid[y_r + 1][x_r] == "O"
                    or grid[y_r][x_r + 1] == "O"
                ):
                    print("Game Over!!!!")
                    game_over = True
                else:
                    print_nath()
            # If the rabbit is at the right edge of the board
            elif x_r == grid_size - 1:
                # If there is a hole adjacent to the rabbit
                if (
                    grid[y_r - 1][x_r] == "O"
                    or grid[y_r + 1][x_r] == "O"
                    or grid[y_r][x_r - 1] == "O"
                ):
                    print("Game Over!!!!")
                    game_over = True
                else:
                    print_nath()
            # If the rabbit is not at the edge of the board
            else:
                # If there is a hole adjacent to the rabbit
                if (
                    grid[y_r - 1][x_r] == "O"
                    or grid[y_r + 1][x_r] == "O"
                    or grid[y_r][x_r - 1] == "O"
                    or grid[y_r][x_r + 1] == "O"
                ):
                    print("Game Over!!!!")
                    game_over = True
                else:
                    print_nath()

    # If a carrot has been picked then it become R
    if picked:
        grid[y_r][x_r] = "R"
    else:
        grid[y_r][x_r] = "r"

    # Prints the grid
    print_grid(grid)


def find_shortest_path(start_x, start_y, x_cords, y_cords):
    dis_x = []
    dis_y = []
    dis = []
    for x in x_cords:
        dis_x.append(abs(start_x - x))

    for y in y_cords:
        dis_y.append(abs(start_y - y))

    for i in range(len(dis_x)):
        dis.append(dis_x[i] + dis_y[i])

    min_dis = min(dis)
    return dis, min(dis)


dis, min_dis = find_shortest_path(x_r, y_r, x_c, y_c)

for i in range(len(dis)):
    dis_h, min_hole_dis = find_shortest_path(x_c[i], y_c[i], x_h, y_h)
    dis[i] += min_hole_dis

print(f"The min number of steps required to finish the game is: {min(dis)}")

while not game_over:
    # Reads the keyboard input
    event = keyboard.read_event()

    # Check if it's a key press event
    if event.event_type == keyboard.KEY_DOWN:
        movement(event)
