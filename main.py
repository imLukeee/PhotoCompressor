from PIL import Image, ImageTk
import customtkinter as ctk
from tkinter import filedialog
from ui import *

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color = "#1E1E1F")

        APP_SIZE = (800, 800)
        MIN_SIZE = (600,600)

        #fonts
        import_image_button_font = ctk.CTkFont('Arial', 24, 'bold')

        #General window setup
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = screen_width // 2 - (APP_SIZE[0] // 2)
        y = screen_height // 2 - (APP_SIZE[1] // 2)

        self.title('Photo Compressor')
        self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}+{x}+{y}')
        self.minsize(MIN_SIZE[0], MIN_SIZE[1])

        #create grid layout
        self.grid_columnconfigure((0,1,2), uniform = 'a')
        self.grid_rowconfigure((0,1,2), uniform = 'a')

        #create ui elements
        self.import_button = ImportImageButton(self, font = import_image_button_font, func = self.import_image)


        self.mainloop()

    def import_image(self):
        filepath = filedialog.askopenfilename()
        self.original_image = Image.open(filepath)
        self.import_button.place_forget()

        self.image_tk = ImageTk.PhotoImage(self.original_image)

        self.image_preview = ImageCanvas(self, self.image_tk)


if __name__ == "__main__":
    App()