from langdetect import detect
from PIL import Image
from googletrans import Translator, constants
from pprint import pprint
import pytesseract


img = Image.open("TestingPics/Lookism.png").convert('L')

pytesseract.pytesseract.tesseract_cmd = r'Z:\Tesseract\tesseract'

print(pytesseract.image_to_string(r'TestingPics\python.jpg'))
lookism = pytesseract.image_to_string(img, lang="kor")
data = pytesseract.image_to_string(r'TestingPics\KoreanRegon.PNG', lang = "kor")


print(lookism)

translation = Translator.translate("hello")
print(translation)