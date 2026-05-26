from game import *

userDifficulty = int(input("Enter the desired difficulty (1-3): "))

if userDifficulty < 1 or userDifficulty > 3:
    print("Invalid difficulty level. Defaulting to 1 (Easy).")
    _game = Game(0)
else:
    _game = Game(userDifficulty - 1)

message = _game.start()
print(message)