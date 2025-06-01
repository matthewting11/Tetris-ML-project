import tkinter as tk

root = tk.Tk()
root.title("Blank Window")
root.geometry("400x300")

canvas = tk.Canvas(root, width=400, height = 300, bg="white")
canvas.pack()

canvas.create_rectangle(50,50,150,150,fill="green")
canvas.create_oval(200,50,300,150,fill="blue")

canvas.create_line(50,200,300,250,fill="red",width=3)

root.mainloop()

