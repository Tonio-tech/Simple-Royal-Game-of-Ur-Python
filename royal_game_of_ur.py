"""
File:    royal_game_of_ur.py
Author:  Toni Olafunmiloye
Date:    11/15/20
Section: 41
E-mail:  oolafun1@umbc.edu
Description: This file is a project that implements an old game, the Royal Game of Ur
"""

from sys import argv
from random import choice
from board_square import BoardSquare, UrPiece

P1 = 0
P2 = 1
# player 1 (white player) and player 2 (black player), numbers are for the players list


class RoyalGameOfUr:
    STARTING_PIECES = 7
    WHITE = "White"
    BLACK = "Black"

    def __init__(self, board_file_name):
        self.board = None
        self.load_board(board_file_name)
        self.WhiteStarts = []  # [3, 0]
        self.WhiteEnds = []  # [6, 0]
        self.BlackStarts = []  # [3, 2]
        self.BlackEnds = []  # [6, 2]

    def load_board(self, board_file_name):
        """
        This function takes a file name and loads the map, creating BoardSquare objects in a grid.

        :param board_file_name: the board file name
        :return: sets the self.board object within the class
        """

        import json
        try:
            with open(board_file_name) as board_file:
                board_json = json.loads(board_file.read())
                self.num_pieces = self.STARTING_PIECES
                self.board = []
                for x, row in enumerate(board_json):
                    self.board.append([])
                    for y, square in enumerate(row):
                        self.board[x].append(BoardSquare(x, y, entrance=square['entrance'], _exit=square['exit'], rosette=square['rosette'], forbidden=square['forbidden']))

                for i in range(len(self.board)):
                    for j in range(len(self.board[i])):
                        if board_json[i][j]['next_white']:
                            x, y = board_json[i][j]['next_white']
                            self.board[i][j].next_white = self.board[x][y]
                        if board_json[i][j]['next_black']:
                            x, y = board_json[i][j]['next_black']
                            self.board[i][j].next_black = self.board[x][y]
        except OSError:
            print('The file was unable to be opened. ')

    def draw_block(self, output, i, j, square):
        """
        Helper function for the display_board method
        :param output: the 2d output list of strings
        :param i: grid position row = i
        :param j: grid position col = j
        :param square: square information, should be a BoardSquare object
        """
        MAX_X = 8
        MAX_Y = 5
        for y in range(MAX_Y):
            for x in range(MAX_X):
                if x == 0 or y == 0 or x == MAX_X - 1 or y == MAX_Y - 1:
                    output[MAX_Y * i + y][MAX_X * j + x] = '+'
                if square.rosette and (y, x) in [(1, 1), (1, MAX_X - 2), (MAX_Y - 2, 1), (MAX_Y - 2, MAX_X - 2)]:
                    output[MAX_Y * i + y][MAX_X * j + x] = '*'
                if square.piece:
                    # print(square.piece.symbol)
                    output[MAX_Y * i + 2][MAX_X * j + 3: MAX_X * j + 5] = square.piece.symbol

    def display_board(self):
        """
        Draws the board contained in the self.board object

        """
        if self.board:
            output = [[' ' for _ in range(8 * len(self.board[i//5]))] for i in range(5 * len(self.board))]
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    if not self.board[i][j].forbidden:
                        self.draw_block(output, i, j, self.board[i][j])

            print('\n'.join(''.join(output[i]) for i in range(5 * len(self.board))))

    def roll_d4_dice(self, n=4):
        """
        Keep this function as is.  It ensures that we'll have the same runs with different random seeds for rolls.
        :param n: the number of tetrahedral d4 to roll, each with one dot on
        :return: the result of the four rolls.
        """
        dots = 0
        for _ in range(n):
            dots += choice([0, 1])
        return dots

    def play_game(self):
        """
            Your job is to recode this function to play the game.
        """
        self.find_starting_square()
        # in order to effectvely switch players
        players = [white_player, black_player]
        current_player = P1
        
        # the pieces
        W1 = UrPiece("White", "W1")
        W2 = UrPiece("White", "W2")
        W3 = UrPiece("White", "W3")
        W4 = UrPiece("White", "W4")
        W5 = UrPiece("White", "W5")
        W6 = UrPiece("White", "W6")
        W7 = UrPiece("White", "W7")

        B1 = UrPiece("Black", "B1")
        B2 = UrPiece("Black", "B2")
        B3 = UrPiece("Black", "B3")
        B4 = UrPiece("Black", "B4")
        B5 = UrPiece("Black", "B5")
        B6 = UrPiece("Black", "B6")
        B7 = UrPiece("Black", "B7")

        white_player_pieces = [W1, W2, W3, W4, W5, W6, W7]
        black_player_pieces = [B1, B2, B3, B4, B5, B6, B7]



        # in order to keep going until the game is over
        game_is_not_over = True
        while game_is_not_over:
            self.display_board()
            self.take_turn(current_player, players, white_player_pieces, black_player_pieces)

            # how to make sure that all 7 pieces are completed/ off the board
            white_completion_count = 0
            black_completion_count = 0
            if current_player == P1:
                for i in range(len(white_player_pieces)):
                    if white_player_pieces[i].complete == True:
                        white_completion_count += 1
                if white_completion_count == 7:
                    game_is_not_over = False
                    self.display_board()
                    self.game_over(white_completion_count, black_completion_count)
                current_player = P2
            else:
                for i in range(len(black_player_pieces)):
                    if black_player_pieces[i].complete == True:
                        black_completion_count += 1
                if black_completion_count == 7:
                    game_is_not_over = False
                    self.display_board()
                    self.game_over(white_completion_count, black_completion_count)
                current_player = P1

            # self.piece_display(players, current_player, num_moves)

            # white goes first
            # roll the dice
            # print the roll
            # print out pieces
            # ask player which piece to move
            # move the piece/ display new board
            # switch turn/

            # black goes
            # roll the dice
            # print the roll
            # print out pieces
            # ask player which piece to move
            # move the piece/ display new board
            # switch turn/
            # white goes

    def piece_display(self, players, current_player, white_player_pieces, black_player_pieces):
        """
        Displays all of the avliable pieces and there positions for each player
        :param players: list of players
        :param current_player: either white_player or black_player
        :param white_player_pieces: a list of all the white players pieces
        :param black_player_pieces: a list of all the black players pieces
        :return: it prints out a list of all avalibale moves the player can make
        """
        # shows which pieces are off or on the board,
        # if on the board then shows the position

        # if its the white players turn, display all their pieces
        if players[current_player] == white_player:
            for i in range(self.STARTING_PIECES):
                # if the piece isnt on the board, say currently off the board
                if white_player_pieces[i].position == None:
                    print(i + 1, white_player_pieces[i].symbol, "is currently off the board")
                # if it on the board, display the position of the piece
                else:
                    print(i + 1, white_player_pieces[i].symbol, white_player_pieces[i].position.position)
        # do the same with the black player
        else:
            for i in range(self.STARTING_PIECES):
                if black_player_pieces[i].position == None:
                    print(i + 1, black_player_pieces[i].symbol, "is currently off the board")
                else:
                    print(i + 1, black_player_pieces[i].symbol, black_player_pieces[i].position.position)


    def take_turn(self, current_player, players, white_player_pieces, black_player_pieces):
        """
        Notifies each player of their rolls and goes to shows their pieces, then goes to move them
        :param current_player: either white or black player
        :param players: list of players
        :param white_player_pieces: list of available pieces of white player
        :param black_player_pieces: list of available pieces of black player
        :return:
        """
        roll = self.roll_d4_dice(n=4)
        print("You rolled a", roll)
        num_moves = roll
        # display the avaliable pieces
        self.piece_display(players, current_player, white_player_pieces, black_player_pieces)
       # then move the chosen piece
        self.player_move(current_player, players, num_moves, white_player_pieces, black_player_pieces)


    def player_move(self, current_player, players, num_moves, white_player_pieces, black_player_pieces):
        """
        :param current_player: either the white or black player
        :param num_moves: the roll the player gets
        :param white_player_pieces: a list of white pieces chosen by the player to move
        :param black_player_pieces: a list of black pieces chosen by the player to move
        :return: the board
        """
        # current position is supposed to be a boardsquare,
        # set .position to the boardsquare instance that you're on

        # player chooses which piece they wanna move
        which_move = int(input("Which move do you which to make? "))

        if current_player == P1:
            piece = white_player_pieces[which_move - 1]
        else:
            piece = black_player_pieces[which_move - 1]

        # if the roll is 0, they cant move
        if num_moves == 0:
            return

        cant_move_count = 0
        while (piece.can_move(num_moves)) != True:
            print("You cannot move that piece.")
            cant_move_count += 1
            which_move = int(input("Which move do you which to make? "))
            if current_player == P1:
                piece = white_player_pieces[which_move - 1]
            else:
                piece = black_player_pieces[which_move - 1]
            if cant_move_count == 7:
                print("you cannot move any pieces")
                return

        current_position = piece.position

        if piece.complete == True:
            # if the piece completed th eboard, ut cant move anymore
            print("This piece has completed the board.")
            return

        # If you are off the board, and you can move onto the board at the white starting position,
        # and you can move num_moves - 1 additional times (moving onto the board counts as a move),
        # then you can move.  You can move there as long as it's unoccupied or occupied by an opponent's piece (except rule 5).
        if current_position == None:
            if piece.color == self.WHITE:
                # set it to the entrance first
                current_position = self.WhiteStarts

            else:
                current_position = self.BlackStarts
            num_moves -= 1

        # you have to set the piece to none to reset it because its no longer on that square anymore
        current_position.piece = None

        for i in range(num_moves):
            # If you are on the board, and you can move to the next position num_moves times, then you can move,
            # if the position is unoccupied or occupied by an opponent's piece (except rule 5).
            if current_position != None:
                # If you can move to the end position and have one move left, then you can move
                # (and you would then leave the board, that piece would have completed its course.
                # Also, watch out for this, the prof told us that when a piece actually moves off of a square
                # you've got to change that square's piece to None. otherwise, it'll keep showing the piece there.
                last_square = current_position.exit or (not current_position.next_white and not current_position.next_black)
                if last_square and num_moves - i == 1:
                    if piece.color == self.WHITE:
                        current_position = self.WhiteEnds
                        # have to get it off the board
                        current_position = None
                        # and then set it to complete
                        piece.complete = True
                        # no longer on the board

                    else:
                        current_position = self.BlackEnds
                        current_position = None
                        piece.complete = True
                elif last_square:
                    return

                if piece.color == self.WHITE:
                    if piece.complete == True:
                        # if the piece has just completed the board, then dont do next_white
                        return
                    else:
                        current_position = current_position.next_white
                    # piece.position = current_position
                    # piece.position = piece.position.next_white

                if piece.color == self.BLACK:
                    if piece.complete == True:
                        return
                    else:
                        current_position = current_position.next_black



        # If you are on or off the board, and you would land on your own piece by moving, then you cannot move.
        if current_position.piece:
            # if the piece color is the same color as the piece on the square, they cant move there
            if piece.color == current_position.piece.color:
                print("You cannot move here, your piece is already on that square")
                which_move = int(input("Which move do you which to make? "))
            if piece.color != current_position.piece.color:
                # If you try to move onto a piece of opposing color,
                # but that position is on a rosette, then you cannot move there.
                if current_position.rosette == True:
                    which_move = int(input("Which move do you which to make? "))
                else:
                    # if its not a rosette, you can capture the piece
                    current_position.piece.position = None
                    current_position.piece = piece
                    piece.position = current_position
        else:
            # once they know if they can move, then they move to that position
            piece.position = current_position
            current_position.piece = piece
            # if they land on a rossette, they get another turn
            if piece.position.rosette == True:
                self.display_board()
                print("You landed on a rosette and get another turn!")
                self.take_turn(current_player, players, white_player_pieces, black_player_pieces)



    def game_over(self, white_completion_count, black_completion_count):
        """
        If all 7 pieces pass the exit, then the game is over
        :param white_completion_count: the amount of white pieces that have completed the game
        :param black_completion_count: the amount of black pieces that have completed the game
        :return:
        """
        # if all 7 piece pass the exit, then game over
        if white_completion_count == 7:
            print("Game over, white player has one, black has lost")
        if black_completion_count == 7:
            print("Game over, black player has one, white has lost")



    def find_starting_square(self):
        """
        iterate through self.board to find start and ending square
        :return:
        """
        # its a 2D list so i and j are needed
        # After they’ve been found, you let the appropriate pieces know what their entrance square is
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                # print(self.board[i][j].entrance)
                # if the entrance == "white" then make that the white starting position
                if self.board[i][j].entrance == self.WHITE:
                    self.WhiteStarts = self.board[i][j]

                if self.board[i][j].entrance == self.BLACK:
                    self.BlackStarts = self.board[i][j]

                # find the exits, and set them
                if self.board[i][j].exit == self.WHITE:
                    self.WhiteEnds = self.board[i][j]
                if self.board[i][j].exit == self.BLACK:
                    self.BlackEnds = self.board[i][j]



if __name__ == '__main__':
    file_name = input('What is the file name of the board json? ') if len(argv) < 2 else argv[1]

        # get some player names, establish white/black player
    white_player = input("What is your name? ")
    print(white_player, "you will play as white.")
    black_player = input("What is your name? ")
    print(black_player, "you will play as black.")


    
    rgu = RoyalGameOfUr(file_name)
    rgu.play_game()


    # what is None? just nothing, no value, evaluates to false
# board square represents a square on the board
# create functions for: playing a turn for a player (color of player, dice roll)
#                       displaying a list of pieces a player can move and their positions
#                       determining whether a player can move at all
#                       moving a piece
#                       checking if the game is over
#                       finding starting squares
# UrPiece.can_move(): only does if it can move or not, doesnt actually move
# self.position.piece = self, means its gonna display the current pieces on the board
# do a loop through self.board to find a white or black entrance or exit
# entering the board, find starting position and move it one place
# move one square at a time however many times, a loop. if u roll a 3, do .next_white 3 times,
# for i in range(num_moves): self.position = self.position.next_white, s
# self.piece.position will give a board square
# position.peice is the piece on the board
