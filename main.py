import customtkinter as ctk
from ui import Initiate_Image_Import, SettingsMenu
from colors import *
import csv

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

        self.settings = None #settings window variable for when openend

        #initiate ui and fucntionality
        self.run_app()

        #run
        self.mainloop()


    def restart_app(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.run_app()


    def get_settings_from_csv(self):
        settings_filename = SETTINGS_FILENAME

        with open(settings_filename, 'r') as settings_file:
            csvreader = csv.reader(settings_file)
            rows = list(csvreader)
            
            if len(rows) == 0:
                saved = SETTINGS_DEAFULTS
            else:
                saved = rows[0]

        self.save_dir = saved[0]
        self.color_scheme = saved[1]
        self.default_compression = saved[2]

        ctk.set_appearance_mode(self.color_scheme)


    def run_app(self):
        self.get_settings_from_csv()
        Initiate_Image_Import(self, self.save_dir, self.default_compression)
        SettingsMenu(self, self.settings, self.save_dir, self.color_scheme, self.default_compression)


if __name__ == "__main__":
    App()