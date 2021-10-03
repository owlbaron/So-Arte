from functools import partial
from tkinter import *
from tkinter.font import *
from editor import Editor
from utils import Utils
from window_positioning import centered
from image_system import ImageSystem
from functools import partial
from recents import Recents


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        

        self.protocol("WM_DELETE_WINDOW", partial(Utils.close_all, self))
        self.image_system = ImageSystem()

        self.title('Só Arte')

        width = 500
        height = 350

        self.geometry(
            centered(
                width,
                height,
                self.winfo_screenwidth(),
                self.winfo_screenheight()
            )
        )

        buttonFont = Font(size=14)
        window = Canvas(self, bg="#000000", highlightthickness=0)

        leftPanel = Canvas(window, bg="#000000", highlightthickness=0)
        rightPanel = Canvas(window, bg="#000000", highlightthickness=0)


        openFileButton = Button(
            leftPanel,
            text="Abrir um arquivo",
            command=self.open_file,
            borderwidth=0,
            font=buttonFont
        )
        openFileButton.grid(row=0, column=0)

        openSamples = Label(leftPanel, text="Abrir exemplos")
        openSamples.grid(row=1, column=0)

        samples = ["Camera", "Moedas", "Foguete", "Astronauta"]

        on_click_sample = lambda sample: lambda e: self.open_sample(sample.lower())
        on_click_file = lambda filepath: lambda e: self.open_file(filepath)
        for index, sample in enumerate(samples):
            label = Label(leftPanel, text=sample)
            label.bind("<Button-1>", on_click_sample(sample))
            label.grid(row=index+2, column=0)

        leftPanel.grid(row=0, column=0, sticky="nsew")

        openRecently = Label(rightPanel, text="Abertos recentemente")
        openRecently.grid(row=0, column=0)

        recents = Recents.read()

        for index, recent in enumerate(recents):
            label = Label(rightPanel, text=recent["name"])
            if recent["type"] == "file":
                label.bind("<Button-1>", on_click_file(recent["param"]))
            else:
                label.bind("<Button-1>", on_click_sample(recent["param"]))
            label.grid(row=index+1, column=0)

        rightPanel.grid(row=0, column=1, sticky="nsew")

        window.grid_columnconfigure(0, weight=1, uniform="panels")
        window.grid_columnconfigure(1, weight=1, uniform="panels")
        window.grid_rowconfigure(0, weight=1)
        window.pack(expand=1, fill=BOTH)

    def __open_editor_and_destroy(self, img):
        if img is not None:
            self.destroy()

            editor = Editor(img)
            editor.mainloop()

    def open_file(self, filepath=None):
        img = self.image_system.open_file(filepath)

        self.__open_editor_and_destroy(img)

    def open_sample(self, sample):
        img = self.image_system.open_sample(sample)

        self.__open_editor_and_destroy(img)


if __name__ == '__main__':
    app = App()
    
    app.mainloop()