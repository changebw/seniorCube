import cv2
import numpy as np

class colorByFace:
    def __init__(self, fileName, botFile):
        self.fileName = fileName
        self.botFile = botFile

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

        face = pixelVals
        print(pixelVals)
        return face

    def allFaces(self):
        faceList = []

        im1, im2, _ = self.processImages()

        whitePixels = [( 124 , 110 ) ,( 131 , 128 ) ,( 138 , 149 ) ,( 133 , 95 ) ,( 146 , 114 ) ,( 149 , 134 ) ,( 143 , 76 ) ,( 152 , 97 ) ,( 162 , 118 )]
        redPixels = [(158, 69),(169, 88),(178, 108),(180, 71),(189, 91),(201, 111),(200, 75),(206, 91),(218, 113)]
        bluePixels = [( 176 , 129 ) ,( 164 , 146 ) ,( 150 , 161 ) ,( 199 , 130 ) ,( 183 , 145 ) ,( 171 , 158 ) ,( 219 , 130 ) ,( 202 , 144 ) ,( 188 , 158 )]

        whitePixels = [(i[0]//2,i[1]//2) for i in whitePixels]
        redPixels = [(i[0]//2,i[1]//2) for i in redPixels]
        bluePixels = [(i[1]//2,i[1]//2) for i in bluePixels]

        # whitePixels = [(int(x * 2/3), int(y * 3/8)) for x, y in whitePixels]
        # redPixels = [(int(x * 2/3), int(y * 3/8)) for x, y in redPixels]
        # bluePixels = [(int(x * 2/3), int(y * 3/8)) for x, y in bluePixels]
        topPixels = [whitePixels, redPixels, bluePixels]

        yellowPixels = [(165, 109), (174, 139), (184, 166), (178, 93), (183, 128), (193, 149), (188, 83), (196, 111), (201, 135)]
        orangePixels = [(128, 83), (113, 93), (97, 104), (151, 79), (137, 89), (122, 101), (173, 75), (162, 85), (150, 98)]
        greenPixels = [(96, 122), (105, 148), (116, 173), (118, 121), (129, 147), (139, 174), (146, 118), (157, 149),(164, 174)]

        yellowPixels = [(i[0]//2,i[1]//2) for i in yellowPixels]
        orangePixels = [(i[0]//2,i[1]//2) for i in orangePixels]
        greenPixels = [(i[0]//2,i[1]//2) for i in greenPixels]

        # yellowPixels = [(int(x * 2/3), int(y * 3/8)) for x, y in yellowPixels]
        # orangePixels = [(int(x * 2/3), int(y * 3/8)) for x, y in orangePixels]
        # greenPixels = [(int(x * 2/3), int(y * 3/8)) for x, y in greenPixels]

        botPixels = [yellowPixels, orangePixels, greenPixels]

        for pixelList in topPixels:
            faces = self.pixelColor(im1, im2, pixelList)
            faceList.append(faces)

        for pixels in botPixels:
            faces = self.pixelColor(im2, im1, pixels)
            faceList.append(faces)

        temp = [[y[x*3:x*3+3] for x in range(3)] for y in faceList]

        #print(faceList)

        #print(temp)

        return temp

if __name__ == "__main__":
    self = colorByFace('topview.bmp', 'botview.bmp')
    faceList = self.allFaces()

    print('White:', faceList[0])
    print('Red:', faceList[1])
    print('Blue:', faceList[2])
    print('Yellow:', faceList[3])
    print('Orange:', faceList[4])
    print('Green:', faceList[5])

    #cv2.imshow('HsvBot', hsvBot)
    #cv2.imshow('Im2', im2)
    #cv2.imshow('HsvTop', hsvIm)

    plainBot = cv2.imread(self.botFile)
    plainTop = cv2.imread(self.fileName)
    cv2.imshow('Topview', plainTop)
    cv2.imshow('Botview', plainBot)

    cv2.waitKey(0)
    cv2.destroyAllWindows()