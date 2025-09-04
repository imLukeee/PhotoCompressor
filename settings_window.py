import customtkinter as ctk
from tkinter import filedialog
from colors import *
from widgets import *
import csv, os

#csv structure:
#save_directory ; light/dark mode ; default compression quality


class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent, save_dir_var, color_scheme_var, default_compression_var, main_window):
        super().__init__(parent, fg_color = BG_COLOR)
        self.geometry('600x800')
        self.title('Settings')
        self.resizable(False, False)
        self.main_window = main_window

        self.setting_title_font = ctk.CTkFont('Arail', 24, 'bold')

        self.save_dir_path = save_dir_var
        self.color_scheme = color_scheme_var
        self.default_compression = default_compression_var
 
        self.create_settings_ui()


    def create_settings_ui(self):
        SaveFileSelector(self, self.setting_title_font, self.save_dir_path)
        ColorSchemeSelector(self, self.setting_title_font, self.color_scheme)
        DefaultCompressionSelector(self, self.setting_title_font, self.default_compression)
        ConfirmSettings(self, self.save_dir_path, self.color_scheme, self.default_compression)


class SaveFileSelector(ctk.CTkFrame):
    def __init__(self, parent, title_font, save_location_var):
        super().__init__(master = parent, fg_color= 'transparent')
        self.pack(side = 'top', expand = True, fill = 'both')
        self.save_location = save_location_var

        self.setting_title = ctk.CTkLabel(self, text = 'Save directory', font = title_font)
        self.current_location_label = ctk.CTkLabel(self, textvariable = save_location_var, bg_color = MENU_BUTTON_HOVER, corner_radius = 12, anchor = 'w', justify = 'left')
        self.change_save_dir_button = ctk.CTkButton(self.current_location_label, text = '...', fg_color = BUTTON_COLOR, hover_color = BUTTON_HOVER, command = self.select_save_folder)


        self.setting_title.place(relx = 0.05, rely = 0.1, anchor = 'nw')
        self.current_location_label.place(relx = 0.05, rely = 0.4, relwidth = 0.9, relheight = 0.25, anchor = 'nw')
        
        #inside current_loaction_label
        self.change_save_dir_button.place(relx = 1, rely = 0, relwidth = 0.15, relheight = 1, anchor = 'ne')


    def select_save_folder(self):
        path = filedialog.askdirectory()

        if not path:
            path = './CompressedImages/'

        self.save_location.set(path)


class ColorSchemeSelector(ctk.CTkFrame):
    def __init__(self, parent, title_font, color_scheme_var):
        super().__init__(master = parent, fg_color= 'transparent')
        self.pack(side = 'top', expand = True, fill = 'both')
    
        self.default_color_mode_var = ctk.StringVar(value = 'Dark')

        self.setting_title = ctk.CTkLabel(self, text = 'Apperance', font = title_font)
        self.color_mode_toggle = SegmentedSelector(self, color_scheme_var, values = ['Light', 'Dark'])


        self.setting_title.place(relx = 0.05, rely = 0.05, anchor = 'nw')
        self.color_mode_toggle.place(relx = 0.5, rely= 0.55, relwidth = 0.75, relheight = 0.45, anchor = 'center')


class DefaultCompressionSelector(ctk.CTkFrame):
    def __init__(self, parent, title_font, default_compression_var):
        super().__init__(master = parent, fg_color= 'transparent')
        self.pack(side = 'top', expand = True, fill = 'both')

        self.setting_title = ctk.CTkLabel(self, text = 'Default Compression', font = title_font)
        self.default_compression_toggle = SegmentedSelector(self, default_compression_var, values = QUALITY_LIST)
        

        self.setting_title.place(relx = 0.05, rely = 0.05, anchor = 'nw')
        self.default_compression_toggle.place(relx = 0.5, rely= 0.55, relwidth = 0.75, relheight = 0.45, anchor = 'center')


class ConfirmSettings(ctk.CTkFrame):
    def __init__(self, parent, save_dir_var, color_scheme_var, default_compression_var):
        super().__init__(master = parent, fg_color = ACCENT_COLOR)
        self.pack(side = 'bottom', fill = 'x')

        self.save_dir_path = save_dir_var
        self.color_scheme = color_scheme_var
        self.default_compression = default_compression_var

        self.rowconfigure(0)
        self.columnconfigure((0,1,2), uniform = 'a', weight = 1)

        self.cancel_button = ConfirmSettingsButton(self, 'Cancel', parent.destroy, 0)
        self.apply_button = ConfirmSettingsButton(self, 'Apply', self.save_settings_to_file, 1)
        self.reset_button = ConfirmSettingsButton(self, 'Reset', self.reset_settings, 2)


    def save_settings_to_file(self):
        with open (SETTINGS_FILENAME, 'w', newline='') as f:
            csvwrtiter = csv.writer(f)
            csvwrtiter.writerow([self.save_dir_path.get(), self.color_scheme.get(), self.default_compression.get()])


    def reset_settings(self):
        self.save_dir_path.set(SETTINGS_DEAFULTS[0])
        self.color_scheme.set(SETTINGS_DEAFULTS[1])
        self.default_compression.set(SETTINGS_DEAFULTS[2])
