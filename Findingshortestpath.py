import random
from collections import deque


# Prints the grid
def print_grid(grid, cords):
    # I am printing the cords so that it will be easier while testing
    print(" ", end="")
    print(*cords, sep="    ")
    for i in range(len(grid)):
        print()
        print(i, *grid[i], sep="    ")
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
            if is_valid(grid, new_x, new_y, grid_size, target_x, target_y):
                # If the cords are not visited
                if (new_x, new_y) not in visited:
                    # Since it is a possible move it is add to q and is also added to visited as it will be visited
                    q.append((new_x, new_y, steps + 1))
                    visited.add((new_x, new_y))

            # Since the move of new_x and new_y is not valid meaning that there might be a hole there, I check if the next one is free
            elif is_valid_j(
                grid, new_x + move_x, new_y + move_y, new_x, new_y, grid_size
            ):
                # If the cords are not visited
                if (new_x + move_x, new_y + move_y) not in visited:
                    # Since it is a possible move it is add to q and is also added to visited as it will be visited
                    q.append((new_x + move_x, new_y + move_y, steps + 1))
                    visited.add((new_x + move_x, new_y + move_y))

    return grid_size * grid_size + 1  # If no path found


# The function which calls the bfs and has all the carrots data
def find_carrots(grid, x_r, y_r, carrot_positions, hole_positions, grid_size):
    carrot_steps = []  # Number of steps
    carrot_cords = []  # The cords of the carrots

    # Goes through all the carrots and for each of the carrot goes through the holes to find the number of steps it takes to finish the game
    for c_x, c_y in carrot_positions:
        hole_steps = []
        for h_x, h_y in hole_positions:
            steps_h = bfs(
                grid, c_x, c_y, h_x, h_y, grid_size
            )  # Number of steps from the carrot to the hole
            hole_steps.append(steps_h)
        steps = bfs(
            grid, x_r, y_r, c_x, c_y, grid_size
        )  # Number of steps from the rabbit to the carrot
        # The number of steps to finish the game if the carrot was chosen is being added to carrot_steps
        carrot_steps.append(steps + min(hole_steps))
        # The cords of the carrot is being added to carrot_cords
        carrot_cords.append([c_x, c_y])

    return carrot_steps, carrot_cords


# Takes the grid size, the number of carrots and the number of holes
grid_size = int(input("Enter grid size: "))
n_c = int(input("Enter number of carrots: "))
n_h = int(input("Enter number of holes: "))
cords = [i for i in range(10)]
cords.insert(0, "")

# Makes sure that the input is matches the criteria
while (grid_size < 10 or n_c < 2 or n_h < 2) and (n_c + n_h < grid_size * grid_size):
    print(
        "Minimum of 10 for grid size, 2 for carrots and 2 for holes and the sum of carrots and the holes should not exceed (grid size squared - 1)"
    )
    grid_size = int(input("Enter grid size: "))
    n_c = int(input("Enter number of carrots: "))
    n_h = int(input("Enter number of holes: "))

# Generate the grid and prints it
grid, x_r, y_r, carrot_positions, hole_positions = generate_grid(grid_size, n_c, n_h)
print_grid(grid, cords)

# Find all the carrots and the number of steps it takes to reach it
carrot_steps, carrot_cords = find_carrots(
    grid, x_r, y_r, carrot_positions, hole_positions, grid_size
)

# Prints the minimum number of steps required to finish the game and the cords of the carrot
if min(carrot_steps) < grid_size * grid_size:
    print(
        f"The minimum number of steps required to finish the game is: {min(carrot_steps)}"
    )
else:
    print("The cannot finsih the game")
print(f"The cords are: {carrot_cords[carrot_steps.index(min(carrot_steps))]}")
