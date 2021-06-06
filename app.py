from os import remove
from langdetect import detect, LangDetectException
from PIL import Image, ImageEnhance
from deep_translator import GoogleTranslator
from pprint import pprint
import easyocr
import string

editLocation = "TestingPics/Edit.png"
lang = "ko"

def load():
    global reader
    reader = easyocr.Reader(['ko', 'en'], gpu = False)

def loadImage(imageLocation):
    image = Image.open(imageLocation)
    imgSave = imageEnhance(image).save(editLocation)
    global rawImageInfo
    rawImageInfo = reader.readtext(editLocation)


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

def langCheck(phrase):
    phrase = phrase.translate(str.maketrans("", "", string.punctuation))
    #print(phrase)
    symbols = "!@#$%^&*()_-+={}[]"
    for letter in phrase:
        try:
            if detect(letter) == lang and not (letter in symbols) and not letter.isdigit():
                return True
        except LangDetectException:
            pass
    return False

def removeNoise():
    clone = rawImageInfo.copy()
    for box in clone:
        #print(box)
        #print(box[1] + " " + str(not langCheck(box[1])))
        if not langCheck(box[1]):
            rawImageInfo.remove(box)
    #print(rawImageInfo)

def createDictionary():
    langText = []
    boxes = []
    for data in rawImageInfo:
        boxes.append(data[0])
        langText.append(data[1])
    global dataDict
    dataDict = dict(zip(langText, boxes))
    print(dataDict)

def translateText():
    text = []
    for data in rawImageInfo:
        text.append(data[1])
    print(text)
    translated = GoogleTranslator(source = "auto", target = "en").translate_batch(text)
    print(translated)
    return text

def translateImage():
    #TODO
    return

def main():
    load()
    loadImage("TestingPics/Lookism3_kor.png")
    removeNoise()
    translateText()
    createDictionary()

main()

#maybe use machine learning to train a bot to understand informal korean