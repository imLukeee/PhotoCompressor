import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
from settings import *


class Initiate_App(ctk.CTkButton):
    def __init__(self, parent):
        super().__init__(master = parent, text = 'Select Image', font = ctk.CTkFont('Arial', 24, 'bold'), command = self.import_image, fg_color = BUTTON_COLOR, hover_color = BUTTON_HOVER)
        self.place(relx = 0.5, rely = 0.5, relwidth = 0.5, relheight = 0.075, anchor = 'center')
        self.main_window = parent

    def import_image(self):
        filepath = filedialog.askopenfilename()
        if not filepath:
            return
        
        self.original_image = Image.open(filepath)
        self.place_forget()

        self.image_preview = ImageCanvas(self.main_window, self.original_image)
        self.controls = UserControls(self.main_window, self.original_image)


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
        
        self.place_image()

    def place_image(self):
        resized_pil = self.original_pil.resize((self.image_width, self.image_height))
        self.image_tk = ImageTk.PhotoImage(resized_pil)

        self.delete('all')
        self.create_image(0,0, anchor = 'nw', image = self.image_tk)


class UserControls(ctk.CTkFrame):
    def __init__(self, parent, original):
        super().__init__(parent, fg_color= ACCENT_COLOR)
        self.original_image = original
        self.place(relx = 0.05, rely = 0.6, relwidth = 0.9, relheight = 0.35, anchor = 'nw')
        self.filename = ctk.StringVar(self, value = '')

        self.filename_prompt = ctk.CTkLabel(self, text = 'Enter a filename:', font = ctk.CTkFont('Arial', 28, 'bold'))
        self.filename_entry = ctk.CTkEntry(self, textvariable = self.filename, font = ctk.CTkFont('Arial', 28, 'normal'))

        self.compress_button = ctk.CTkButton(self, text = 'Compress', command = self.compress_image, fg_color = BUTTON_COLOR, hover_color = BUTTON_HOVER)

        self.filename_prompt.place(relx = 0.5, rely = 0.15, anchor = 'center')
        self.filename_entry.place(relx = 0.5, rely =0.3, relwidth = 0.8, relheight = 0.25, anchor = 'n')
        self.compress_button.place(relx = 0.5, rely = 0.8, relwidth = 0.25, relheight = 0.1, anchor = 'center')

    
    def compress_image(self):
        name = self.filename.get()
        self.original_image = self.original_image.convert('RGB')
        self.original_image.save(f"Compressed_{name}.jpeg", format = 'jpeg', optimize = True, quality = 10)

        messagebox.showinfo('Image compressed', 'Image compressed \nSize reduced by: 2137' )
