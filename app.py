from langdetect import detect
from PIL import Image
from googletrans import Translator, constants
from pprint import pprint
import pytesseract

def locateText():

    return

def locateTextBox():
    return

def translate():
    return

def getStringFromImage():
    return

pytesseract.pytesseract.tesseract_cmd = r'/opt/local/bin/tesseract'
img = Image.open("TestingPics/Lookism2_kor.png")
img = img.convert('L')

find = pytesseract.image_to_data(img, lang="kor")
print(find[0])
lookism = pytesseract.image_to_string(img, lang="kor")
data = pytesseract.image_to_string(r'TestingPics/KoreanRegon.PNG', lang = "kor")
print(lookism)