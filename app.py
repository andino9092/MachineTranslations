from os import remove
from PIL import Image, ImageEnhance
from deep_translator import GoogleTranslator
from pprint import pprint
from google_trans_new import google_translator
import easyocr
import string

from torch.utils import data

editLocation = "TestingPics/Edit.png"
lang = "ch_tra"

class Translation:
    def __init__(self, boxes, translation):
        self.boxes = boxes
        self.translation = translation
    def getTranslation(self):
        return self.translation
    def getBoxes(self):
        return self.boxes

class Box:
    def __init__(self, a, b, c, d):
        self.topLeft = a
        self.topRight = b
        self.bottomLeft = c
        self.bottomRight = d
    def getTopLeft(self):
        return self.topLeft
    def getTopRight(self):
        return self.topRight
    def getBottomLeft(self):
        return self.bottomLeft
    def getBottomRight(self):
        return self.bottomRight

def load():
    global reader
    reader = easyocr.Reader(['ch_tra'], gpu = False)

def loadImage(imageLocation):
    global image
    image = Image.open(imageLocation)
    imgSave = imageEnhance(image).save(editLocation)
    global rawImageInfo
    rawImageInfo = reader.readtext(editLocation, paragraph=True)

def imageEnhance(image):
    img = image.convert('L')
    enhancer = ImageEnhance.Contrast(img)
    newImg = enhancer.enhance(5)
    return newImg

# make sure its a phrase and not just symbols
def langCheck(phrase):
    translator = google_translator()
    phrase = phrase.translate(str.maketrans("", "", string.punctuation))
    symbols = "!@#$%^&*()_-+={}[]"
    try:
        print(translator.detect(phrase))
        print(phrase)
        if translator.detect(phrase)[0] == "zh-CN" and not phrase.isdigit():
            return True
    except Exception:
        pass
    return False

#fix remove noise, not covering text
def removeNoise():
    clone = rawImageInfo.copy()
    for box in clone:
        #print(box)
        #print(box[1] + " " + str(not langCheck(box[1])))
        if not langCheck(box[1]):
            rawImageInfo.remove(box)
    #print(rawImageInfo)

def createDictionary(translated):
    global langText
    langText = []
    translations = []
    for data in rawImageInfo:
        index = 0
        translations.append(Translation(data[0], translated[index]))
        index += 1
        langText.append(data[1])
    global dataDict
    dataDict = dict(zip(langText, translations))
    

def translateText():
    text = []
    for data in rawImageInfo:
        text.append(data[1])
    translated = GoogleTranslator(source = "auto", target = "en").translate_batch(text)
    return translated
    
def whiten():
    for key in dataDict:
        boxes = dataDict[key].getBoxes()
        for i in range(boxes[0][0], boxes[1][0]):
            for m in range(boxes[0][1], boxes[2][1]):
                image.putpixel( (i,m), (255, 255, 255))
    imgSave = image.save(editLocation)
# [[383, 63], [457, 63], [457, 99], [383, 99]]
# [[614, 52], [807, 52], [807, 119], [614, 119]]
# [[64, 546], [243, 546], [243, 610], [64, 610]]
# [[645, 677], [773, 677], [773, 709], [645, 709]]
# [[698, 732], [802, 732], [802, 794], [698, 794]]
# [[99, 877], [239, 877], [239, 917], [99, 917]]
def translateImage():
    #TODO
    return

def main():
    load()
    loadImage("TestingPics/002.jpg")
    removeNoise()
    translated = translateText()
    createDictionary(translated)
    whiten()
main()


# Dictionary for boxes: dataDict
# Array for raw text: langText
# Idea for another project: maybe use machine learning to train a bot to understand informal korean
