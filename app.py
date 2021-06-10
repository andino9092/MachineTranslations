from os import remove
from PIL import Image, ImageEnhance
from deep_translator import GoogleTranslator
from pprint import pprint
from google_trans_new import google_translator
import easyocr
import string

class Translation:
    def __init__(self, boxes, translation):
        self.boxes = boxes
        self.translation = translation
    def getTranslation(self):
        return self.translation
    def getBoxes(self):
        return self.boxes
    
editLocation = "TestingPics/Edit.png"
lang = "ch_tra"

def load():
    global reader
    reader = easyocr.Reader(['ch_tra'], gpu = False)

def loadImage(imageLocation):
    image = Image.open(imageLocation)
    imgSave = imageEnhance(image).save(editLocation)
    global rawImageInfo
    rawImageInfo = reader.readtext(editLocation, paragraph=True)


def imageEnhance(image):
    img = image.convert('L')
    enhancer = ImageEnhance.Contrast(img)
    newImg = enhancer.enhance(5)
    return newImg

def locateText():
    #TODO
    return

def locateTextBox():
    #TODO
    return

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

def translateImage():
    #TODO
    return

def main():
    load()
    loadImage("TestingPics/002.jpg")
    removeNoise()
    translated = translateText()
    createDictionary(translated)

main()

#maybe use machine learning to train a bot to understand informal korean
