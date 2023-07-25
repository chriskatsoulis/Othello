# Description: This is a text-based version of Othello. There is a class to represent an Othello game, and
#              its methods include: printing the current board, creating a player, returning a winner (or
#              declaring a tie), returning available positions (i.e. legal moves), making a move where the
#              board/scores are updated, validating whether a proposed move is legal or not, and play_game
#              that attempts to make a move for the player with the given color at the specified position.
#              Also, there is a class to represent a player in an Othello game with methods to initialize
#              the player's name and color, as well as getters and setters for both attributes.

class Othello:
    """A class to represent an Othello game. The Othello class will communicate with the Player
    class to facilitate player creation, player moves, etc. Methods include printing the current
    board, creating a player, returning a winner (or declaring a tie), returning available
    positions (i.e. legal moves), making a move where the board/scores are updated, validating
    whether a proposed move is legal or not, and play_game that attempts to make a move for the
    player with the given color at the specified position."""
    def __init__(self):
        """Initializes the game's title, board, score, and an empty list of players."""
        self._title = """   
   ____ _______ _    _ ______ _      _      ____  
  / __ \__   __| |  | |  ____| |    | |    / __ \ 
 | |  | | | |  | |__| | |__  | |    | |   | |  | |
 | |  | | | |  |  __  |  __| | |    | |   | |  | |
 | |__| | | |  | |  | | |____| |____| |___| |__| |
  \____/  |_|  |_|  |_|______|______|______\____/
  """
        self._board = [['.' for _ in range(10)] for _ in range(10)]
        self._board[4][4] = 'O'
        self._board[4][5] = 'X'
        self._board[5][4] = 'X'
        self._board[5][5] = 'O'
        self._position_flips = []
        self._black_score = 2
        self._white_score = 2
        self._players = []

        print(self._title)

    def print_board(self):
        """Prints out the current board, including the boundaries."""
        print('* * * * * * * * * *')
        for row in range(1, 9):
            print('*', end=' ')
            for col in range(1, 9):
                print(self._board[row][col], end=' ')
            for col in range(10, 11):
                print('*')
        print('* * * * * * * * * *')

    def create_player(self, player_name, piece_color):
        """Creates a Player object with the given name and color ("black" or "white") and
        adds it to the list of players."""
        player = Player(player_name, piece_color)
        self._players.append(player)

    def return_winner(self):
        """Returns the winner of the game or returns that the game is a tie."""
        for player in self._players:
            if player.get_piece_color() == "black":
                player_black = player.get_player_name()
            if player.get_piece_color() == "white":
                player_white = player.get_player_name()

        if self._black_score > self._white_score:
            return f"Winner is black player: {player_black}"
        elif self._white_score > self._black_score:
            return f"Winner is white player: {player_white}"
        else:
            return "It's a tie"

    def return_available_positions(self, color):
        """Returns a list of possible positions for the player with the given color to
        move on the current board."""
        available_positions = []
        for row in range(1, 9):
            for col in range(1, 9):
                position = self.valid_move_check(color, (row, col))
                if position is True:
                    available_positions.append((row, col))
        return available_positions

    def make_move(self, color, piece_position):
        """Puts a piece of the specified color at the given position and updates the board/scores
        accordingly, then returns the current board (as a 2d list). This method is an internal
        method and is meant to be called by play_game."""
        if self.valid_move_check(color, piece_position) is False:
            self._position_flips = []
            self.play_game(color, piece_position)

        if color == "black":
            your_color = 'X'
        if color == "white":
            your_color = 'O'
        row, col = piece_position

        self._board[row][col] = your_color

        for position in self._position_flips:
            row, col = position
            self._board[row][col] = your_color
        self._position_flips = []

        black_score = 0
        white_score = 0
        game_board = [[] for _ in range(8)]
        for row in range(1, 9):
            for element in self._board[row][1:9]:
                game_board[row - 1].append(element)
                if element == 'X':
                    black_score += 1
                if element == 'O':
                    white_score += 1
        self._black_score = black_score
        self._white_score = white_score
        return game_board

    def valid_move_check(self, color, piece_position):
        """Determines if a move is valid or not. Returns True if the move is valid, returns
        False if the move is invalid."""
        if color == "black":
            opponent_color = 'O'
            your_color = 'X'
        if color == "white":
            opponent_color = 'X'
            your_color = 'O'

        row, col = piece_position
        if 1 < row > 8:
            return False
        if 1 < col > 8:
            return False
        if self._board[row][col] != '.':
            return False

        flip_list_1 = []
        valid_end_1 = 0
        r1, c1 = piece_position
        while self._board[r1+1][c1] != '.':
            if self._board[r1+1][c1] == opponent_color:
                flip_list_1.append((r1+1, c1))
            if self._board[r1+1][c1] == your_color:
                valid_end_1 += 1
                break
            r1 += 1
        if len(flip_list_1) and valid_end_1 > 0:
            for position in flip_list_1:
                self._position_flips.append(position)

        flip_list_2 = []
        valid_end_2 = 0
        r2, c2 = piece_position
        while self._board[r2+1][c2+1] != '.':
            if self._board[r2+1][c2+1] == opponent_color:
                flip_list_2.append((r2+1, c2+1))
            if self._board[r2+1][c2+1] == your_color:
                valid_end_2 += 1
                break
            r2 += 1
            c2 += 1
        if len(flip_list_2) and valid_end_2 > 0:
            for position in flip_list_2:
                self._position_flips.append(position)

        flip_list_3 = []
        valid_end_3 = 0
        r3, c3 = piece_position
        while self._board[r3][c3+1] != '.':
            if self._board[r3][c3+1] == opponent_color:
                flip_list_3.append((r3, c3+1))
            if self._board[r3][c3+1] == your_color:
                valid_end_3 += 1
                break
            c3 += 1
        if len(flip_list_3) and valid_end_3 > 0:
            for position in flip_list_3:
                self._position_flips.append(position)

        flip_list_4 = []
        valid_end_4 = 0
        r4, c4 = piece_position
        while self._board[r4-1][c4+1] != '.':
            if self._board[r4-1][c4+1] == opponent_color:
                flip_list_4.append((r4-1, c4+1))
            if self._board[r4-1][c4+1] == your_color:
                valid_end_4 += 1
                break
            r4 -= 1
            c4 += 1
        if len(flip_list_4) and valid_end_4 > 0:
            for position in flip_list_4:
                self._position_flips.append(position)

        flip_list_5 = []
        valid_end_5 = 0
        r5, c5 = piece_position
        while self._board[r5-1][c5] != '.':
            if self._board[r5-1][c5] == opponent_color:
                flip_list_5.append((r5-1, c5))
            if self._board[r5-1][c5] == your_color:
                valid_end_5 += 1
                break
            r5 -= 1
        if len(flip_list_5) and valid_end_5 > 0:
            for position in flip_list_5:
                self._position_flips.append(position)

        flip_list_6 = []
        valid_end_6 = 0
        r6, c6 = piece_position
        while self._board[r6-1][c6-1] != '.':
            if self._board[r6-1][c6-1] == opponent_color:
                flip_list_6.append((r6-1, c6-1))
            if self._board[r6-1][c6-1] == your_color:
                valid_end_6 += 1
                break
            r6 -= 1
            c6 -= 1
        if len(flip_list_6) and valid_end_6 > 0:
            for position in flip_list_6:
                self._position_flips.append(position)

        flip_list_7 = []
        valid_end_7 = 0
        r7, c7 = piece_position
        while self._board[r7][c7-1] != '.':
            if self._board[r7][c7-1] == opponent_color:
                flip_list_7.append((r7, c7-1))
            if self._board[r7][c7-1] == your_color:
                valid_end_7 += 1
                break
            c7 -= 1
        if len(flip_list_7) and valid_end_7 > 0:
            for position in flip_list_7:
                self._position_flips.append(position)

        flip_list_8 = []
        valid_end_8 = 0
        r8, c8 = piece_position
        while self._board[r8+1][c8-1] != '.':
            if self._board[r8+1][c8-1] == opponent_color:
                flip_list_8.append((r8+1, c8-1))
            if self._board[r8+1][c8-1] == your_color:
                valid_end_8 += 1
                break
            r8 += 1
            c8 -= 1
        if len(flip_list_8) and valid_end_8 > 0:
            for position in flip_list_8:
                self._position_flips.append(position)

        if len(flip_list_1) and valid_end_1 > 0:
            return True
        elif len(flip_list_2) and valid_end_2 > 0:
            return True
        elif len(flip_list_3) and valid_end_3 > 0:
            return True
        elif len(flip_list_4) and valid_end_4 > 0:
            return True
        elif len(flip_list_5) and valid_end_5 > 0:
            return True
        elif len(flip_list_6) and valid_end_6 > 0:
            return True
        elif len(flip_list_7) and valid_end_7 > 0:
            return True
        elif len(flip_list_8) and valid_end_8 > 0:
            return True
        else:
            return False

    def play_game(self, player_color, piece_position):
        """Attempts to make a move for the player with the given color at the specified position.
        If the position the player wants to move is invalid, the function should not make any
        move and return "Invalid move", and also print out this message "Here are the valid
        moves:" followed by a list of possible positions. If no valid moves exist then the
        returned list is empty. If the position is valid, the function should make that move and
        update the board. If the game is ended at that point, the function should print "Game is
        ended white piece: number black piece: number" and call the return_winner method."""
        proposed_move = self.valid_move_check(player_color, piece_position)

        if proposed_move is False:
            if len(self.return_available_positions('black')) < 1:
                if len(self.return_available_positions('white')) < 1:
                    print(f"Game is ended white piece: {self._white_score} black piece: {self._black_score}")
                    print(self.return_winner())
            else:
                print(f"Here are the valid moves: {self.return_available_positions(player_color)}")
                return "Invalid move"
        else:
            self.make_move(player_color, piece_position)


class Player:
    """A class to represent a player in an Othello game. Methods to initialize the player's
    name and color, as well as getters and setters for both attributes. This class will
    communicate with the Othello class to facilitate player creation, player moves, etc."""
    def __init__(self, player_name, piece_color):
        """Initializes a player's name and color."""
        self._player_name = player_name
        self._piece_color = piece_color

    def get_player_name(self):
        """Returns a player's name."""
        return self._player_name

    def set_player_name(self, name):
        """Sets a player's name."""
        self._player_name = name

    def get_piece_color(self):
        """Returns a player's color."""
        return self._piece_color

    def set_piece_color(self, color):
        """Sets a player's color."""
        self._piece_color = color
