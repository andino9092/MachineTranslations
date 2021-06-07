from os import remove
from langdetect import detect, LangDetectException
from PIL import Image, ImageEnhance
from deep_translator import GoogleTranslator
from pprint import pprint
import easyocr
import string
# Papago Translator
# Note

# You need to require a client id and client secret key if you want to
# use the papago translator. visit the official website for more information 
# about how to get one.

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

def langCheck(phrase):
    phrase = phrase.translate(str.maketrans("", "", string.punctuation))
    #print(phrase)
    symbols = "!@#$%^&*()_-+={}[]"
    for letter in phrase:
        
        try:
            if detect(letter) == "zh-cn" and not (letter in symbols) and not letter.isdigit():
                return True
        except LangDetectException:
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
    loadImage("TestingPics/002.jpg")
    print(rawImageInfo)
    removeNoise()
    print(rawImageInfo)
    translateText()
    createDictionary()

main()

#maybe use machine learning to train a bot to understand informal korean
