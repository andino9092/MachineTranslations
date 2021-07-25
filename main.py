from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
import os

Window.size = (1080, 720)

class UI(Widget):

    folderButton = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(UI, self).__init__(**kwargs)
        self.minimum_height = 1
        self.minimum_width = 3
        self.folderButton.bind(on_press = FolderButton.callback)

class FolderButton(Button):
    
    def callback(instance):
        os.system('explorer')
    

class IntroLabel(Label):
    pass

class MTApp(App):
    def build(self):
        return UI()


if __name__ == '__main__':
    MTApp().run()