from PIL import Image
import customtkinter as ctk
from tkinter import filedialog

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
        ImportImageSelector(self, font = import_image_button_font)


        self.mainloop()


class ImportImageSelector(ctk.CTkButton):
    def __init__(self, parent, font):
        super().__init__(master = parent, text = 'Select Image', font = font, command = self.select_image_file)
        self.place(relx = 0.5, rely = 0.5, relwidth = 0.5, relheight = 0.075, anchor = 'center')

    
    def select_image_file(self):
        filepath = filedialog.askopenfilename()
        img = Image.open(filepath)
        img.show()

if __name__ == "__main__":
    App()