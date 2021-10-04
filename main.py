from functools import partial
from tkinter import *
from editor import Editor
from utils import Utils
from window_positioning import centered
from image_system import ImageSystem


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

        openFileButton = Button(self, text="Abrir um arquivo", command=self.open_file)

        openFileButton.pack()

    def __open_editor_and_destroy(self, img):
        if img is not None:
            self.destroy()

            editor = Editor(img)
            editor.mainloop()

    def open_file(self):
        img = self.image_system.open_file()
        self.__open_editor_and_destroy(img)

    def open_camera(self):
        img = self.image_system.open_sample("camera")

        self.__open_editor_and_destroy(img)


if __name__ == '__main__':
    app = App()
    
    app.mainloop()