import cv2
import numpy as np

class colorByFace:
    def __init__(self, fileName, botFile):
        self.fileName = fileName
        self.botFile = botFile

        #top/botview2 pixels
        # self.whitePixels = [( 124 , 110 ),( 131 , 128 ),( 138 , 149 ),( 133 , 95 ),( 146 , 114 ),( 149 , 134 ),( 143 , 76 ),( 152 , 97 ),( 162 , 118 )]
        # self.whiteCenter = self.whitePixels[4]
        # self.redPixels = [(158 , 69),(169 , 88),(178 , 108),(180 , 71),(189 , 91),(201 , 111),(200 , 75),(206 , 91),(218 , 113)]
        # self.redCenter = self.redPixels[4]
        # self.bluePixels = [( 176 , 129 ),( 164 , 146 ),( 150 , 161 ),( 199 , 130 ),( 183 , 145 ),( 171 , 158 ),( 219, 130 ),( 202 , 144 ),( 188 , 158 )]
        # self.blueCenter = self.bluePixels[4]
        # self.yellowPixels = [(165, 109), (174, 139), (184, 166), (178, 93), (183, 128), (193, 149), (188, 83),(196, 111), (201, 135)]
        # self.yellowCenter = self.yellowPixels[4]
        # self.orangePixels = [(128, 83), (113, 93), (97, 104), (151, 79), (137, 89), (122, 101), (173, 75), (162, 85),(150, 98)]
        # self.orangeCenter = self.orangePixels[4]
        # self.greenPixels = [(96, 122), (105, 148), (116, 173), (118, 121), (129, 147), (139, 174), (146, 118),(157, 149), (164, 174)]
        # self.greenCenter = self.greenPixels[4]

        #top/botview pixels
        # self.whitePixels = [( 102 , 114 ) ,( 110 , 131 ) ,( 122 , 152 ) ,( 113 , 93 ) ,( 128 , 113 ) ,( 133 , 133 ) ,( 121 , 73 ) ,( 132 , 91 ) ,( 146 , 113 )]
        # self.whiteCenter = self.whitePixels[4]
        # self.redPixels = [( 136 , 65 ) ,( 148 , 83 ) ,( 158 , 102 ) ,( 156 , 66 ) ,( 166 , 84 ) ,( 181 , 102 ) ,( 174 , 72 ) ,( 186 , 87 ) ,( 198 , 101 )]
        # self.redCenter = self.redPixels[4]
        # self.bluePixels = [( 163 , 120 ) ,( 150 , 139 ) ,( 137 , 161 ) ,( 180 , 121 ) ,( 168 , 139 ) ,( 157 , 157 ) ,( 199 , 121 ) ,( 185 , 140 ) ,( 173 , 154 )]
        # self.blueCenter = self.bluePixels[4]
        # self.yellowPixels = [( 90 , 114 ) ,( 102 , 135 ) ,( 114 , 158 ) ,( 102 , 92 ) ,( 113 , 113 ) ,( 128 , 134 ) , (115 , 69 ) ,( 126 , 88 ) ,( 142 , 113 )]
        # self.yellowCenter = self.yellowPixels[4]
        # self.orangePixels = [( 163 , 122 ) ,( 147 , 146 ) ,( 132 , 166 ) ,( 182 , 122 ) ,( 167 , 142 ) ,( 153 , 163 ) ,( 200 , 122 ) ,( 187 , 140 ) ,( 172 , 159 )]
        # self.orangeCenter = self.orangePixels[4]
        # self.greenPixels = [( 129 , 61 ) ,( 143 , 79 ) ,( 160 , 101 ) ,( 150 , 63 ) ,( 164 , 82 ) ,( 182 , 102 ) ,( 169 , 65 ) ,( 184 , 84 ) ,( 200 , 101 )]
        # self.greenCenter = self.greenPixels[4]

        #top/botvieww3 pixels
        self.whitePixels = [( 95 , 106 ) ,( 105 , 126 ) , ( 117 , 148 ) , ( 106 , 82 ) , ( 128 , 106 ) , ( 133 , 130 ) , ( 117 , 62 ) , ( 133 , 82 ) , ( 148 , 105 )]
        self.whiteCenter = self.whitePixels[4]
        self.redPixels = [( 136 , 54 ) , ( 149 , 73 ) , ( 163 , 94 ) , ( 156 , 58 ) , ( 168 , 76 ) , ( 184 , 97 ) , ( 173 , 61 ) , ( 186 , 79 ) , ( 203 , 97 )]
        self.redCenter = self.redPixels[4]
        self.bluePixels = [( 165 , 117 ) , ( 150 , 137 ) , ( 134 , 159 ) , ( 187 , 114 ) , ( 169 , 136 ) , ( 156 , 155 ) , ( 204 , 115 ) , ( 186 , 135 ) , ( 173 , 151 )]
        self.blueCenter = self.bluePixels[4]
        self.yellowPixels = [( 109 , 113 ) , ( 121 , 134 ) , ( 132 , 154 ) , ( 120 , 91 ) , ( 133 , 114 ) , ( 145 , 136 ) , ( 133 , 70 ) , ( 146 , 90 ) , ( 161 , 114 )]
        self.yellowCenter = self.yellowPixels[4]
        self.orangePixels = [( 180 , 122 ) , ( 164 , 145 ) , ( 147 , 165 ) , ( 201 , 122 ) , ( 184 , 143 ) , ( 169 , 161 ) , ( 217 , 122 ) , ( 201 , 141 ) , ( 186 , 158 )]
        self.orangeCenter = self.orangePixels[4]
        self.greenPixels = [( 148 , 61 ) , ( 160 , 81 ) , ( 179 , 102 ) , ( 170 , 65 ) , ( 184 , 85 ) , ( 198 , 102 ) , ( 185 , 66 ) , ( 201 , 84 ) , ( 216 , 103 )]
        self.greenCenter = self.greenPixels[4]

    def processImages(self):
        initialImage = cv2.imread(self.fileName)
        botImage = cv2.imread(self.botFile)

        hsvBot = cv2.cvtColor(botImage, cv2.COLOR_BGR2HSV)
        hsvBot = cv2.GaussianBlur(hsvBot, (5, 5), 1)

        im2 = cv2.imread(self.botFile)

        hsvIm = cv2.cvtColor(initialImage, cv2.COLOR_BGR2HSV)
        hsvIm = cv2.GaussianBlur(hsvIm, (5, 5), 1)

        return hsvIm, hsvBot, im2

    def calibrateColors(self):
        hsvIm, hsvBot, im2 = self.processImages()

        whiteCenter = hsvIm[self.whiteCenter[0]][self.whiteCenter[1]]
        redCenter = hsvIm[self.redCenter[0]][self.redCenter[1]]
        blueCenter = hsvIm[self.blueCenter[0]][self.blueCenter[1]]
        yellowCenter = hsvBot[self.yellowCenter[0]][self.yellowCenter[1]]
        orangeCenter = hsvBot[self.orangeCenter[0]][self.orangeCenter[1]]
        greenCenter = hsvBot[self.greenCenter[0]][self.greenCenter[1]]

        #allCenters = [whiteCenter, redCenter, blueCenter, yellowCenter, orangeCenter, greenCenter]
        allCenters = [redCenter, blueCenter, yellowCenter, orangeCenter, greenCenter]
        lower = [[0, 0, 99]]
        upper = [[179, 62, 255]]

        x = 10
        y = 100

        for array in allCenters:
            temparray = array.copy()
            if temparray[0] - x < 0:
                temparray[0] = 0
            else:
                temparray[0] -= x/2
            if temparray[1] - y < 0:
                temparray[1] = 0
            else:
                temparray[1] -= y
            if temparray[2] - y < 0:
                temparray[2] = 0
            else:
                temparray[2] -= y

            temp = [temparray[0], temparray[1], temparray[2]]
            lower.append(temp)

        for array in allCenters:
            temparray = array.copy()
            if temparray[0] + x > 180:
                temparray[0] = 180
            else:
                temparray[0] += x/2
            if temparray[1] + y > 250:
                temparray[1] = 255
            else:
                temparray[1] += y
            if temparray[2] + y > 250:
                temparray[2] = 255
            else:
                temparray[2] += y

            temp = [temparray[0], temparray[1], temparray[2]]
            upper.append(temp)

        #print(allCenters)
        #print(lower)
        #print(upper)

        lowerDict = {'r': lower[1], 'o': lower[4], 'y': lower[3],
                     'g': lower[5], 'b': lower[2], 'w': lower[0]}  # HSV color values
        upperDict = {'r': upper[1], 'o': upper[4], 'y': upper[3],
                     'g': upper[5], 'b': upper[2], 'w': upper[0]}

        #print(upperDict)

        return upperDict, lowerDict


    def pixelColor(self, im1, im2, pixelList):
        colorsDict = {'r': [0, 0, 255], 'o': [0, 165, 255], 'y': [0, 255, 255],
                      'g': [60, 255, 50], 'b': [255, 0, 0], 'w': [255, 255, 255]}  # BGR color values
        # upperDict = {'r': [180, 255, 255], 'o': [20, 255, 255], 'y': [44, 255, 255],
        #              'g': [90, 255, 255], 'b': [140, 255, 255], 'w': [179, 62, 255]}  # HSV color values
        # lowerDict = {'r': [119, 50, 70], 'o': [8, 170, 50], 'y': [21, 90, 50],
        #              'g': [45, 50, 45], 'b': [91, 200, 50], 'w': [0, 0, 99]}
        upperDict, lowerDict = self.calibrateColors()
        pixelVals = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

        print("upperDict: ", upperDict)
        print("lowerDict: ", lowerDict)

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

        im1, im2, _ = pixelDetector.processImages()

        topPixels = [self.whitePixels, self.redPixels, self.bluePixels]
        botPixels = [self.yellowPixels, self.orangePixels, self.greenPixels]

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
    pixelDetector = colorByFace('topview3.jpg', 'botview3.jpg')

    faceList = pixelDetector.allFaces()

    print(faceList)

    print('White:', faceList[0])
    print('Red:', faceList[1])
    print('Blue:', faceList[2])
    print('Yellow:', faceList[3])
    print('Orange:', faceList[4])
    print('Green:', faceList[5])

    #cv2.imshow('HsvBot', hsvBot)
    #cv2.imshow('Im2', im2)
    #cv2.imshow('HsvTop', hsvIm)

    plainBot = cv2.imread(pixelDetector.botFile)
    plainTop = cv2.imread(pixelDetector.fileName)
    cv2.imshow('Topview', plainTop)
    cv2.imshow('Botview', plainBot)

    pixelDetector.calibrateColors()

    cv2.waitKey(0)
    cv2.destroyAllWindows()