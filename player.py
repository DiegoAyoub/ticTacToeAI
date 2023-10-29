import math
import random

class Player:
    def __init__(self, letter):
        # letter = x, o
        self.letter = letter

    # we want all players to get their next move given a game
    def get_move(self, game):
        pass

class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        # random valid spot for next move
        square = random.choice(game.available_moves())
        return square

class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-8):' )
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True #great success

            except ValueError:
                print('Invalid square. Please try again')

        return val

class GeniusComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self,game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())
        else:
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter #yourself!
        other_player = 'O' if player == 'X' else 'X'

        if state.current_winner == other_player:

            return { 'position' : None,
                     'score' : 1 * (state.num_empty_squares() + 1) if other_player == max_player
                     else -1 * (state.num_empty_squares() + 1) }

        elif not (state.empty_squares()):
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf} #each score we should maximize
        else:
            best = {'position': None, 'score': math.inf}

        for possible_move in state.available_moves():
            #1. move to 1 spot
            #print("INCOMMING")
            #print(possible_move)
            state.make_move(possible_move, player)
            #2 recurse using minimax to simulate a game after making that move
            sim_score = self.minimax(state, other_player)
            #3 undo move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move
            #4 update dictionaries if necessary
            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score

        return best
