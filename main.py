import PIL as pillow
import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color = "#1E1E1F")

        APP_SIZE = (800, 800)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = screen_width // 2 - (APP_SIZE[0] // 2)
        y = screen_height // 2 - (APP_SIZE[1] // 2)

        self.title('Photo Compressor')
        self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}+{x}+{y}')

        self.mainloop()

if __name__ == "__main__":
    App()