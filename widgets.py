from colors import *
import customtkinter as ctk

class SegmentedSelector(ctk.CTkSegmentedButton):
    def __init__(self, parent, variable, values):
        super().__init__(master = parent,
                        variable = variable,
                        values = values, 
                        corner_radius = 12,
                        text_color = TEXT_COLOR,
                        fg_color = BG_COLOR,
                        selected_color = BUTTON_COLOR,
                        unselected_color = MENU_BUTTON_HOVER,
                        selected_hover_color = BUTTON_HOVER,
                        unselected_hover_color = MENU_BUTTON_HOVER)
        

class ConfirmSettingsButton(ctk.CTkButton):
    def __init__(self, parent, text, command, column):
        super().__init__(master = parent,
                         text = text,
                         command = command,
                         text_color = TEXT_COLOR,
                         fg_color = BUTTON_COLOR,
                         hover_color = BUTTON_HOVER,
                         corner_radius = 12,
                         height = 50)
        self.grid(row = 0, column = column, sticky = 'nsew', padx = 10, pady = 20)