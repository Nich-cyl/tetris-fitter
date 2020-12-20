# tetris-fitter
Fills in a square board with tetris tiles and tries to figures out original configuration when given only the outline.

Neeeeech is just my old account I lost the password to. Also it's my first repository so cut me some slack if I haven't uploaded everything right :)
Note this project uses Pyglet for drawing and displaying the tiles.

branch "master" is the setting up of the generating and displaying of the grids and problems
branch "solve_approach1" is my first attempt, messy since I had no plan going into this
branch "main-solve_approach2" is my second attempt, being more structured after I actually planned this time and learnt from the first attempt
  - this one is my best working version and so is the default
branch "solve_approach3" is my third attempt, where I tried to log what merges it made and backtrack whenever it hits a dead end
  - this one hurt my head a lot so I had to give up :(


Below is a brief outline on what each file does (in main-solve_approach2)

main.py 
  - sets up the different variables (2D arrays) where the boards are held (the original, the outline, and the computed solution) as well as drawing up the window and the grids.
When the grid is drawn, pressing a few number keys will display the different boards:
  - 1 draws the outline on the left
  - 2 draws the original on the left
  - 3 computes and then draws the computed solution on the right, as well as logging accuracies in terminal
  - 0 clears both sides and generates a new problem board

generate.py
  - goes through the whole grid and tries a max of 3 times to fit a random tetris piece into it
  - if the tetris piece collides with something all 3 times it gives up and moves on
  - this leaves gaps in the board but not too many
  - returns both the original grid (with each tetris piece assigned a number) and the outline (with only 1s for filled tiles and 0s for empty ones)

display.py
  - holds functions for drawing the gridlines and the boards

solve.py
  - all works for sol()
  - first connects all tiles that are only connected to 1 other tile (must be connected since there are no standalone tiles)
  - connects least-connected tiles to each other 
    - by looking at number of neighbours, no. of neighbours' neighbours, no. of neighbours' neighbours' neighbours)
    - whether this tile can connect to said neighbour ie creates group <= 4? 
  - merges groups together by assigning the same "colour" id


Anyways, this is just a fun little project I did :D
