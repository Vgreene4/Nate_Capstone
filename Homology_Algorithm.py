import numpy as np

def low(matrix, j):
    col = matrix[:, j]
    indices = np.where(col == 1)[0]
    return max(indices) if indices.size > 0 else -1

def process_matrix(matrix):
    n = matrix.shape[1]  # Number of columns

    for j in range(1, n):  # Iterate through columns from 1 to n-1
        while True:
            found = False
            low_j = low(matrix, j)

            for i in range(j):
                if low(matrix, i) == low_j and low_j != -1:
                    matrix[:, j] = (matrix[:, j] + matrix[:, i]) % 2  # Binary addition (mod 2)
                    print("{} + {}".format(j+1, i+1))
                    found = True
                    break  # Restart checking since column j changed

            if not found:
                break  # No more conflicts for column j

    return matrix

#executing/testing
            #  a  b  c  d bd  e ab ac cd ad abd
D = np.array([[0, 0, 0, 0, 0, 0, 1 ,1, 0, 1, 0],
              [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

R = process_matrix(D)
print(R)