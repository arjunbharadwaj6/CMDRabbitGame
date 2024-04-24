# Imports
import os  # To clear the screen
import random  # Generating random positions
import time  # Stops the code for the user
from collections import deque


# Prints the grid
def print_grid(grid, cords):
    # I am printing the cords so that it will be easier while testing
    print(" " * len(cords[1]), end="")  # Indentation
    print(*cords, sep="   ")  # Prints the cords
    for i in range(len(grid)):
        print()  # Spacing

        # Two values for spacing
        x = len(cords[1])
        y = "  " + (" " * x)
        print(cords[i + 1], *grid[i], sep=y)
    print()


# Function to clear the screen
def clear_screen():
    # For Windows
    if os.name == "nt":
        os.system("cls")
    # For Linux/MacOS
    else:
        os.system("clear")


# Generates the grid
def generate_grid(grid_size, n_carrots, n_holes):
    # Using list comprehension i have generated a grid
    grid = [["-" for _ in range(grid_size)] for _ in range(grid_size)]

    # Rabbit position
    x_r, y_r = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
    # Adds the rabbit to the grid
    grid[y_r][x_r] = "r"

    # Carrots positions
    carrot_positions = []
    for _ in range(n_carrots):
        x, y = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
        # Makes sure that the carrot position is always unique
        while grid[y][x] != "-":
            x, y = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
        # Adds the carrot to the grid and the position to the list of positions
        grid[y][x] = "c"
        carrot_positions.append((x, y))

    # Holes positions
    hole_positions = []
    for _ in range(n_holes):
        x, y = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
        # Makes sure that the carrot position is always unique
        while grid[y][x] != "-":
            x, y = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
        # Adds the hole to the grid and the position to the list of positions
        grid[y][x] = "O"
        hole_positions.append((x, y))

    return grid, x_r, y_r, carrot_positions, hole_positions


# Checks the the move is vaild
def is_valid(grid, x, y, grid_size, target_x, target_y):
    # Check if the move is not out of bounds and there there is no hole in the preticular position
    if x == target_x and y == target_y:
        return True
    else:
        return (
            0 <= x < grid_size
            and 0 <= y < grid_size
            and grid[y][x] != "c"
            and grid[y][x] != "O"
        )


# Checks if the move is vaild for a jump
def is_valid_j(grid, x, y, old_x, old_y, grid_size):
    # Check if the move is not out of bounds and there there is no hole or carrot in the preticular position and that at the previous x and y there is a hole
    return (
        0 <= x < grid_size
        and 0 <= y < grid_size
        and grid[y][x] != "O"
        and grid[y][x] != "c"
        and grid[old_y][old_x] == "O"
    )


# The code for the sorting algorithm bfs(breadth-first search)
def bfs(grid, start_x, start_y, target_x, target_y, grid_size):
    # A double ended queue which stores the x and y cords, the number of steps and the path
    q = deque([(start_x, start_y, 0, [])])
    # A set of all the visited paths
    visited = set([(start_x, start_y)])

    # While q is not empty meaning there are more paths for the rabbit to go through
    while q:
        # Gets the x and y cords, the number of steps and the path that the rabbit has gone through
        x, y, steps, path = q.popleft()

        # If the carrot has been reached
        if (x, y) == (target_x, target_y):
            return steps, path

        # Movement of the rabbit up, down, left, right
        for move_x, move_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            # new_x and new_y are the x and y cords where the rabbit will go to
            new_x, new_y = x + move_x, y + move_y
            # Calls the vaild function checking if the move is vaild
            if is_valid(grid, new_x, new_y, grid_size, target_x, target_y):
                # If the cords are not visited
                if (new_x, new_y) not in visited:
                    # Since it is a possible move it is add to q and is also added to visited as it can be visited afterwards
                    q.append((new_x, new_y, steps + 1, path + [[new_x, new_y]]))
                    visited.add((new_x, new_y))

            # Since the move of new_x and new_y is not valid meaning that there might be a hole there, I check if there is a hole and that the next one is free
            elif is_valid_j(
                grid, new_x + move_x, new_y + move_y, new_x, new_y, grid_size
            ):
                # If the cords are not visited
                if (new_x + move_x, new_y + move_y) not in visited:
                    # Since it is a possible move it is add to q and is also added to visited as it can be visited afterwards
                    q.append(
                        (
                            new_x + move_x,
                            new_y + move_y,
                            steps + 1,
                            path + [[new_x + move_x, new_y + move_y]],
                        )
                    )
                    visited.add((new_x + move_x, new_y + move_y))

    return grid_size * grid_size + 1, []  # If no path found


# The function which calls the bfs and has all the carrots data
def find_carrots(grid, x_r, y_r, carrot_positions, hole_positions, grid_size):
    carrot_steps = []  # Number of steps
    carrot_paths = []  # The paths of the carrots

    # Goes through all the carrots and for each of the carrot goes through the holes to find the number of steps it takes to finish the game
    for c_x, c_y in carrot_positions:
        hole_steps = []
        hole_paths = []
        for h_x, h_y in hole_positions:
            # Number of steps from the carrot to the hole and the path taken
            steps_h, path_h = bfs(grid, c_x, c_y, h_x, h_y, grid_size)
            hole_steps.append(steps_h)
            hole_paths.append(path_h)
        # Number of steps from the rabbit to the carrot and the paths
        steps, path = bfs(grid, x_r, y_r, c_x, c_y, grid_size)
        # The number of steps to finish the game if the carrot was chosen is being added to carrot_steps
        carrot_steps.append(steps + min(hole_steps))
        # The quickest path if the carrot was chosen is being add to carrot_paths
        carrot_paths.append(path + hole_paths[hole_steps.index(min(hole_steps))])

    return carrot_steps, carrot_paths


# Moves the rabbit through the quickest path
def movement_of_rabbit(grid, cords, x_r, y_r, path):
    # CLears the screen and prints the path and the grid and waits for 4 seconds so that the user can look at the board
    clear_screen()
    print_grid(grid, cords)
    print(
        f"The path that the rabbit need to take to finish the game in least number of steps"
    )
    print(*path)
    time.sleep(4)
    picked = False  # If the carrot has been picked
    for i in range(len(path)):
        # Sets the previous position of the rabbit to a pathway stone
        grid[y_r][x_r] = "-"
        x_r = path[i][0]  # Gets the new x cord of rabbit
        y_r = path[i][1]  # Gets the new y cord of rabbit
        # If the carrot has already been picked or is going to be picked on next move
        if picked or grid[y_r][x_r] == "c":
            grid[y_r][x_r] = "R"  # New position of the rabbit
            picked = True  # Since the carrot has been picked it will become true
        else:
            grid[y_r][x_r] = "r"  # New position of the rabbit
        clear_screen()  # Clears the screen
        print_grid(grid, cords)  # Prints the new grid
        # Prints the path that the rabbit will follow
        print(
            f"The path that the rabbit need to take to finish the game in least number of steps"
        )
        print(*path)
        time.sleep(1.5)  # Waits for 1.5 seconds


# Takes the grid size, the number of carrots and the number of holes
grid_size = int(input("Enter grid size: "))
n_c = int(input("Enter number of carrots: "))
n_h = int(input("Enter number of holes: "))
cords = [""]

# Adds the numbers to the cords list  in a way so that the length of each number is the same
for i in range(grid_size):
    # Gets the difference between the length of the largest and the smalles number
    num_zeros = len(str(grid_size - 1)) - len(str(i))
    # Adds the necessary number of zeros
    formatted_number = "0" * num_zeros + str(i)
    # Adds the number to the cords list
    cords.append(formatted_number)

# Makes sure that the input is matches the criteria
while (grid_size < 10 or n_c < 2 or n_h < 2) and (n_c + n_h < grid_size * grid_size):
    print(
        "Minimum of 10 for grid size, 2 for carrots and 2 for holes and the sum of carrots and the holes should not exceed (grid size squared - 1)"
    )
    grid_size = int(input("Enter grid size: "))
    n_c = int(input("Enter number of carrots: "))
    n_h = int(input("Enter number of holes: "))

# Generate the grid
grid, x_r, y_r, carrot_positions, hole_positions = generate_grid(grid_size, n_c, n_h)

# Find all the carrots and the number of steps it takes to reach it
carrot_steps, carrot_paths = find_carrots(
    grid, x_r, y_r, carrot_positions, hole_positions, grid_size
)

# Moves the rabbit on the shortest path
movement_of_rabbit(
    grid, cords, x_r, y_r, carrot_paths[carrot_steps.index(min(carrot_steps))]
)
