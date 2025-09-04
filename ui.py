import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
from colors import *
from settings_window import *
import os, subprocess, platform
from widgets import SegmentedSelector


class Initiate_Image_Import(ctk.CTkButton):
    def __init__(self, parent, save_dir_var, default_compression_var):
        super().__init__(master = parent,
                         text = 'Select Image',
                         font = ctk.CTkFont('Arial', 24, 'bold'),
                         command = self.import_image,
                         fg_color = BUTTON_COLOR,
                         hover_color = BUTTON_HOVER,
                         corner_radius = 12)
        self.place(relx = 0.5, rely = 0.5, relwidth = 0.5, relheight = 0.075, anchor = 'center')
        self.main_window = parent

        self.save_dir = save_dir_var
        self.default_compression = default_compression_var


    def import_image(self):
        filepath = filedialog.askopenfilename()
        if not filepath:
            return
        
        #get original size in kilobytes
        self.original_size = os.stat(filepath).st_size / 1000
        
        #once image is imported, delete the import button
        self.original_image = Image.open(filepath)
        self.place_forget()

        #display image preview and user controls
        self.image_preview = ImageCanvas(self.main_window, self.original_image)
        self.controls = UserControls(self.main_window, self.original_image, self.original_size, self.save_dir, self.default_compression)

    

class ImageCanvas(ctk.CTkCanvas):
    def __init__(self, parent, pil_image):
        super().__init__(master = parent,
                         background = themed_color(ACCENT_COLOR),
                         highlightbackground = themed_color(BUTTON_COLOR))
        self.place(relx = 0.5, rely = 0.05, relwidth = 0.75, relheight = 0.5, anchor = 'n')

        self.original_pil = pil_image
        self.image_tk = ImageTk.PhotoImage(self.original_pil)

        self.bind('<Configure>', self.resize_image)

        self.create_image(0, 0, anchor = 'nw', image = self.image_tk)
    
    def resize_image(self, event):
        image_ratio = self.original_pil.width / self.original_pil.height
        canvas_ratio = event.width / event.height

        #get ratio to scale image
        if image_ratio < canvas_ratio:
            self.image_height = event.height
            self.image_width = int(self.image_height * image_ratio)
        elif image_ratio > canvas_ratio:
            self.image_width = event.width
            self.image_height = int(self.image_width / image_ratio)
        
        self.place_image(event)

    def place_image(self, event):
        resized_pil = self.original_pil.resize((self.image_width, self.image_height))
        self.image_tk = ImageTk.PhotoImage(resized_pil)

        self.center_width = (event.width - self.image_width) / 2
        self.center_height = (event.height - self.image_height) / 2

        self.delete('all')
        self.create_image(self.center_width, self.center_height, anchor = 'nw', image = self.image_tk)


class UserControls(ctk.CTkFrame):
    def __init__(self, parent, original, original_size, save_path_var, compression_var):
        super().__init__(parent, fg_color = ACCENT_COLOR)
        self.main_window = parent

        self.ArialBold = ctk.CTkFont('Arial', 28, 'bold')
        self.ArialBoldQL = ctk.CTkFont('Arial', 24, 'bold')
        self.ArialRegular = ctk.CTkFont('Arial', 28, 'normal')
        self.ButtonFont = ctk.CTkFont('Arial', 18, 'bold')

        self.original_image = original
        self.orignal_size = original_size
        self.place(relx = 0.05, rely = 0.6, relwidth = 0.9, relheight = 0.35, anchor = 'nw')

        self.filename = ctk.StringVar(self, value = '')
        self.save_path = save_path_var
        self.quality = compression_var

        self.filename_label = ctk.CTkLabel(self, text = 'Enter a filename:', font = self.ArialBold)
        self.filename_entry = ctk.CTkEntry(self,
                                           textvariable = self.filename,
                                           font = self.ArialRegular,
                                           corner_radius = 12)

        self.quality_label = ctk.CTkLabel(self, text = 'Quality:', font = self.ArialBoldQL)
        self.quality_select = SegmentedSelector(self, self.quality, values = QUALITY_LIST)

        self.compress_button = ctk.CTkButton(self,
                                             text = 'Compress',
                                             font = self.ButtonFont,
                                             command = self.compress_image,
                                             fg_color = BUTTON_COLOR,
                                             hover_color = BUTTON_HOVER,
                                             corner_radius = 12)

        self.filename_label.place(relx = 0.5, rely = 0.1, anchor = 'center')
        self.filename_entry.place(relx = 0.5, rely =0.2, relwidth = 0.8, relheight = 0.2, anchor = 'n')
        self.quality_label.place(relx = 0.3, rely = 0.6, anchor = 'center')
        self.quality_select.place(relx = 0.6, rely = 0.6, relwidth = 0.4, relheight = 0.2, anchor = 'center')
        self.compress_button.place(relx = 0.5, rely = 0.85, relwidth = 0.25, relheight = 0.1, anchor = 'center')


    def reset_app(self):
        self.main_window.restart_app()

    
    def open_save_folder(self):
        system = platform.system()
    
        if system == "Windows":
            subprocess.run(f'explorer /select,"{self.full_path}"')
        elif system == "Darwin": #macOS
            subprocess.run(["open", "-R", self.full_path])
        elif system == "Linux":
            subprocess.run(["xdg-open", os.path.dirname(self.full_path)])
        else:
            raise NotImplementedError(f"OS {system} not supported")


    def compress_image(self):
        quality = QUALITY_DICT[self.quality.get()]
        self.filename = f'Compressed_{self.filename.get()}.jpeg'

        save_path = self.save_path.get()

        #ensure save dir exists
        os.makedirs(save_path, exist_ok = True)

        self.original_image = self.original_image.convert('RGB')
        self.full_path = os.path.join(save_path, self.filename)
        self.original_image.save(self.full_path,
                                 format = 'jpeg',
                                 optimize = True,
                                 quality = quality)

        #get compressed image size in kilobytes
        self.compressed_size = os.stat(self.full_path).st_size / 1000

        reduced_size = round(self.orignal_size - self.compressed_size, 2)
        percentage = round((self.orignal_size - self.compressed_size)/self.orignal_size * 100, 2)

        #summary + ask for another one 
        ans = messagebox.askquestion('Compression Finished', f'Image compressed\nSize reduced by {percentage}% ({reduced_size} kB) 🤩\n\nCompress another image?')
        
        if ans == 'yes':
            self.reset_app()
        else:
            self.open_save_folder()
            self.main_window.destroy()

    
class SettingsMenuButton(ctk.CTkButton):
    def __init__(self, parent, settings_var, save_dir_var, color_scheme_var, default_compression_var):
        super().__init__(master = parent,
                         text = '⚙︎',
                         font = ctk.CTkFont('Arial', 24),
                         fg_color = 'transparent',
                         hover_color = MENU_BUTTON_HOVER,
                         text_color = TEXT_COLOR,
                         corner_radius = 12,
                         command = self.open_settings)
        self.place(relx = 0.99, rely = 0.01, relwidth = 0.05, relheight = 0.05, anchor = 'ne')
        
        self.settings_window = settings_var
        self.main_window = parent
        
        self.save_dir_csv = save_dir_var
        self.color_scheme_csv = color_scheme_var
        self.default_compression_csv = default_compression_var


    def open_settings(self):
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = SettingsWindow(self, self.save_dir_csv, self.color_scheme_csv, self.default_compression_csv, self.main_window)  # create window if its None or destroyed
        else:
            self.settings_window.focus()  # if window exists focus it