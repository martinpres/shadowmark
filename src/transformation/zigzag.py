import numpy as np

_GO_BACK = -1
_STAY = 0
_GO_FORWARD = 1

_RIGHT = (_GO_FORWARD, _STAY)
_DOWN = (_STAY, _GO_FORWARD)
_DOWN_LEFT = (_GO_BACK, _GO_FORWARD)
_UP_RIGHT = (_GO_FORWARD, _GO_BACK)


def _traverse(shape: tuple[int, int]) -> tuple[int, int]:
    rows, cols = shape

    if rows == 1:
        yield from [(x, 0) for x in range(0, cols)]
        return

    if cols == 1:
        yield from [(0, y) for y in range(0, rows)]
        return

    x = 0
    y = 0

    xm = cols - 1
    yn = rows - 1

    direction = _RIGHT

    while x < cols and y < rows:
        yield x, y

        dx, dy = direction
        x += dx
        y += dy

        if direction == _RIGHT:
            if y == 0:
                direction = _DOWN_LEFT
            elif y >= yn:
                direction = _UP_RIGHT
            elif x >= xm:
                direction = _DOWN
            else:
                raise RuntimeError("Illegal movement to the right occurred")

        elif direction == _DOWN_LEFT:
            if x > 0 and y < yn:
                direction = _DOWN_LEFT
            elif x == 0 and y < yn:
                direction = _DOWN
            elif y >= yn:
                direction = _RIGHT
            else:
                raise RuntimeError("Illegal movement to the down-left occurred")

        elif direction == _DOWN:
            if x == 0:
                direction = _UP_RIGHT
            elif x >= xm:
                direction = _DOWN_LEFT
            else:
                raise RuntimeError("Illegal movement down occurred")

        elif direction == _UP_RIGHT:
            if x < xm and y > 0:
                direction = _UP_RIGHT
            elif x < xm and y == 0:
                direction = _RIGHT
            elif x >= xm:
                direction = _DOWN
            else:
                raise RuntimeError("Illegal movement to the up-right occurred")


def scan(matrix: np.ndarray) -> np.ndarray:
    """
    Traverse a 2D matrix and convert its elements into a 1D array. The elements of the matrix are traversed in a
    zigzag fashion by simply walking through the matrix while reading its elements and deciding on each step which
    way to go next.

    :param matrix: A 2D numpy array representing the input matrix.
    :return: A 1D numpy array containing elements from the matrix collected by the zigzag traversal.
    """
    return np.array([matrix[y][x].item() for x, y in _traverse(matrix.shape[0:2])])


def inverse(vector: list | np.ndarray, shape: tuple[int, int]) -> np.ndarray:
    """
    Reconstruct a 2D matrix from 1D vector and a desired shape. The matrix is reconstructed in a zigzag fashion by
    traversing empty matrix and putting elements from the input vector to respective coordinates.

    :param vector: A 1D vector containing the elements to reshape into a matrix.
    :param shape:  A tuple specifying the shape (rows, cols) of the desired output matrix.
    :raises ValueError: If the size of the vector does not match `rows * cols`.
    :return:
    """
    rows, cols = shape[0:2]

    if len(vector) != rows * cols:
        raise ValueError('Size of the input vector must be equal to rows * cols')

    matrix = np.empty(shape)

    for i, (x, y) in enumerate(_traverse(shape)):
        matrix[y][x] = vector[i]

    return matrix
