import numpy as np
import random
import pygame
import sys
import math


# minimax class with alpha beta pruning

class MinimaxAgent:
    # default depth of 5, but can be changed
    def __init__(self, depth=5):
        self.name= "Minimax"
        self.depth = depth
        self.ROW_COUNT = 6
        self.COLUMN_COUNT = 7
        self.WINDOW_LENGTH = 4
    
    # evaluate a window. A window is a all straight lines ( horizantal, vertical and diagonal)
    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = 1 if piece == 2 else 2

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(0) == 1:
            score -= 4

        return score

    # give a score for the current position by looking through all possible directions
    def score_position(self, board, piece):
        score = 0

        # Center column gets extra reward
        center_array = [int(i) for i in list(board[:, self.COLUMN_COUNT//2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        # Horizontal
        for r in range(self.ROW_COUNT):
            row_array = [int(i) for i in list(board[r,:])]
            for c in range(self.COLUMN_COUNT-3):
                window = row_array[c:c+self.WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        # Vertical
        for c in range(self.COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:,c])]
            for r in range(self.ROW_COUNT-3):
                window = col_array[r:r+self.WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        # Positive diagonal
        for r in range(self.ROW_COUNT-3):
            for c in range(self.COLUMN_COUNT-3):
                window = [board[r+i][c+i] for i in range(self.WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        # Negative diagonal
        for r in range(self.ROW_COUNT-3):
            for c in range(self.COLUMN_COUNT-3):
                window = [board[r+3-i][c+i] for i in range(self.WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        return score

    # find all valid locations
    def get_valid_locations(self, board):
        valid_locations = []
        for col in range(self.COLUMN_COUNT):
            if board[self.ROW_COUNT-1][col] == 0:
                valid_locations.append(col)
        return valid_locations
    
    # Check if its a winning move or if the board is full ( in that case we can stop the search)
    def is_terminal_node(self, board):
        def winning_move(piece):
            # Horizontal
            for c in range(self.COLUMN_COUNT-3):
                for r in range(self.ROW_COUNT):
                    if board[r][c] == piece and board[r][c+1] == piece and \
                       board[r][c+2] == piece and board[r][c+3] == piece:
                        return True

            # Vertical
            for c in range(self.COLUMN_COUNT):
                for r in range(self.ROW_COUNT-3):
                    if board[r][c] == piece and board[r+1][c] == piece and \
                       board[r+2][c] == piece and board[r+3][c] == piece:
                        return True

            # Diagonals
            for c in range(self.COLUMN_COUNT-3):
                for r in range(self.ROW_COUNT-3):
                    if board[r][c] == piece and board[r+1][c+1] == piece and \
                       board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                        return True

            for c in range(self.COLUMN_COUNT-3):
                for r in range(3, self.ROW_COUNT):
                    if board[r][c] == piece and board[r-1][c+1] == piece and \
                       board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                        return True
            return False

        return winning_move(1) or winning_move(2) or len(self.get_valid_locations(board)) == 0

    # the main minimax logic. Lets look through it
    # I think it alternates between maximizingPlayer and else, until alpha and beta are equal.
    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        #
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:

            # if its a end node, check who won
            if is_terminal:
                if self.winning_move(board, 2):
                    return (None, 100000000000000)
                elif self.winning_move(board, 1):
                    return (None, -10000000000000)
                else:
                    return (None, 0)
            else:
                return (None, self.score_position(board, 2))

        if maximizingPlayer:
            value = float('-inf')
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy = board.copy()
                self.drop_piece(b_copy, row, col, 2)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:
            value = float('inf')
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy = board.copy()
                self.drop_piece(b_copy, row, col, 1)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    # find a open_row to place the piece vertically
    def get_next_open_row(self, board, col):
        for r in range(self.ROW_COUNT):
            if board[r][col] == 0:
                return r

    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece

    # this winning move is used by the main minimax algorrithm with self.winning_move()
    # I think this is duplicated in is_terminal_node but its not a big issue since this one uses self

    def winning_move(self, board, piece):
        # Horizontal
        for c in range(self.COLUMN_COUNT-3):
            for r in range(self.ROW_COUNT):
                if board[r][c] == piece and board[r][c+1] == piece and \
                   board[r][c+2] == piece and board[r][c+3] == piece:
                    return True

        # Vertical
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c] == piece and \
                   board[r+2][c] == piece and board[r+3][c] == piece:
                    return True

        # Diagonals
        for c in range(self.COLUMN_COUNT-3):
            for r in range(self.ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c+1] == piece and \
                   board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                    return True

        for c in range(self.COLUMN_COUNT-3):
            for r in range(3, self.ROW_COUNT):
                if board[r][c] == piece and board[r-1][c+1] == piece and \
                   board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                    return True
        return False

    # find_move
    #the main function
    def find_move(self, board):
        col, _ = self.minimax(board, self.depth, float('-inf'), float('inf'), True)
        return col