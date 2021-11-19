import interface

inter = interface.Interface()

while True:
    try:
        inter.setup()
        break
    except Exception as ex:
        print("Setup failed!", ex)

try:
    if inter.startGame():
        print("You win!")
    else:
        print("You loose!")
except EOFError:
    print("Error: Connection lost!")

inter.cleanup()