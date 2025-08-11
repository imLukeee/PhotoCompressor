import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
from settings import *
import os, subprocess, platform


class Initiate_App(ctk.CTkButton):
    def __init__(self, parent):
        super().__init__(master = parent, text = 'Select Image', font = ctk.CTkFont('Arial', 24, 'bold'), command = self.import_image, fg_color = BUTTON_COLOR, hover_color = BUTTON_HOVER, corner_radius = 12)
        self.place(relx = 0.5, rely = 0.5, relwidth = 0.5, relheight = 0.075, anchor = 'center')
        self.main_window = parent

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
        self.controls = UserControls(self.main_window, self.original_image, self.original_size)


class ImageCanvas(ctk.CTkCanvas):
    def __init__(self, parent, pil_image):
        super().__init__(master = parent, background = ACCENT_COLOR)
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
    def __init__(self, parent, original, original_size):
        super().__init__(parent, fg_color= ACCENT_COLOR)
        self.main_window = parent

        self.ArialBold = ctk.CTkFont('Arial', 28, 'bold')
        self.ArialRegular = ctk.CTkFont('Arial', 28, 'normal')
        self.ButtonFont = ctk.CTkFont('Arial', 18, 'bold')

        self.original_image = original
        self.orignal_size = original_size
        self.place(relx = 0.05, rely = 0.6, relwidth = 0.9, relheight = 0.35, anchor = 'nw')

        self.filename = ctk.StringVar(self, value = '')
        self.quality = ctk.StringVar(self, value = QUALITY_LIST[0])

        self.filename_label = ctk.CTkLabel(self, text = 'Enter a filename:', font = self.ArialBold)
        self.filename_entry = ctk.CTkEntry(self, textvariable = self.filename, font = self.ArialRegular, corner_radius = 12)

        self.quality_label = ctk.CTkLabel(self, text = 'Quality:', font = self.ArialBold)
        self.quality_select = ctk.CTkOptionMenu(self, values = QUALITY_LIST, variable = self.quality, fg_color= BUTTON_COLOR, button_color = BUTTON_COLOR, button_hover_color = BUTTON_HOVER, dropdown_hover_color = BUTTON_HOVER, font = self.ArialRegular, corner_radius = 12)

        self.compress_button = ctk.CTkButton(self, text = 'Compress', font = self.ButtonFont, command = self.compress_image, fg_color = BUTTON_COLOR, hover_color = BUTTON_HOVER, corner_radius = 12)

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
            subprocess.run(f'explorer /select,"{self.filename}"')
        elif system == "Darwin": #macOS
            subprocess.run(["open", "-R", self.filename])
        elif system == "Linux":
            subprocess.run(["xdg-open", os.path.dirname(self.filename)])
        else:
            raise NotImplementedError(f"OS {system} not supported")


    def compress_image(self):
        quality = QUALITY_DICT[self.quality.get()]
        self.filename = f'Compressed_{self.filename.get()}.jpeg'

        self.original_image = self.original_image.convert('RGB')
        self.original_image.save(self.filename, format = 'jpeg', optimize = True, quality = quality)

        #get compressed image size in kilobytes
        self.compressed_size = os.stat(self.filename).st_size / 1000

        reduced_size = round(self.orignal_size - self.compressed_size, 2)
        percentage = round((self.orignal_size - self.compressed_size)/self.orignal_size * 100, 2)

        ans = messagebox.askquestion('Compression Finished', f'Image compressed\nSize reduced by {percentage}% ({reduced_size} kB) 🤩\n\nCompress another image?')
        
        if ans == 'yes':
            self.reset_app()
        else:
            self.open_save_folder()
            self.main_window.destroy()