import cv2
import numpy as np

class colorByFace:
    def __init__(self, fileName, botFile):
        self.fileName = fileName
        self.botFile = botFile

    def getTopPixels(self):
        orangePixels = [(142, 58), (156, 78), (174, 103), (162, 64), (176, 81), (191, 102), (177, 67), (191, 83), (209, 104)]
        greenPixels = [(174, 124), (153, 144), (136, 164), (192, 122), (174, 142), (158, 160), (208, 121), (191, 140), (175, 155)]
        whitePixels = [(100, 108), (108, 128), (121, 153), (111, 89), (124, 100), (137, 133), (125, 64), (138, 86), (153, 112)]
        return [orangePixels, greenPixels, whitePixels]

    def getBotPixels(self):
        redPixels = [(101, 73), (86, 87), (64, 103), (126, 73), (114, 87), (96, 103), (158, 70), (145, 85), (130, 103)]
        bluePixels = [(59, 128), (72, 156), (83, 183), (91, 129), (100, 158), (113, 186), (128, 127), (136, 161), (143, 189)]
        yellowPixels = [(150, 117), (160, 149), (166, 180), (163, 98), (168, 128), (175, 155), (171, 83), (175, 112), (180, 138)]
        return [redPixels, bluePixels, yellowPixels]

    def processImages(self):
        initialImage = cv2.imread(self.fileName)
        botImage = cv2.imread(self.botFile)

        hsvBot = cv2.cvtColor(botImage, cv2.COLOR_BGR2HSV)
        hsvBot = cv2.GaussianBlur(hsvBot, (5, 5), 4)

        im2 = cv2.imread(self.botFile)

        hsvIm = cv2.cvtColor(initialImage, cv2.COLOR_BGR2HSV)
        hsvIm = cv2.GaussianBlur(hsvIm, (5, 5), 4)

        return hsvIm, hsvBot, im2

    def pixelColor(self, im1, im2, pixelList):
        colorsDict = {'r': [0, 0, 255], 'o': [0, 165, 255], 'y': [0, 255, 255],
                      'g': [60, 255, 50], 'b': [255, 0, 0], 'w': [255, 255, 255]}  # BGR color values
        upperDict = {'r': [180, 255, 255], 'o': [20, 255, 255], 'y': [44, 255, 255],
                     'g': [90, 255, 255], 'b': [140, 255, 200], 'w': [179, 62, 255]}  # HSV color values
        lowerDict = {'r': [170, 50, 70], 'o': [10, 170, 50], 'y': [21, 100, 50],
                     'g': [45, 50, 45], 'b': [91, 55, 50], 'w': [0, 0, 99]}
        pixelVals = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

        i = 0
        for row, col in pixelList:
            initialImage = im1

            im2[row, col] = [147, 20, 255]

            pixel = initialImage[row, col]

            print('Row:', row, ' Col:', col, 'Pixel:', pixel) #TODO: for debugging, can comment out before implementation

            for colorName, color in colorsDict.items():
                lower = np.array(lowerDict.get(colorName))
                upper = np.array(upperDict.get(colorName))

                if np.all(pixel >= lower) and np.all(pixel <= upper):
                    pixelVals[i] = colorName
                    break

            i += 1

        face = np.array(pixelVals)
        print(pixelVals)
        return face

    def allFaces(self, im1, im2, topPixels, botPixels):
        faceList = []

        for pixelList in topPixels:
            faces = self.pixelColor(im1, im2, pixelList)
            faceList.append(np.array(faces))

        for pixels in botPixels:
            faces = self.pixelColor(im2, im1, pixels)
            faceList.append(np.array(faces))

        return faceList

if __name__ == "__main__":
    pixelDetector = colorByFace('topview.jpg', 'botview.jpg')
    hsvIm, hsvBot, im2 = pixelDetector.processImages()
    topPixels = pixelDetector.getTopPixels()
    botPixels = pixelDetector.getBotPixels()

    faceList = pixelDetector.allFaces(hsvIm, hsvBot, topPixels, botPixels)

    print('Orange:', faceList[0])
    print('Green:', faceList[1])
    print('White:', faceList[2])
    print('Red:', faceList[3])
    print('Blue:', faceList[4])
    print('Yellow:', faceList[5])

    cv2.imshow('HsvBot', hsvBot)
    cv2.imshow('Im2', im2)
    cv2.imshow('HsvTop', hsvIm)

    plainBot = cv2.imread(pixelDetector.botFile)
    plainTop = cv2.imread(pixelDetector.fileName)
    cv2.imshow('Topview', plainTop)
    cv2.imshow('Botview', plainBot)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

