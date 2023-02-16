#!/usr/bin/env python3

from parser import parse_moves, parse_boards


class BingoBoard(object):
    def __init__(self, board):
        self.board = board

    def use_value(self, value: int):
        for row in self.board:
            for col in row:
                if col["value"] == value:
                    col["used"] = True

    def is_solved(self) -> bool:
        # check all rows
        for row in self.board:
            if all(map(lambda cell: cell["used"], row)):
                return True

        # check all columns
        for i in range(0,5):
            col = [row[i]["used"] for row in self.board]
            if all(col):
                return True
            
        # no solution found
        return False

    def score(self, value: int) -> int:
        sum = 0
        
        # sum of all un-used cells
        for row in self.board:
            for col in row:
                if not col["used"]:
                    sum += col["value"]

        # multiply the sum of un-used cells times value
        return sum * value


data_file = "./2021/day04/data/full"
moves = parse_moves(data_file)

last_board = -1
last_move = -1
last_score = -1

for b, raw in enumerate(parse_boards(data_file)):
    board = BingoBoard(raw)

    # play the moves until the board is solved
    for m, move in enumerate(moves):
        board.use_value(move)
        solved = board.is_solved()

        if solved:
            if m > last_move:
                print(f"{b} at move {m} with {move}")
                last_move = m
                last_board = b
                last_score = board.score(move)
            break
            

print(f"last board: {last_board}, move: {last_move}, value: {moves[last_move]}, score: {last_score}")