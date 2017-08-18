from distutils.core import setup

setup(
    name='GameOfThronesHandofKing',
    version='0.0.1-dev',
    author='Nemo',
    author_email='me@captnemo.in',
    packages=['hok'],
    entry_points={
        'jrb_board.games': 'hok = hok.board:Board',
    },
    license='LICENSE',
    description="An implementation of GoT: Hand of King board game",
)
