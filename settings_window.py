import customtkinter as ctk
from tkinter import filedialog
from colors import *
import csv

#csv structure:
#save_directory ; light/dark mode ; default compression quality


class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent, fg_color = ACCENT_COLOR)
        self.geometry('600x800')
        self.title('Settings')
        self.resizable(False, False)

        self.setting_title_font = ctk.CTkFont('Arail', 24, 'bold')

        self.save_dir_path = ctk.StringVar(self, value = './CompressedImages/')
        self.color_scheme = ctk.StringVar(self, 'Dark')
        self.default_compression = ctk.StringVar(self, QUALITY_LIST[0])
 
        self.create_settings_ui()


    def create_settings_ui(self):
        SaveFileSelector(self, self.setting_title_font, self.save_dir_path)
        ColorSchemeSelector(self, self.setting_title_font, self.color_scheme)
        DefaultCompressionSelector(self, self.setting_title_font, self.default_compression)
        ConfirmSettings(self)


    def select_save_folder(self):
        path = filedialog.askdirectory()

        if not path:
            path = './CompressedImages/'

    
    def save_settings_to_file(self):
        filename = SETTINGS_FILENAME

        with open (filename, 'w') as settings:
            csvwrtiter = csv.writer(settings)
            csvwrtiter.writerow([self.save_dir.get(), self.color_scheme.get(), self.default_compression.get()])


class SaveFileSelector(ctk.CTkFrame):
    def __init__(self, parent, title_font, save_location_var):
        super().__init__(master = parent)
        self.pack(side = 'top', expand = True, fill = 'both')

        self.setting_title = ctk.CTkLabel(self, text = 'Save directory', font = title_font)
        self.current_location_label = ctk.CTkLabel(self, textvariable = save_location_var, bg_color = ACCENT_COLOR, corner_radius = 12, anchor = 'w', justify = 'left')
        self.change_save_dir_button = ctk.CTkButton(self.current_location_label, text = '...', fg_color = BUTTON_COLOR)


        self.setting_title.place(relx = 0.05, rely = 0.1, anchor = 'nw')
        self.current_location_label.place(relx = 0.05, rely = 0.4, relwidth = 0.9, relheight = 0.25, anchor = 'nw')
        
        #inside current_loaction_label
        self.change_save_dir_button.place(relx = 1, rely = 0, relwidth = 0.15, relheight = 1, anchor = 'ne')


class ColorSchemeSelector(ctk.CTkFrame):
    def __init__(self, parent, title_font, color_scheme_var):
        super().__init__(master = parent)
        self.pack(side = 'top', expand = True, fill = 'both')
    
        self.default_color_mode_var = ctk.StringVar(value = 'Dark')

        self.setting_title = ctk.CTkLabel(self, text = 'Apperance', font = title_font)
        self.color_mode_toggle = ctk.CTkSegmentedButton(self, variable = color_scheme_var, values = ['Light', 'Dark'],corner_radius = 12)


        self.setting_title.place(relx = 0.05, rely = 0.05, anchor = 'nw')
        self.color_mode_toggle.place(relx = 0.5, rely= 0.55, relwidth = 0.75, relheight = 0.45, anchor = 'center')


class DefaultCompressionSelector(ctk.CTkFrame):
    def __init__(self, parent, title_font, default_compression_var):
        super().__init__(master = parent)
        self.pack(side = 'top', expand = True, fill = 'both')

        self.default_compression_mode = ctk.StringVar(value = QUALITY_LIST[0])

        self.setting_title = ctk.CTkLabel(self, text = 'Default Compression', font = title_font)
        self.default_compression_toggle = ctk.CTkSegmentedButton(self, variable = default_compression_var, values = QUALITY_LIST ,corner_radius = 12)


        self.setting_title.place(relx = 0.05, rely = 0.05, anchor = 'nw')
        self.default_compression_toggle.place(relx = 0.5, rely= 0.55, relwidth = 0.75, relheight = 0.45, anchor = 'center')


class ConfirmSettings(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent, fg_color = ACCENT_COLOR)
        self.pack(side = 'bottom', pady = 20)
        self.rowconfigure(0)
        self.columnconfigure((0,1,2), uniform = 'a', weight = 1)

        self.cancel_button = ConfirmSettingsButton(self, 'Cancel', 'toadd', 0)
        self.apply_button = ConfirmSettingsButton(self, 'Apply', 'toadd' , 1)
        self.reset_button = ConfirmSettingsButton(self, 'Reset', 'toadd', 2)
        

class ConfirmSettingsButton(ctk.CTkButton):
    def __init__(self, parent, text, command, column):
        super().__init__(master = parent, text = text, fg_color = BUTTON_COLOR, hover_color = BUTTON_HOVER, corner_radius = 12, height = 50)
        self.grid(row = 0, column = column, sticky = 'nsew', padx = 10, pady = 10)
