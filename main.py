import customtkinter as ctk
from ui import Initiate_Image_Import, SettingsMenuButton, ImageCanvas
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

        #run
        self.run_app()
        self.mainloop()


    def restart_app(self):
        #remove all widgets and varaible tracing
        for widget in self.winfo_children():
            widget.destroy()
        self.settings['color_scheme'].trace_remove('write', self.trace_id) 
        self.run_app()


    def load_settings(self):
        try:
            with open(SETTINGS_FILENAME, 'r') as f:
                reader = csv.reader(f)
                row = next(reader, SETTINGS_DEAFULTS)
        except FileNotFoundError:
            row = SETTINGS_DEAFULTS

        return {
            'save_dir': ctk.StringVar(self, value = row[0]),
            'color_scheme': ctk.StringVar(self, value = row[1]),
            'compression': ctk.StringVar(self, value = row[2])
        }
    
    def apply_theme(self, *args):
        ctk.set_appearance_mode(self.settings['color_scheme'].get())
        for widget in self.winfo_children(): #workaround: Canvas does not accept tuples
            if isinstance(widget, ImageCanvas):
                widget.configure(background = themed_color(ACCENT_COLOR), highlightbackground = themed_color(BUTTON_COLOR))


    def run_app(self):
        self.settings_window = None #settings window variable for when openend
        self.settings = self.load_settings()
        self.trace_id = self.settings['color_scheme'].trace_add('write', self.apply_theme) #trace changes to theme color 
        self.apply_theme()
        Initiate_Image_Import(self, self.settings['save_dir'],
                              self.settings['compression'])
        SettingsMenuButton(self, self.settings_window,
                           self.settings['save_dir'],
                           self.settings['color_scheme'],
                           self.settings['compression'])


if __name__ == "__main__":
    App()