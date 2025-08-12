import customtkinter as ctk
from tkinter import filedialog
import csv

#csv structure:
#save_directory ; light/dark mode ; default compression quality


class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry('500x400')
        self.title('Settings')

        self.save_dir = '.'
        self.color_scheme = 'dark'
        self.default_compression = 'Lowest size'

        filename = 'settings.csv'

        with open (filename, 'w') as settings:
            csvwrtiter = csv.writer(settings)
            csvwrtiter.writerow([self.save_dir, self.color_scheme, self.default_compression])
                


    def select_save_folder(self):
        path = filedialog.askdirectory()

        if not path:
            path = './CompressedImages/'