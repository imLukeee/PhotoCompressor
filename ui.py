import customtkinter as ctk

class ImportImageButton(ctk.CTkButton):
    def __init__(self, parent, font, func):
        super().__init__(master = parent, text = 'Select Image', font = font, command = func)
        self.place(relx = 0.5, rely = 0.5, relwidth = 0.5, relheight = 0.075, anchor = 'center')


class ImageCanvas(ctk.CTkCanvas):
    def __init__(self, parent, image):
        super().__init__(master = parent, background = 'white')
        self.place(relx = 0.5, rely = 0.05, relwidth = 0.75, relheight = 0.5, anchor = 'n')
        self.original = image
        self.image = self.original

        self.bind('<Configure>', self.resize_image)

        self.create_image(0, 0, anchor = 'nw', image = image)
    
    def resize_image(self, event):
        self.image_ratio = self.original.width() / self.original.height()
        
        self.canvas_width = event.width
        self.canvas_height = event.height

        #get ratio to scale image
        self.image_width = self.image.width()
        self.image_height = self.image.height()
        
        #self.place_image(self.image, self.width, self.height)

    def place_image(self, image, width, height):
        pass 