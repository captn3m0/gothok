# A Game of Thrones: Hand of the King

See [rules][rules]. This is a very toned down version of the game, without the companion cards as that reduces the state space by a lot (since all house cards can be treated as identical)

Card lists can be found at the following 2 images:

- [Characters](https://boardgamegeek.com/image/3687891/game-thrones-hand-king)
- [Companions](https://boardgamegeek.com/image/3253090/game-thrones-hand-king)

## Setup:

1. Shuffle the following string: SSSSSSSSGGGGGGGLLLLLLTTTTTBBBBYYYUUV
2. Fit it into a 6x6 grid

## Play:

1. Check for valid moves (Max = 10) from (5 in east/west and 5 in north/south directions).
2. Declare for a house and move Varys to the corresponding character. This must be the farthest card for that house in that direction.
3. Collect the card, and gain the banner token for that house if you have the highest number of cards for that House (This can be made simpler by giving you the token if you have a proven majority)

## Score

If there are no legal moves left in the game, check number of tokens held by each player. Highest banner token player wins.

## Why

This is a learning experiment for Monte Carlo Tree Search. I picked this game because:

1. It is a perfect information game
2. Lookahead is a crucial part of the gameplay
3. A reduced set of the game (no companion cards) is easily understandable

I am using <https://jeffbradberry.com/posts/2015/09/intro-to-monte-carlo-tree-search/> as a base reference for the MCTS and the data structure implementatio

## License

All code is licensed under [MIT License](https://nemo.mit-license.org/)

[rules]: https://images-cdn.fantasyflightgames.com/filer_public/07/d3/07d30fde-83cf-4de7-abde-3c3a08eacd02/handoftheking_rules_eng.pdf
