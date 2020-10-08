"""Console game - tic-tac-toe"""
from random import randint
import argparse
import os


class TicTacGame:
    """Realizes the game of tic-tac-toe."""
    _ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    _NUMBERS = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def __init__(self, height=3, width=3):
        """Form board for the game.

        Keyword arguments:
            height -- height of the field of play
            width -- width of the field of play

        Exceptions:
            ValueError - if received incorrect height or width
        """
        self._width = width
        self._height = height
        if self._width < 3 or self._width > 9:
            raise ValueError
        if self._height < 3 or self._height > 9:
            raise ValueError
        self._matrix = []
        for _ in range(self._height):
            line = []
            for _ in range(self._width):
                line.append(0)
            self._matrix.append(line)

    def show_board(self):
        """Draw current situation on the playing field."""
        print(' ', end='')
        for j in range(self._width):
            print(' {}'.format(self._ALPHABET[j]), end='')
        print()
        print(' ', end='')
        print(' ─'*self._width)
        for i in range(self._height):
            print('{}│'.format(self._NUMBERS[i]), end='')
            for j in range(self._width):
                if self._matrix[i][j] == 0:
                    print(' │', end='')
                elif self._matrix[i][j] == 1:
                    print('X│', end='')
                elif self._matrix[i][j] == 2:
                    print('0│', end='')
            print()
            print(' ', end='')
            print(' ─'*self._width)

    def move_reading(self):
        """Read and validate move.

        Returns:
            tuple of validated move in self._matrix coordinates
        """
        while True:
            field = input('Enter field: ')
            try:
                h_coord, w_coord = self.validate_move(field)
            except ValueError:
                os.system('clear')
                print('Input error, try again')
                print('Field is expected in the format "LetterNumber"')
                self.show_board()
            else:
                break
        return (h_coord-1, self._ALPHABET.index(w_coord))

    def validate_move(self, field):
        """Validate move.

        Keyword arguments:
            field -- not validated user move

        Exceptions:
            ValueError -- if user move has not been validated

        Returns:
            tuple of validated move in board coordinates
        """
        if len(field) != 2:
            raise ValueError
        w_coord = field[0].upper()
        h_coord = int(field[1])
        if w_coord not in self._ALPHABET[:self._width]:
            raise ValueError
        if h_coord not in self._NUMBERS[:self._height]:
            raise ValueError
        if self._matrix[h_coord-1][self._ALPHABET.index(w_coord)] != 0:
            raise ValueError
        return (h_coord, w_coord)

    def start_pvp_game(self):
        """Realizes the game of two people."""
        os.system('clear')
        for i in range(self._width*self._height):
            print('Field is expected in the format "LetterNumber"')
            self.show_board()
            h_index, w_index = self.move_reading()
            self._matrix[h_index][w_index] = i % 2 + 1
            os.system('clear')
            if self.check_winner(h_index, w_index):
                self.show_board()
                if i % 2 == 0:
                    print('First player wins')
                else:
                    print('Second player wins')
                return
        self.show_board()
        print('Draw')

    def start_pve_game(self):
        """Realizes the game of man against ai_player."""
        os.system('clear')
        priority = randint(0, 1)
        for i in range(self._width*self._height):
            print('Field is expected in the format "LetterNumber"')
            self.show_board()
            if priority == 1:
                priority -= 1
                h_index, w_index = self.move_reading()
            elif priority == 0:
                priority += 1
                h_index, w_index = self.ai_player()
            self._matrix[h_index][w_index] = i % 2 + 1
            os.system('clear')
            if self.check_winner(h_index, w_index):
                self.show_board()
                if priority == 0:
                    print('Player wins')
                elif priority == 1:
                    print('AI wins')
                return
        self.show_board()
        print('Draw')

    def check_winner(self, h_index, w_index):
        """Check existing a winning line.

        Keyword arguments:
            h_index -- last move height index
            w_index -- last move width index

        Returns:
            True -- if move is winning
            False -- if move is not winning
        """
        check_list = self.determine_check_list(h_index, w_index)
        for check_set in check_list:
            if check_set in ({1}, {2}):
                return True
        return False

    def determine_check_list(self, h_index, w_index):
        """Aggregates all lines that need to be checked for winning.

        Keyword arguments:
            h_index -- last move height index
            w_index -- last move width index

        Returns:
            check_list -- list of sets composed of board elements lying on
             line that we want check for winning
        """
        check_list = []
        if h_index > 1:
            check_list.append({self._matrix[h_index-i][w_index]
                               for i in range(3)})
        if h_index > 1 and w_index < self._width - 2:
            check_list.append({self._matrix[h_index-i][w_index+i]
                               for i in range(3)})
        if w_index < self._width - 2:
            check_list.append({self._matrix[h_index][w_index+i]
                               for i in range(3)})
        if h_index < self._height - 2 and w_index < self._width - 2:
            check_list.append({self._matrix[h_index+i][w_index+i]
                               for i in range(3)})
        if h_index < self._height - 2:
            check_list.append({self._matrix[h_index+i][w_index]
                               for i in range(3)})
        if h_index < self._height - 2 and w_index > 1:
            check_list.append({self._matrix[h_index+i][w_index-i]
                               for i in range(3)})
        if w_index > 1:
            check_list.append({self._matrix[h_index][w_index-i]
                               for i in range(3)})
        if h_index > 1 and w_index > 1:
            check_list.append({self._matrix[h_index-i][w_index-i]
                               for i in range(3)})
        if 0 < h_index < self._height - 1:
            check_list.append({self._matrix[h_index+i][w_index]
                               for i in range(-1, 2)})
        if 0 < h_index < self._height - 1 and 0 < w_index < self._width - 1:
            check_list.append({self._matrix[h_index+i][w_index-i]
                               for i in range(-1, 2)})
            check_list.append({self._matrix[h_index+i][w_index+i]
                               for i in range(-1, 2)})
        if 0 < w_index < self._width - 1:
            check_list.append({self._matrix[h_index][w_index+i]
                               for i in range(-1, 2)})
        return check_list

    def ai_player(self):
        """Simulation of an opponent.

        Returns:
            tuple -- computer move
        """
        moves_list = []
        for i in range(self._height):
            for j in range(self._width):
                if self._matrix[i][j] == 0:
                    moves_list.append((i, j))
        return moves_list[randint(0, len(moves_list)-1)]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple Tic-Tac-Toe game.')
    parser.add_argument('-t', '--type', default='pve',
                        choices=['pve', 'pvp'], type=str,
                        help='Type of game: pvp or pve.')
    parser.add_argument('--width', default=3,
                        choices=[3, 4, 5, 6, 7, 8, 9], type=int,
                        help='Width of game board.')
    parser.add_argument('--height', default=3,
                        choices=[3, 4, 5, 6, 7, 8, 9], type=int,
                        help='Height of game board.')
    args = parser.parse_args()
    game = TicTacGame(args.height, args.width)
    if args.type == 'pve':
        game.start_pve_game()
    elif args.type == 'pvp':
        game.start_pvp_game()
