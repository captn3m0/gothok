import random

'''
Class for holding the entire
Kings Landing
'''


class Board(object):
    TOTAL_PLAYERS = 4
    GRID_SIZE = 6
    '''
    We use the following values for each card:
    '''
    STARK = 8
    GREYJOY = 7
    LANNISTER = 6
    TARGARYEN = 5
    BARATHEON = 4
    TYRELL = 3
    TULLY = 2
    VARYS = 1
    EMPTY = 0

    def start(self):
        '''
        Total 36 cards
        '''
        l = ([self.STARK] * 8) + ([self.GREYJOY] * 7) + \
            ([self.LANNISTER] * 6) + ([self.TARGARYEN] * 5) + \
            ([self.BARATHEON] * 4) + ([self.TYRELL] * 3) + \
            ([self.TULLY] * 2) + [self.VARYS]

        assert(len(l) == 36)

        random.shuffle(l)

        return {
            "board": [l[i:i+self.GRID_SIZE]
                      for i in range(0, len(l), self.GRID_SIZE)],
            "players": self.TOTAL_PLAYERS,
            "current_player": 0,
            "scores": [0] * self.TOTAL_PLAYERS,
            "cards": [[] for i in range(self.TOTAL_PLAYERS)]
        }

    def scores(self, cards):
        scores = [0] * self.TOTAL_PLAYERS
        '''
        >>> cards
        [[2, 3], [2, 2, 2], [1, 1, 1], [4, 2]]
        get the length of all the character list for each player
        where the house matches the given house (2)
        >>> [len(list(filter(lambda y: y==2, x))) for x in cards]
        [1, 3, 0, 1]
        '''
        for house in range(self.TULLY, self.STARK + 1):
            totals = [len(list(filter(lambda y: y == house, x)))
                      for x in cards]
            max_count = max(totals)
            # If only one player has the majority
            if totals.count(max_count) == 1:
                player_index = totals.index(max_count)
                scores[player_index] += 1
        return scores

    def display_state(self, state):
        print()
        lookup = ['-', 'V', 'U', 'Y', 'B', 'T', 'L', 'G', 'S']
        for row in state['board']:
            print("".join([lookup[card] for card in row]))

    def current_player(self, state):
        return state['current_player']

    # Takes the game state, and the move to be applied.
    # Returns the new game state.
    # play = (x,y)
    def next_state(self, state, move):
        x = move[0]
        y = move[1]
        current = state['current_player']

        # Check move is on the square board
        assert(0 <= x < self.GRID_SIZE)
        assert(0 <= y < self.GRID_SIZE)

        varys = self.find_varys(state)
        startx = varys[0]
        starty = varys[1]
        picked_card = state['board'][x][y]

        # The X or Y index must match
        assert(startx == x or starty == y)
        # But you can't move on Varys
        assert(picked_card != self.VARYS)
        # And you can't move on an empty spot
        assert(picked_card != self.EMPTY)

        # This enumerates all the x,y cords
        # that fall in Varys' path
        cards_attempted = []
        if (startx == x):
            left = min(y, starty)
            right = max(y, starty)
            # We want this to be inclusive
            cards_attempted = [(startx, yy) for yy in range(left, right + 1)]
            pass
        elif (starty == y):
            top = min(x, startx)
            bottom = max(x, startx)
            # We want this to be inclusive
            cards_attempted = [(xx, starty) for xx in range(top, bottom + 1)]
            pass
        else:
            raise Exception("Invalid move")

        for card_position in cards_attempted:
            row = card_position[0]
            col = card_position[1]
            card = state['board'][row][col]
            # If it is of the same house as declared
            if (card == picked_card):
                # Pick it up
                state['cards'][current].append(picked_card)
                state['board'][row][col] = self.EMPTY

        # Now we move Varys
        state['board'][x][y] = self.VARYS
        state['board'][startx][starty] = self.EMPTY

        # Whatever cards each player has
        state['scores'] = self.scores(state['cards'])

        # Fix the next player
        current = state['current_player'] = current + 1

        if current >= self.TOTAL_PLAYERS:
            state['current_player'] = 0
        return state

    def find_varys(self, state):
        for row_index, row in enumerate(state['board']):
            for column, card in enumerate(row):
                if (card == self.VARYS):
                    return (row_index, column)

        raise Exception("Invalid state, no Varys in game")

    # Takes a sequence of game states representing the full
    # game history, and returns the full list of moves that
    # are legal plays for the current player.
    def legal_plays(self, state_history):
        # In our simple case, past state is not required
        # to check for valid moves
        current_state = state_history[len(state_history) - 1]
        varys = self.find_varys(current_state)
        # For this, since the total number of possible moves
        # is just 10, we enumerate them all and then assign
        # them to a "direction,house bucket". This ensures
        # that only card from each house is picked for a specific
        # direction (and the furthest card at that)

        pass

    def winner(self, state_history):
        # Takes a sequence of game states representing the full
        # game history.  If the game is now won, return the player
        # number.  If the game is still ongoing, return zero.  If
        # the game is tied, return a different distinct value, e.g. -1.
        pass
