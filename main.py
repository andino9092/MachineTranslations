from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.core.text import LabelBase
from kivy.lang import Builder
from tkinter import Tk, filedialog
from PIL import Image, ImageFont
from kivy.uix.dropdown import DropDown
from kivy.factory import Factory
from kivy.uix.popup import Popup
import easyocr
import os
import translate
import threading
import time

Tk().withdraw()

Window.size = (540, 720)

fontSize = 16
reader = easyocr.Reader(['ch_sim'])
loading = False

langs = ["Chinese", "Korean", "Japanese"]

LabelBase.register(name = 'WildWords', fn_regular="wildWords.ttf")

class UI(Widget):

    folderButton = ObjectProperty(None)
    authorLabel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(UI, self).__init__(**kwargs)
        self.minimum_height = 1
        self.minimum_width = 3
        self.folderButton.bind(on_release = FolderButton.callback)
        self.authorLabel.text = "Andy Li"

class FolderButton(Button):
    
    def callback(self):
        font = ImageFont.truetype("wildWords.ttf", fontSize)
        folderName = filedialog.askdirectory()
        if folderName == "":
            return
        
        print(folderName)
        fileList = os.listdir(folderName)
        os.chdir(folderName)
        if os.path.isdir("Translated"):
            pass
        else:
            os.mkdir("Translated")
        targetDirectory = folderName + "/Translated"
        print(fileList)
        for file in fileList:
            translate.translate(file, targetDirectory, fontSize, font, reader)

    

class LoadingPopup(Popup):
    pass

class AuthorLabel(Label):
    pass

class CustomDropDown(DropDown):
    pass

class IntroLabel(Label):
    pass

class MTApp(App):
    def build(self):
        self.title = "Machine Translations"
        return UI()


if __name__ == '__main__':
    MTApp().run()