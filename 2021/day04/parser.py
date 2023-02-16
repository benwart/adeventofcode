def parse_strs(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()

def parse_moves(filepath):
    with open(filepath) as f:
        line = f.readline()

    return [int(move) for move in line.split(",")]


def parse_boards(filepath):
    # skip the first row of moves
    data = parse_strs(filepath)
    next(data)

    board = []

    for line in data:

        # skip blank lines and clear the board
        if len(line) == 0:
            # reset board
            board = []
            continue

        # add row to board converting to ints as we go
        board.append([{"value": int(v), "used": False} for v in [int(v) for v in line.split(" ") if len(v.strip()) > 0]])

        # check if we should yield a board
        if len(board) == 5:
            yield board