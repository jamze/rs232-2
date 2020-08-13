import tkinter as tk

window = tk.Tk()
window.title('My Window')
window.geometry('500x300')

e1 = tk.Entry(window, show=None, font=('Arial', 14))
e2 = tk.Entry(window, show='*', font=('Arial', 14))
e1.grid(row=0)


def show():
    global text
    text = e1.get()
    print(text)


tk.Button(window, command=show).grid(row=1)

window.mainloop()
