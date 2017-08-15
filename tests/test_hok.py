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

    def test_move(self, basic_board):
        start = self.make_board_state("\
-B----\
TV-L--\
------\
-S----\
-S----\
------")
        left = basic_board.next_state(start, (1, 0))
        assert(left['board'][1][0] == Board.VARYS)
        assert(left['board'][1][1] == Board.EMPTY)
        assert(left['cards'][0] == [Board.TARGARYEN])

        right = basic_board.next_state(start, (1, 3))
        assert(right['board'][1][3] == Board.VARYS)
        assert(right['board'][1][1] == Board.EMPTY)
        assert(right['cards'][0] == [Board.LANNISTER])
