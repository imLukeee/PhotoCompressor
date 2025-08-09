import customtkinter as ctk
from ui import Initiate_App
from settings import BG_COLOR

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color = BG_COLOR)

        APP_SIZE = (800, 800)
        MIN_SIZE = (600,600)

        #General window setup
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = screen_width // 2 - (APP_SIZE[0] // 2)
        y = screen_height // 2 - (APP_SIZE[1] // 2)

        #window parameters
        self.title('Photo Compressor')
        self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}+{x}+{y}')
        self.minsize(MIN_SIZE[0], MIN_SIZE[1])

        #create grid layout
        self.grid_columnconfigure((0,1,2), uniform = 'a')
        self.grid_rowconfigure((0,1,2), uniform = 'a')

        #initiate ui and fucntionality
        Initiate_App(self)

        #run
        self.mainloop()


if __name__ == "__main__":
    App()