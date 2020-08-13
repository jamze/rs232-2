import tkinter as tk
from threading import Thread

break_loop = 0

def measure():
    while running == 1:

        print("hello\n")

        if break_loop == 1:
            break


def stop_measure():
    global running
    global ab
    global break_loop

    running = 0
    ab = 444
    # input1="exit"
    break_loop = 1

def start_measure():
    global running
    global ab
    global break_loop

    running = 1
    ab = 22

    t = Thread (target=measure)
    t.start()
    break_loop = 0

window = tk.Tk()

window.title("Data acquisition")

# tk.Button(window, text="1. CONFIRM", command=show_values).grid(row=8, column=0)
tk.Button(window, text="2. START TEST", command=start_measure).grid(row=8, column=1)
tk.Button(window, text="3. STOP TEST", command=stop_measure).grid(row=8, column=2)
tk.Button(window, text="QUIT", command=quit).grid(row=8, column=3)

window.mainloop()