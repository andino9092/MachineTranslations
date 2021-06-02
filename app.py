from langdetect import detect
from PIL import Image, ImageEnhance
from googletrans import Translator, constants
from pprint import pprint
import pytesseract

def imageEnhance(image):
    img = Image.open(image)
    img = img.convert('L')
    # enhancer = ImageEnhance.Contrast(img)
    # newImg = enhancer.enhance(2)
    return img

def locateText():

    return

def locateTextBox():
    return

def translate():
    return

def getStringFromImage():
    return

pytesseract.pytesseract.tesseract_cmd = r'Z:\Tesseract\tesseract'
#pytesseract.pytesseract.tesseract_cmd = r'/opt/local/bin/tesseract'
imageLocation = "TestingPics/Lookism_kor.png"

img = imageEnhance(imageLocation)
text = pytesseract.image_to_string(img, lang = "kor+eng", config='psm 12')
print(text)
img1 = img.save("TestingPics/Lookism2_kor_edited.png")
#find = pytesseract.image_to_data(img, lang="kor").split("\n")
