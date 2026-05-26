from game import *


print("""To play, left click to reveal and right click to flag.
Your goal is to reveal all the cells without clicking on any mines.
Each number tells you how many mines are adjacent to you. 
Have fun, and good luck!\n""")
userDifficulty = int(input("Enter the desired difficulty (1-3): "))
print()
if userDifficulty < 1 or userDifficulty > 3:
    print("Invalid difficulty level. Defaulting to 1 (Easy).")
    _game = Game(0)
else:
    _game = Game(userDifficulty - 1)

message = _game.start()
print(message)