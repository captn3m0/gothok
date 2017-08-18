import random
import json

'''
Class for holding the entire
Kings Landing
'''


class Board(object):
    num_players = 4

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

    def unpack_state(self, state):
        return state

    def pack_action(self, play):
        return json.dumps(play)

    def unpack_action(self, play):
        return json.loads(play)

    def pack_state(self, state):
        return state

    def starting_state(self):
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
            "player": 1,
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

    def display(self, state, action, _unicode=True):
        ret = "\n"
        lookup = ['-', 'V', 'U', 'Y', 'B', 'T', 'L', 'G', 'S']
        for row in state['board']:
            ret += "".join([lookup[card] for card in row]) + "\n"

        return (ret)

    # Takes the game state, and the move to be applied.
    # Returns the new game state.
    # play = (x,y)
    def next_state(self, state, move):
        x = move[0]
        y = move[1]
        current = state['player'] - 1

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
        # Current always holds the index
        current = current + 1
        if current >= self.TOTAL_PLAYERS:
            current = 0

        state['player'] = current + 1

        return state

    def find_varys(self, state):
        for row_index, row in enumerate(state['board']):
            for column, card in enumerate(row):
                if (card == self.VARYS):
                    return (row_index, column)

        raise Exception("Invalid state, no Varys in game")

    def is_legal(self, history, action):
        state = history[-1]
        plays = self.legal_plays([state])
        return(action in state)

    # Takes a sequence of game states representing the full
    # game history, and returns the full list of moves that
    # are legal plays for the current player.
    def legal_plays(self, state_history):
        # In our simple case, past state is not required
        # to check for valid moves
        current_state = state_history[len(state_history) - 1]
        varys = self.find_varys(current_state)

        x = varys[0]
        y = varys[1]

        # Constant X = same row
        # Constant Y =  same column
        # These are all sorted lists starting from the card next
        # to varys and going to the edge of the board
        ranges = [
            list(reversed([(x, col) for col in range(0, x+1)])),   # Left
            [(x, col) for col in range(x+2, 6)],                   # Right
            list(reversed([(row, y) for row in range(0, y-1)])),   # Up
            [(row, y) for row in range(y, 6)]                      # Down
        ]

        ranges = [
            [
                (pos[0], pos[1])
                for pos in rrange
                # Remove any empty cards on the way
                if current_state['board'][pos[0]][pos[1]] != self.EMPTY
            ]
            for rrange
            # Remove some directions if we are the edge
            in ranges if len(rrange) > 0]

        # For this, since the total number of possible moves
        # is just 10, we enumerate them all and then assign
        # them to a "direction,house bucket". This ensures
        # that only card from each house is picked for a specific
        # direction (and the furthest card at that)

        final_ranges = [
            [[] for ii in range(self.TULLY, self.STARK+3)]
            for i in range(0, 4)]

        for index, rrange in enumerate(ranges):
            for pos in rrange:
                x = pos[0]
                y = pos[1]
                card = current_state['board'][x][y]
                final_ranges[index][card] = pos

        flatten = lambda l: [
            item for sublist in l
            for item in sublist if len(item) > 0]

        return(flatten(final_ranges))

    # Takes a sequence of game states representing the full
    # game history.  If the game is now won, return the player
    # number.  If the game is still ongoing, return zero.  If
    # the game is tied, return a different distinct value, e.g. -1.
    def winner(self, state_history):
        current_state = state_history[len(state_history) - 1]
        # Player has a move left
        if len(self.legal_plays(state_history)) > 0:
            return 0

        cards = current_state['cards']
        scores = self.scores(cards)
        highest = max(scores)

        # We have a tie
        if scores.count(highest) == 1:
            return scores.index(max(scores))
        else:
            return -1
