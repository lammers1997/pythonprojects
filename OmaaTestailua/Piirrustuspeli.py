from tkinter import *
from tkinter import ttk, colorchooser, filedialog

class piirtopeli:

    def __init__(self):
        self.__window = Tk()
        self.__window.title("Piirtopeli")

        self.green_button = Button(self.__window, command=self.set_color_green, bg="green",width=10, height=10)
        self.green_button.grid(column=0,row=0)
        self.black_button = Button(self.__window, command=self.set_color_black, bg="black")
        self.black_button.grid(column=0, row=1)

        self.c = Canvas(self.__window, width=800,height=500, bg="white")
        self.c.grid(column=1,row=1)
        self.c.old_coords = None



        self.__window.bind('<B1-Motion>', self.draw)
        self.__window.bind('<ButtonRelease-1>', self.reset_coords)

    def set_color_black(self):
        self.color = "black"

    def set_color_green(self):
        self.color = "green"

    def reset_coords(self, event):
        self.c.old_coords = None

    def draw(self, event):
        x, y = event.x, event.y
        if self.c.old_coords:
            x1, y1 = self.c.old_coords
            self.c.create_line(x, y, x1, y1, fill=self.color)
        self.c.old_coords = x, y

    def start(self):
        self.__window.mainloop()

    def quit(self):
        self.__window.quit()


def main():
    ui=piirtopeli()
    ui.start()

main()