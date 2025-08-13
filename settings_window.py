import customtkinter as ctk
from tkinter import filedialog
from colors import *
import csv

#csv structure:
#save_directory ; light/dark mode ; default compression quality


class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry('600x800')
        self.title('Settings')
        self.resizable(False, False)

        self.setting_title_font = ctk.CTkFont('Arail', 24, 'bold')

        self.save_dir = '.'
        self.color_scheme = 'dark'
        self.default_compression = 'Lowest size'

        self.create_settings_ui()


    def create_settings_ui(self):
        SaveFileSelector(self, self.setting_title_font)
        ColorSchemeSelector(self, self.setting_title_font)
        DefaultCompressionSelector(self, self.setting_title_font)


    def select_save_folder(self):
        path = filedialog.askdirectory()

        if not path:
            path = './CompressedImages/'

    
    def save_settings_to_file(self):
        filename = 'settings.csv'

        with open (filename, 'w') as settings:
            csvwrtiter = csv.writer(settings)
            csvwrtiter.writerow([self.save_dir, self.color_scheme, self.default_compression])


class SaveFileSelector(ctk.CTkFrame):
    def __init__(self, parent, title_font):
        super().__init__(master = parent)
        #self.place(relx = 0, rely = 0, relwidth = 1, relheight = 0.33)
        self.pack(side = 'top', expand = True, fill = 'both')

        self.setting_title = ctk.CTkLabel(self, text = 'Save directory', font = title_font)
        self.current_location_label = ctk.CTkLabel(self, text = 'variable to be added', bg_color = ACCENT_COLOR, corner_radius = 12, anchor = 'w', justify = 'left')
        self.change_save_dir_button = ctk.CTkButton(self.current_location_label, text = '...', fg_color = BUTTON_COLOR)


        self.setting_title.place(relx = 0.05, rely = 0.1, anchor = 'nw')
        self.current_location_label.place(relx = 0.05, rely = 0.4, relwidth = 0.9, relheight = 0.25, anchor = 'nw')
        
        #inside current_loaction_label
        self.change_save_dir_button.place(relx = 1, rely = 0, relwidth = 0.15, relheight = 1, anchor = 'ne')


class ColorSchemeSelector(ctk.CTkFrame):
    def __init__(self, parent, title_font):
        super().__init__(master = parent)
        #self.place(relx = 0, rely = 0.33, relwidth = 1, relheight = 0.33)
        self.pack(side = 'top', expand = True, fill = 'both')
    
        self.color_mode_var = ctk.StringVar(value = 'Dark')

        self.setting_title = ctk.CTkLabel(self, text = 'Apperance', font = title_font)
        self.color_mode_toggle = ctk.CTkSegmentedButton(self, variable = self.color_mode_var, values = ['Light', 'Dark'],corner_radius = 12)


        self.setting_title.place(relx = 0.05, rely = 0.05, anchor = 'nw')
        self.color_mode_toggle.place(relx = 0.5, rely= 0.55, relwidth = 0.75, relheight = 0.45, anchor = 'center')


class DefaultCompressionSelector(ctk.CTkFrame):
    def __init__(self, parent, title_font):
        super().__init__(master = parent)
        self.pack(side = 'top', expand = True, fill = 'both')

        self.default_compression_mode = ctk.StringVar(value = QUALITY_LIST[0])

        self.setting_title = ctk.CTkLabel(self, text = 'Default Compression', font = title_font)
        self.default_compression_toggle = ctk.CTkSegmentedButton(self, variable = self.default_compression_mode, values = QUALITY_LIST ,corner_radius = 12)


        self.setting_title.place(relx = 0.05, rely = 0.05, anchor = 'nw')
        self.default_compression_toggle.place(relx = 0.5, rely= 0.55, relwidth = 0.75, relheight = 0.45, anchor = 'center')

