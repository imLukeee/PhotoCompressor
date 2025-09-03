from customtkinter import get_appearance_mode
#Colors 
BG_COLOR = ("#caebe0", '#1E1E1F')
MENU_BUTTON_HOVER = ("#3DCC90", "#323233")
ACCENT_COLOR = ('#c0ffee', '#484848')
BUTTON_COLOR = ("#40a78b", "#2c6c8f")
BUTTON_HOVER = ("#129572", "#398ab7")
TEXT_COLOR = ("#111827", "#F9FAFB")
SEG_BUTTON_BG = ('#')

#Compression Quality Map
QUALITY_DICT = {'Lowest size': 10,
           'Balanced': 50,
           'Highest quality': 80}

QUALITY_LIST = ['Lowest size', 'Balanced', 'Highest quality']

SETTINGS_FILENAME = 'settings.csv'

SETTINGS_DEAFULTS = ['./CompressedImages', 'Dark', 'Lowest size']


def themed_color(color_tuple):
    mode = get_appearance_mode()
    if mode == 'Light':
        return color_tuple[0]
    else: 
        return color_tuple[1]
