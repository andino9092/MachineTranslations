from os import remove
from PIL import Image, ImageEnhance, ImageFont, ImageDraw
from deep_translator import GoogleTranslator
from pprint import pprint
from polyglot.detect import Detector
import easyocr
import string
import textwrap


from torch.utils import data

editLocation = "TestingPics/Edit.png"
api_key = "a16c615c2b55e8319c15c6b0ee66e7ce"
fontSize = 18

fontDict = {
    16: 21,
    18: 24,
    20: 27,
    24: 32,
}
class Translation:
    def __init__(self, boxes, translation):
        self.boxes = boxes
        self.translation = translation
    def getTranslation(self):
        return self.translation
    def getBoxes(self):
        return self.boxes

def load():
    global reader
    reader = easyocr.Reader(['ch_sim'], gpu = False)

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
    phrase = phrase.translate(str.maketrans("", "", string.punctuation))
    symbols = "!@#$%^&*()_-+={}[]"
    data = Detector(phrase, quiet = True).language.name
    print(data)
    if data == "Chinese" and not phrase.isdigit():
        return True
    return False

#fix remove noise, not covering text
def removeNoise():
    clone = rawImageInfo.copy()
    for box in clone:
        #print(box)
        #print(box[1] + " " + str(not langCheck(box[1])))
        if not langCheck(box[1]):
            rawImageInfo.remove(box)
    print(rawImageInfo)

def createDictionary(translated):
    global langText
    langText = []
    translations = []
    index = 0
    for data in rawImageInfo:
        translations.append(Translation(data[0], translated[index]))
        index += 1
        langText.append(data[1])
    print(translations)
    global dataDict
    dataDict = dict(zip(langText, translations))
    

def translateText():
    text = []
    print(text)
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

def splitTranslation(boxes, translated):
    pixelSize = fontDict[fontSize]
    threshold = boxes[1][0] - boxes[0][0] 
    translatedList = translated.split(" ")
    newTranslation = ""
    currentPixels = 0
    for line in translatedList:
        lineSize = len(line) * pixelSize
        if len(translatedList) == 1:
            newTranslation += line
            break
        if currentPixels + lineSize - 50 > threshold:
            newTranslation += "\n" + line + " "
            currentPixels = 0
        else:
            newTranslation += line + " "
            currentPixels += lineSize
    return newTranslation

def findMiddle(boxes):
    return (boxes[0][0] + (boxes[1][0] - boxes[0][0]) / 2, boxes[0][1] + (boxes[2][1] - boxes[0][1]) / 2) 

def writeToImage():
    font = ImageFont.truetype("wildWords.ttf", fontSize)
    whitenedImg = Image.open(editLocation)
    d = ImageDraw.Draw(whitenedImg)
    for key in dataDict:
        boxes = dataDict[key].getBoxes()
        translated = dataDict[key].getTranslation()
        print(splitTranslation(boxes, translated))
        d.text(findMiddle(boxes), splitTranslation(boxes, translated), anchor = "mm", spacing = 10, fill = "black", align = "center", font=font)
    imgSave = whitenedImg.save(editLocation)
    whitenedImg.close()

def main():
    load()
    loadImage("TestingPics/009.jpg")
    removeNoise()
    translated = translateText()
    createDictionary(translated)
    whiten()
    writeToImage()
main()

# Improvements that could be made:
# - Let program scan multiple files
# - change background to whatever closest color is rather than just white
# - Fix scaling of words
# - Convert into an executable
# 
# Dictionary for boxes: dataDict
# Array for raw text: langText
# Idea for another project: maybe use machine learning to train a bot to understand informal korean
