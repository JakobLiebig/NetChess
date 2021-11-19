import interface

inter = interface.Interface()

inter.setup()

if inter.startGame():
    print("You win!")
else:
    print("You loose!")