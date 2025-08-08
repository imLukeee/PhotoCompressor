import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import filedialog

class Initiate_App(ctk.CTkButton):
    def __init__(self, parent, font):
        super().__init__(master = parent, text = 'Select Image', font = font, command = self.import_image)
        self.place(relx = 0.5, rely = 0.5, relwidth = 0.5, relheight = 0.075, anchor = 'center')
        self.parent = parent

    def import_image(self):
        filepath = filedialog.askopenfilename()
        if not filepath:
            return
        
        self.original_image = Image.open(filepath)
        self.place_forget()

        self.image_preview = ImageCanvas(self.parent, self.original_image)
        self.controls = UserControls(self.parent, self.original_image)


class ImageCanvas(ctk.CTkCanvas):
    def __init__(self, parent, pil_image):
        super().__init__(master = parent, background = "#484848")
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
        super().__init__(parent, fg_color='white')
        self.original_image = original
        self.place(relx = 0.05, rely = 0.6, relwidth = 0.9, relheight = 0.35, anchor = 'nw')

        self.compress_button = ctk.CTkButton(self, text = 'Compress', command = self.compress_image)

        self.compress_button.place(relx = 0.5, rely = 0.8, relwidth = 0.25, relheight = 0.1, anchor = 'center')

    
    def compress_image(self):
        #self.original_image.save(f"Compressed_{self.original_image.name}.jpeg", optimize = True, quality = 10)
        pass