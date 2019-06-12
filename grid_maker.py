import numpy as np
import matplotlib.pyplot as plt
import sys # used to eliminate printing truncation


# Constructs a 2D array of booleans, true = a given vertex is inside the SC

def get_grid_layout(b, l, level, c):
    '''
        Generates a 2D array that looks something like this

        0,1,1,1,0
        1,1,1,1,1
        1,1,1,1,1
        1,1,1,1,1
        0,1,1,1,0

        Works on multiple levels!
    '''
    if (l!=0 and b%2 != l%2) or b==l:
        print("Invalid Input!")
        return

    num_vertices = (c+1) * b**level + 1
    sc = np.ones((num_vertices, num_vertices))

    for y, row in enumerate(sc):
        for x, val in enumerate(sc):
            if x%(c+1) == 0 and y%(c+1) == 0:
                sc[y, x] = 0

    for current_level in range(1, level+1):
        vertices_current = (c+1)*b**current_level + 1
        prev_vertices_current = (c+1)*b**(current_level-1) + 1
        hole_size = l*(c+1)*b**(current_level-1)-1
        for i in range((b-l)/2*(prev_vertices_current-1)+1, num_vertices, vertices_current-1):
            for j in range((b-l)/2*(prev_vertices_current-1)+1, num_vertices, vertices_current-1):
                sc[i:i+hole_size, j:j+hole_size] = 0

    print(sc)

    return sc

def get_indexed_layout(grid_layout):
    '''
        Generates a 2D array that looks something like this

        -1,0,1,2,-1
        3,4,5,6,7
        8,9,10,11,12
        13,14,15,16,17
        -1,18,19,20,-1

        Each number represents the row of vector which will hold the laplacian
    '''
    indexed_layout = np.full(np.shape(grid_layout), -1, dtype=object)
    counter = 0
    for y, row in enumerate(grid_layout):
        for x, val in enumerate(row):
            if val:
                indexed_layout[y,x] = counter
                counter+=1

    return indexed_layout

def get_coordinates(grid_layout):
    '''
        Returns an 2D array for which each row is the (row,col) coordinates
    '''
    #should not work
    num_coordinates = int(np.sum(grid_layout))
    coordinates = np.zeros((num_coordinates, 2), dtype=object)
    counter = 0
    for y, row in enumerate(grid_layout):
        for x, val in enumerate(row):
            if val:
                coordinates[counter] = (y, x)
                counter+=1

    return coordinates

def compute_laplacian(indexed_layout, crosswires):
    # Gets coordiantes by checking which are not -1
    num_coordinates = int(np.sum(indexed_layout != -1))

    # Compute Laplacian Matrix
    laplacian = np.zeros((num_coordinates, num_coordinates))
    for y, row in enumerate(indexed_layout):
        for x, val in enumerate(row):
            if val != -1:
                neighbors = 0
                if x > 0 and y % (crosswires+1) != 0 and indexed_layout[y, x-1] != -1:
                    laplacian[indexed_layout[y, x], indexed_layout[y, x-1]] = 1
                    neighbors+=1
                if y > 0 and x % (crosswires+1) != 0 and indexed_layout[y-1, x] != -1:
                    laplacian[indexed_layout[y, x], indexed_layout[y-1, x]] = 1
                    neighbors+=1
                if x < np.shape(indexed_layout)[1]-1 and y % (crosswires+1) != 0 and indexed_layout[y, x+1] != -1:
                    laplacian[indexed_layout[y, x], indexed_layout[y, x+1]] = 1
                    neighbors+=1
                if y < np.shape(indexed_layout)[0]-1 and x % (crosswires+1) != 0 and indexed_layout[y+1, x] != -1:
                    laplacian[indexed_layout[y, x], indexed_layout[y+1, x]] = 1
                    neighbors+=1

                laplacian[indexed_layout[y, x], indexed_layout[y, x]] = -neighbors

    return laplacian

def main():
    # Tries to make printing better (fails)
    np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize)

    # Input Values
    b = 3
    l = 1
    level = 2
    crosswires = 1

    grid_layout = get_grid_layout(b, l, level, crosswires)
    plt.imshow(grid_layout)
    plt.show()

    print('Computing \'indexed_layout\' ...')
    indexed_layout = get_indexed_layout(grid_layout)
    #plt.imshow(indexed_layout)

    print('Computing \'coordinates\' ...')
    coordinates = get_coordinates(grid_layout)

    print('Number of Vertices: %d' % (np.shape(coordinates)[0]))

    print('Computing \'laplacian\' ...')
    laplacian = compute_laplacian(indexed_layout, crosswires)
    print(laplacian)
    plt.imshow(laplacian)
    plt.show()





if __name__ == '__main__':
    main()
