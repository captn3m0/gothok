from __future__ import absolute_import
import pytest
from hok.board import Board
import re


@pytest.fixture
def basic_board():
    return Board()


@pytest.mark.usefixtures("basic_board")
class TestHandOfKing(object):

    def make_board_state(self, board_str):
        pattern = re.compile(r"\s")
        # Remove all spaces
        board_str = pattern.sub("", board_str)
        lookup = ['-', 'V', 'U', 'Y', 'B', 'T', 'L', 'G', 'S']
        # Slice in 6 rows
        # And convert strings to numbers
        state = Board().start()
        board = [
            [lookup.index(card) for card in board_str[i:i+Board.GRID_SIZE]]
            for i in range(0, len(board_str), Board.GRID_SIZE)]
        state['board'] = board
        return state

    # Internal method to quickly help test scenarios
    def test_make_board(self, basic_board):
        state = self.make_board_state("SSGTUL\
                        SGGSSG\
                        YSSSVG\
                        GUBLLY\
                        BBLTLG\
                        YTLTB-")
        board = state['board']
        assert(board[0][0] == Board.STARK)
        assert(board[0][1] == Board.STARK)
        assert(board[0][5] == Board.LANNISTER)
        assert(board[5][5] == Board.EMPTY)
        assert(board[2][4] == Board.VARYS)

    def test_init(self, basic_board):
        basic_board.start()
        assert(basic_board.__class__ == Board)

    def test_scoring(self, basic_board):
        cards = [
            # Stark banner
            [Board.VARYS] + [Board.STARK] * 3 + [Board.TULLY],
            # Lannister banner, tie on Tully
            [Board.LANNISTER] + [Board.TULLY],
            # Only greyjoy, second on Targ
            [Board.TARGARYEN] * 2 + [Board.GREYJOY],
            # First on both
            [Board.TARGARYEN] * 3 + [Board.TYRELL]
        ]

        expected_scores = [1, 1, 1, 2]
        assert(expected_scores == basic_board.scores(cards))

    def test_legaly_plays(self, basic_board):
        # We make 5 moves: left right, up down, left
        start = self.make_board_state("\
---B--\
T--L--\
SSLVTT\
---S--\
U-----\
---S--")

        plays = basic_board.legal_plays([start])
        assert((2, 0) in plays)  # Leftmost STARK
        assert((2, 2) in plays)  # Leftmost LANNISTER
        assert((2, 5) in plays)  # Rightmost TARG
        assert((0, 3) in plays)  # Topmost BARATHEON
        assert((1, 3) in plays)  # Topmost LANNISTER
        assert((5, 3) in plays)  # Bottom STARK

        assert((2, 1) not in plays)  # Left middle STARK
        assert((2, 4) not in plays)  # Right middle TARG
        assert((3, 3) not in plays)  # Bottom Middle STARK

        assert(len(plays) == 6)

    def test_winner(self, basic_board):
        state = Board().start()
        state['cards'] = [
            [Board.STARK, Board.STARK],
            [Board.TULLY],
            [],
            [Board.TARGARYEN]
        ]

        winner = basic_board.winner([state])

        assert(winner == 0)

    def test_move(self, basic_board):
        # We make 5 moves: left right, up down, left
        start = self.make_board_state("\
---B--\
TV-L--\
------\
---S--\
U--S--\
------")
        basic_board.next_state(start, (1, 0))
        assert(start['board'][1][0] == Board.VARYS)
        assert(start['board'][1][1] == Board.EMPTY)
        assert(start['cards'][0] == [Board.TARGARYEN])

        basic_board.next_state(start, (1, 3))
        assert(start['board'][1][3] == Board.VARYS)
        assert(start['board'][1][1] == Board.EMPTY)
        assert(start['cards'][1] == [Board.LANNISTER])

        basic_board.next_state(start, (0, 3))
        assert(start['board'][1][3] == Board.EMPTY)
        assert(start['board'][0][3] == Board.VARYS)
        assert(start['cards'][2] == [Board.BARATHEON])

        basic_board.next_state(start, (4, 3))
        assert(start['board'][0][3] == Board.EMPTY)
        assert(start['board'][4][3] == Board.VARYS)
        assert(start['cards'][3] == [Board.STARK, Board.STARK])

        basic_board.next_state(start, (4, 0))
        assert(start['board'][4][3] == Board.EMPTY)
        assert(start['board'][4][0] == Board.VARYS)
        assert(start['cards'][0] == [Board.TARGARYEN, Board.TULLY])
