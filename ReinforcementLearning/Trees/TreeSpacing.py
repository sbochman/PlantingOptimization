import numpy as np
import math
from TreeGenerator import TreeGenerator

tree_types_dict = {
    0: "None",
    1: "Abies Holophylla",
    2: "Pinus Desniflora1",
    3: "Pinus Desniflora2",
    4: "Pinus Desniflora Globosa",
    5: "Taxus Cuspidata",
    6: "White Pine",
    7: "Acer Palmatum",
    8: "Betula Platyphylla",
    9: "Cercidiphyllum Japonicum",
    10: "Chaenomeless Sinensis",
    11: "Chionanthus Retusus",
    12: "Cornus Officinalis",
    13: "Ginkgo Biloba",
    14: "Kobus Magnolia",
    15: "Liriodendron Tulipifera",
    16: "Oak",
    17: "Persimmon",
    18: "Prunus Armeniaca",
    19: "Prunus Yedoensis",
    20: "Sophora Japonica",
    21: "Zelkova Serrata"
}

def update_coords(fill_cords, grid, numerical_representation):
    plantable = True
    for coord in fill_cords:
        x, y = coord
        if grid[x][y] < 0:
            plantable = False
            break
    if plantable:
        for coord in fill_cords:
            x, y = coord

            grid[x][y] = numerical_representation
    return grid, plantable

grid = np.zeros((10, 10))


tree2 = TreeGenerator().generateTree(tree_types_dict[1], (1, 4))
occupied2, numerical_representation2 = tree2.fillGridRadius(10, 10)
tree1 = TreeGenerator().generateTree(tree_types_dict[2], (7, 5))
occupied, numerical_representation = tree1.fillGridRadius(10, 10)

# Update the grid with the tree's radius
grid, plantable = update_coords(occupied2, grid, numerical_representation)
#print new grid
print(plantable)
for row in grid:
    print(" ".join(str(int(cell)) for cell in row))

print("====================================")

grid, plantable = update_coords(occupied, grid, numerical_representation2)
print(plantable)
#print new grid
for row in grid:
    print(" ".join(str(int(cell)) for cell in row))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


# Define a color map: 1 is green and 0 is white
cmap = ListedColormap(['green', 'red', 'white'])

plt.figure(figsize=(10, 10))
plt.imshow(grid, cmap=cmap, aspect='equal')  # Use the color map

# Add grid lines with correct alignment
plt.grid(True, which='both', color='black', linestyle='-', linewidth=2)
plt.xticks(np.arange(-0.5, len(grid[0]), 1), [])
plt.yticks(np.arange(-0.5, len(grid), 1), [])

# Setting grid lines for minor ticks to ensure they are in between cells
plt.gca().set_xticks(np.arange(-0.5, len(grid[0]), 1), minor=True)
plt.gca().set_yticks(np.arange(-0.5, len(grid), 1), minor=True)
plt.grid(True, which='minor', color='black', linestyle='-', linewidth=2)

plt.title('Grid Visualization: Green Planted, White Unplanted')
plt.show()



"""

def create_circle_in_grid(grid_width, grid_height, center_x, center_y, radius):
    # Initialize the grid with zeros
    grid = np.zeros((grid_height, grid_width))

    # Iterate over each cell in the grid
    for x in range(grid_width):
        for y in range(grid_height):
            # Calculate the distance from the center to this cell
            distance = math.sqrt((center_x - x) ** 2 + (center_y - y) ** 2)

            # If the distance is within the radius, mark the cell as 1 (within the buffer zone)
            if distance <= math.ceil(radius):
                grid[y, x] = 1  # Marking 1 for buffer zone

    return grid

# Example usage
grid_width = 9  # width of the grid
grid_height = 9  # height of the grid
center_x = 4  # x-coordinate of the tree center
center_y = 4  # y-coordinate of the tree center
radius = 2.8 # radius of the buffer zone around the tree

# Create the grid with the circular buffer zone
grid = create_circle_in_grid(grid_width, grid_height, center_x, center_y, radius)

# Print the grid
for row in grid:
    print(" ".join(str(int(cell)) for cell in row))


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


# Define a color map: 1 is green and 0 is white
cmap = ListedColormap(['white', 'green'])

plt.figure(figsize=(10, 10))
plt.imshow(grid, cmap=cmap, aspect='equal')  # Use the color map

# Add grid lines with correct alignment
plt.grid(True, which='both', color='black', linestyle='-', linewidth=2)
plt.xticks(np.arange(-0.5, len(grid[0]), 1), [])
plt.yticks(np.arange(-0.5, len(grid), 1), [])

# Setting grid lines for minor ticks to ensure they are in between cells
plt.gca().set_xticks(np.arange(-0.5, len(grid[0]), 1), minor=True)
plt.gca().set_yticks(np.arange(-0.5, len(grid), 1), minor=True)
plt.grid(True, which='minor', color='black', linestyle='-', linewidth=2)

plt.title('Grid Visualization: Green Planted, White Unplanted')
plt.show()
"""