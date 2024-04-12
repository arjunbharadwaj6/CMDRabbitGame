# Imports
import os
import random

# Need to be installed it is used to capture the users input like arrow keys
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


# printing function to avoid repetition
def print_oob():
    print("You can't jump as you will go outside the board")


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
        if n_carrots == 0:
            print("Please enter 1 or more carrots or the game can never end")
            n_carrots = int(input("Enter number of carrots: "))
        # If the user entered 0 holes
        elif n_holes == 0:
            print("Please enter 1 or more holes or the game can never end")
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
    return grid, x_r, y_r


grid_size = int(input("Enter grid size: "))  # The length and width of the grid
n_c = int(input("Enter number of carrots: "))  # Number of carrots
n_h = int(input("Enter number of holes: "))  # Number of holes
grid, x_r, y_r = grid_generator(
    grid_size, n_c, n_h
)  # Calls the grid_generator function and gets all the required values

picked = False  # This is a boolean that is false if the rabbit has not picked a carrot and true if the rabbit has picked the carrot


print_grid(grid)
print("Use arrow keys or wasd to move")
print("Use the 'j' key to jump and the 'p' key to pick up the carrot.")
print(
    "You can only pick up one carrot. You can place the picked up carrot in a hole by using the key 'p'."
)

while True:

    def movement(event):
        """
        This function defines the movement of the rabbit

        Args:
            event (string): The key which is pressed
        """
        global x_r, y_r, grid_size, picked  # These variable are global so that i can access their value inside the function

        # Clears the screen
        clear_screen()

        # If the up or the w key has been pressed
        if event.name == "up" or event.name == "w":
            if y_r == 0:  # edge of the board
                print("You can't go up. You are at the edge of the board.")
            elif grid[y_r - 1][x_r] == "c":  # there is a carrot above
                print("You can't go up as there is a carrot.")
            elif grid[y_r - 1][x_r] == "O":  # there is a hole above
                print("You can't go up as there is a hole. Use 'J' to jump.")
            else:  # if it is none of them that means that the rabbit can go up
                # rabbits current position becomes a path way stone
                grid[y_r][x_r] = "-"
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
                grid[y_r][x_r] = "-"
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
                grid[y_r][x_r] = "-"
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
                grid[y_r][x_r] = "-"
                x_r += 1

        # If the j key is pressed the rabbit has to jump
        elif event.name == "j":
            # Checks if there is a hole above the rabbit
            if grid[y_r - 1][x_r] == "O":
                if (
                    y_r > 1
                ):  # Check that if the rabbit jumps it will not go outside the board
                    grid[y_r][x_r] = "-"
                    y_r -= 2
                else:
                    print_oob()
            # Checks if there is a hole below the rabbit
            elif grid[y_r + 1][x_r] == "O":
                if (
                    y_r < grid_size - 2
                ):  # Check that if the rabbit jumps it will not go outside the board
                    grid[y_r][x_r] = "-"
                    y_r += 2
                else:
                    print_oob()
            # Checks if there is a hole to the left of the rabbit
            elif grid[y_r][x_r - 1] == "O":
                if (
                    x_r > 1
                ):  # Check that if the rabbit jumps it will not go outside the board
                    grid[y_r][x_r] = "-"
                    x_r -= 2
                else:
                    print_oob()
            # Checks if there is a hole to the right of the rabbit
            elif grid[y_r][x_r + 1] == "O":
                if (
                    x_r < grid_size - 2
                ):  # Check that if the rabbit jumps it will not go outside the board
                    grid[y_r][x_r] = "-"
                    x_r += 2
                else:
                    print_oob()
            # Otherwise it means that there is no hole adjacent to the rabbit
            else:
                print("Since there is no hole you cannot jump.")

        # If the p key is pressed it has to either pick up a carrot or place it
        elif event.name == "p":
            # If the rabbit has not picked up the carrot
            if not picked:
                # If there is a carrot above the rabbit
                if grid[y_r - 1][x_r] == "c":
                    grid[y_r - 1][x_r] = "-"
                    picked = True
                # If there is a carrot below the rabbit
                elif grid[y_r + 1][x_r] == "c":
                    grid[y_r + 1][x_r] = "-"
                    picked = True
                # If there is a carrot to the left of the rabbit
                elif grid[y_r][x_r - 1] == "c":
                    grid[y_r][x_r - 1] = "-"
                    picked = True
                # If there is a carrot to the right of the rabbit
                elif grid[y_r][x_r + 1] == "c":
                    grid[y_r][x_r + 1] = "-"
                    picked = True
                else:  # If there is no carrot adjacent to the carrot
                    print("Since you are not adjacent to a carrot you can't pick it up")
            # If the carrot has already been picked and it has to be placed in a hole
            else:
                # If there is a hole adjacent to the rabbit the game ends
                if (
                    grid[y_r - 1][x_r] == "O"
                    or grid[y_r + 1][x_r] == "O"
                    or grid[y_r][x_r - 1] == "O"
                    or grid[y_r][x_r + 1] == "O"
                ):
                    print("Game Over!!!!")
                    exit()
                elif (
                    grid[y_r - 1][x_r] == "c"
                    or grid[y_r + 1][x_r] == "c"
                    or grid[y_r][x_r - 1] == "c"
                    or grid[y_r][x_r + 1] == "c"
                ):
                    print(
                        "Since you already have picked up a carrot you can't pick up one more, you have to place the carrot in a hole."
                    )
                else:  # If there is no hole adjacent to the rabbit it cannot place the carrot in a hole
                    print(
                        "Since you are not adjacent to a hole you can't place it in a hole."
                    )

        # If a carrot has been picked then it become R
        if picked:
            grid[y_r][x_r] = "R"
        else:
            grid[y_r][x_r] = "r"

        # Prints the grid
        print_grid(grid)

    # Using the keyboard library it waits for the users input
    keyboard.on_press_key("up", movement)
    keyboard.on_press_key("w", movement)
    keyboard.on_press_key("down", movement)
    keyboard.on_press_key("s", movement)
    keyboard.on_press_key("left", movement)
    keyboard.on_press_key("a", movement)
    keyboard.on_press_key("right", movement)
    keyboard.on_press_key("d", movement)
    keyboard.on_press_key("j", movement)
    keyboard.on_press_key("p", movement)
    keyboard.wait()  # Waiting for the input
