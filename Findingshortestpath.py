import random
from collections import deque


# Prints the grid
def print_grid(grid):
    for row in grid:
        print("    ".join(row))
        print()


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

    return grid, x_r, y_r, carrot_positions


# Checks the the move is vaild
def is_valid(grid, x, y, grid_size):
    # Check if the move is not out of bounds and there there is no hole in the preticular position
    return 0 <= x < grid_size and 0 <= y < grid_size and grid[y][x] != "O"


# Checks if the move is vaild for a jump
def is_valid_j(grid, x, y, grid_size):
    # Check if the move is not out of bounds and there there is no hole or carrot in the preticular position
    return (
        0 <= x < grid_size
        and 0 <= y < grid_size
        and grid[y][x] != "O"
        and grid[y][x] != "c"
    )


# The code for the sorting algorithm bfs(breadth-first search)
def bfs(grid, start_x, start_y, target_x, target_y, grid_size):
    # A double ended queue which stores the x and y cords and the number of steps
    q = deque([(start_x, start_y, 0)])
    # A set of all the visited paths
    visited = set([(start_x, start_y)])

    # While q is not empty meaning there are more path for the rabbit to go through
    while q:
        # Gets the x and y cords and the number of steps already taken by the rabbit
        x, y, steps = q.popleft()

        # If the carrot has been reached
        if (x, y) == (target_x, target_y):
            return steps

        for move_x, move_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            # new_x and new_y are the x and y cords where the rabbit will go to
            new_x, new_y = x + move_x, y + move_y
            # Calls the vaild function checking if the move is vaild
            if is_valid(grid, new_x, new_y, grid_size):
                # If the cords are not visited
                if (new_x, new_y) not in visited:
                    # Since it is a possible move it is add to q and is also added to visited as it will be visited
                    q.append((new_x, new_y, steps + 1))
                    visited.add((new_x, new_y))

            # Since the move of new_x and new_y is not valid meaning that there might be a hole there, I check if the next one is free
            elif is_valid_j(grid, new_x + move_x, new_y + move_y, grid_size):
                # If the cords are not visited
                if (new_x + move_x, new_y + move_y) not in visited:
                    # Since it is a possible move it is add to q and is also added to visited as it will be visited
                    q.append((new_x + move_x, new_y + move_y, steps + 1))
                    visited.add((new_x + move_x, new_y + move_y))

    return float("inf")  # If no path found


# The function which calls the bfs and has all the carrots data
def find_carrots(grid, x_r, y_r, carrot_positions, grid_size):
    # I have made a list of dictionaries which conation the x and y cords of the carrot and the number of steps it takes to reach them
    carrot_data = []

    # Goes through all the carrots and finds the least number of steps it takes to reach them
    for x, y in carrot_positions:
        steps = bfs(grid, x_r, y_r, x, y, grid_size)
        carrot_data.append({"position": (x, y), "steps": steps})

    return carrot_data


# Takes the grid size, the number of carrots and the number of holes
grid_size = int(input("Enter grid size: "))
n_c = int(input("Enter number of carrots: "))
n_h = int(input("Enter number of holes: "))

# Makes sure that the input is matches the criteria
while grid_size < 10 or n_c < 2 or n_h < 2:
    print("Minimum of 10 for grid size, 2 for carrots and 2 for holes")
    grid_size = int(input("Enter grid size: "))
    n_c = int(input("Enter number of carrots: "))
    n_h = int(input("Enter number of holes: "))

# Generate the grid and prints it
grid, x_r, y_r, carrot_positions = generate_grid(grid_size, n_c, n_h)
print_grid(grid)

# Find all the carrots and the number of steps it takes to reach it
carrot_data = find_carrots(grid, x_r, y_r, carrot_positions, grid_size)
print("\nCarrots:")
# Goes through all the carrots and prints the position and the number of steps to reach it
for i, carrot in enumerate(carrot_data):
    print(f"Carrot {i+1}: Position: {carrot['position']}, Steps: {carrot['steps']}")
