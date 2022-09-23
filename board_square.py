"""
File:    board_square.py
Author:  Toni Olafunmiloye
Date:    11/15/20
Section: 41
E-mail:  oolafun1@umbc.edu
Description: This file implements an old game, the Royal Game of Ur
"""

class UrPiece:
    def __init__(self, color, symbol):
        self.color = color
        self.position = None
        self.complete = False
        self.symbol = symbol

    def can_move(self, num_moves):
        """
        :param num_moves: number of possible moves
        :return: True or False
        """
        current_position = self.position
        WHITE = "White"
        BLACK = "Black"

        if num_moves == 0:
            return False

        if self.complete == True:
            return False

        if current_position == None:
            if self.color == WHITE:
                # current_position = self.WhiteStarts
                num_moves -= 1
                return True
            else :
                # current_position = self.BlackStarts
                num_moves -= 1
                return True

        for i in range(num_moves):
            # If you are on the board, and you can move to the next position num_moves times, then you can move,
            # if the position is unoccupied or occupied by an opponent's piece (except rule 5).
            if current_position != None:
                # If you can move to the end position and have one move left, then you can move
                # (and you would then leave the board, that piece would have completed its course.
                last_square = current_position.exit or (not current_position.next_white and not current_position.next_black)
                if last_square and num_moves - i == 1:
                    if self.color == WHITE:
                        # self.position = self.WhiteEnds
                        # self.complete = True
                        return True
                    if self.color == BLACK:
                        # self.position = self.BlackEnds
                        # self.complete = True
                        return True
                elif last_square:
                    return False

                if self.color == WHITE:
                    current_position = current_position.next_white
                else:
                    current_position = current_position.next_black

            # If you are off the board, and you can move onto the board at the white starting position,
            # and you can move num_moves - 1 additional times (moving onto the board counts as a move),
            # then you can move.  You can move there as long as it's unoccupied or occupied by an opponent's piece (except rule 5).



        # If you are on or off the board, and you would land on your own piece by moving, then you cannot move.
        if current_position.piece:
            if self.color == current_position.piece.color:
                return False
            if self.color != current_position.piece.color:
                # If you try to move onto a piece of opposing color,
                # but that position is on a rosette, then you cannot move there.
                if current_position.rosette == True:
                    return False
                else:
                    return True
        else:
            return True





class BoardSquare:
    def __init__(self, x, y, entrance=False, _exit=False, rosette=False, forbidden=False):
        self.piece = None
        self.position = (x, y)
        self.next_white = None
        self.next_black = None
        self.exit = _exit
        self.entrance = entrance
        self.rosette = rosette
        self.forbidden = forbidden

    def load_from_json(self, json_string):
        import json
        loaded_position = json.loads(json_string)
        self.piece = None
        self.position = loaded_position['position']
        self.next_white = loaded_position['next_white']
        self.next_black = loaded_position['next_black']
        self.exit = loaded_position['exit']
        self.entrance = loaded_position['entrance']
        self.rosette = loaded_position['rosette']
        self.forbidden = loaded_position['forbidden']

    def jsonify(self):
        next_white = self.next_white.position if self.next_white else None
        next_black = self.next_black.position if self.next_black else None
        return {'position': self.position, 'next_white': next_white, 'next_black': next_black, 'exit': self.exit, 'entrance': self.entrance, 'rosette': self.rosette, 'forbidden': self.forbidden}
