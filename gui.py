import tkinter

window = tkinter.Tk()

board = []
for y in range(8):
    for x in range(8):
        cur = tkinter.Button(window)
        
        if abs(x % 2 - y % 2):
            cur.config(background="black")
        
        cur.grid(row=y, column=x)
        
        board.append(cur)

button = tkinter.Button(window, text = "K", background="black")
button.pack()
button = tkinter.Button(window, text = "K", background="white")
button.pack()

window.mainloop()