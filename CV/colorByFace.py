import cv2
import numpy as np

#yellow.png
#orangePixels = [(31, 139), (38, 170), (48, 206), (40, 107), (50, 140), (62, 178), (51, 73), (62, 106), (76, 144)]
#greenPixels = [(80, 58), (95, 87), (111, 125), (125, 58), (128, 89), (156, 127), (172, 76), (184, 102), (195, 133)]
#whitePixels = [(110, 165), (92, 197), (75, 222), (154, 164), (132, 196), (115, 221), (192, 168), (170, 194), (160, 216)]

#bofa.jpg
# orangePixels = [( 108 , 113 ) ,( 116 , 133 ) ,( 124 , 153 ) ,( 117 , 96 ) ,( 126 , 114 ) ,( 135 , 137 ) ,( 127 , 74 ) ,( 136 , 93 ) ,( 147 , 114 )]
# greenPixels = [( 144 , 65 ) ,( 154 , 84 ) ,( 166 , 105 ) ,( 167 , 70 ) ,( 176 , 88 ) ,( 190 , 105 ) ,( 184 , 73 ) ,( 195 , 89 ) ,( 209 , 107 )]
# whitePixels = [( 166 , 125 ) ,( 153 , 144 ) ,( 140 , 164 ) ,( 189 , 124 ) ,( 177 , 139 ) ,( 162 , 162 ) ,( 209 , 122 ) ,( 194 , 143 ) ,( 180 , 157 )]

#test2.jpg
# orangePixels = [( 109 , 116 ) ,( 118 , 136 ) ,( 127 , 165 ) ,( 117 , 89 ) ,( 125 , 113 ) ,( 136 , 141 ) ,( 123 , 62 ) ,( 133 , 84 ) ,( 146 , 111 )]
# greenPixels = [( 142 , 53 ) ,( 152 , 71 ) ,( 168 , 94 ) ,( 171 , 54 ) ,( 183 , 73 ) ,( 203 , 96 ) ,( 196 , 58 ) ,( 211 , 73 ) ,( 235 , 97 )]
# whitePixels = [( 172 , 123 ) ,( 159 , 152 ) ,( 148 , 176 ) ,( 207 , 122 ) ,( 191 , 149 ) ,( 179 , 171 ) ,( 234 , 120 ) ,( 216 , 146 ) ,( 204 , 167 )]

#topview.jpg
orangePixels = [( 142 , 58 ) ,( 156 , 78 ) ,( 174 , 103 ) ,( 162 , 64 ) ,( 176 , 81 ) ,( 191 , 102 ) ,( 177 , 67 ) ,( 191 , 83 ) ,( 209 , 104 )]
greenPixels = [( 174 , 124 ) ,( 153 , 144 ) ,( 136 , 164 ) ,( 192 , 122 ) ,( 174 , 142 ) ,( 158 , 160 ) ,( 208 , 121 ) ,( 191 , 140 ) ,( 175 , 155 )]
whitePixels = [( 100 , 108 ) ,( 108 , 128 ) ,( 121 , 153 ) ,( 111 , 89 ) ,( 124 , 100 ) ,( 137 , 133 ) ,( 125 , 64 ) ,( 138 , 86 ) ,( 153 , 112 )]

#botview.jpg
redPixels = [( 100 , 73 ) ,( 86 , 87 ) ,( 66 , 103 ) ,( 129 , 73 ) ,( 114 , 86 ) ,( 96 , 102 ) ,( 158 , 71 ) ,( 144 , 86 ) ,( 133 , 102 )]
bluePixels = [( 59 , 128 ) ,( 72 , 156 ) ,( 83 , 183 ) ,( 91 , 129 ) ,( 100 , 158 ) ,( 113 , 186 ) ,( 128 , 127 ) ,( 136 , 161 ) ,( 143 , 189 )]
yellowPixels = [( 150 , 117 ) ,( 160 , 149 ) ,( 166 , 180 ) ,( 163 , 98 ) ,( 168 , 128 ) ,( 175 , 155 ) ,( 171 , 83 ) ,( 175 , 112 ) ,( 180 , 138 )]

fileName = 'topview.jpg'
#fileName = 'bofa.jpg'
#fileName = 'test2.jpg'
botFile = 'botView.jpg'

initialImage = cv2.imread(fileName)
botImage = cv2.imread(botFile)

im2 = cv2.imread(fileName)

hsvIm = cv2.cvtColor(initialImage, cv2.COLOR_BGR2HSV)
hsvIm = cv2.GaussianBlur(hsvIm, (5, 5), 4)

hsvBot = cv2.cvtColor(botImage, cv2.COLOR_BGR2HSV)
hsvBot = cv2.GaussianBlur(hsvBot, (5, 5), 4)


def pixelColor(im1, im2, pixelList):

    colorsDict = {'r': [0, 0, 255], 'o': [0, 165, 255], 'y': [0, 255, 255],
                  'g': [60, 255, 50], 'b': [255, 0, 0], 'w': [255, 255, 255]}  # BGR color values
    upperDict = {'r': [180, 255, 255], 'o': [20, 255, 255], 'y': [44, 255, 255],
                 'g': [90, 255, 255],'b': [140, 255, 200], 'w': [179, 62, 255]}  # HSV color values
    lowerDict = {'r': [170, 50, 70], 'o': [10, 170, 50], 'y': [21, 100, 50],
                 'g': [45, 50, 45], 'b': [91, 55, 50], 'w': [0, 0, 99]}
    pixelVals = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    i = 0

    for row, col in pixelList:
        initialImage = im1

        im2[row, col] = [147, 20, 255]

        pixel = initialImage[row, col]

        print('Row:', row, ' Col:', col, 'Pixel:', pixel)

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


orangeFace = pixelColor(hsvIm, im2, orangePixels)
greenFace = pixelColor(hsvIm, im2, greenPixels)
whiteFace = pixelColor(hsvIm, im2, whitePixels)

redFace = pixelColor(hsvBot, im2, redPixels)
blueFace = pixelColor(hsvBot, im2, bluePixels)
yellowFace = pixelColor(hsvBot, im2, yellowPixels)

print('Orange:', orangeFace)
print('Green:', greenFace)
print('White:', whiteFace)
print('Red:', redFace)
print('Blue:', blueFace)
print('Yellow:', yellowFace)


cv2.imshow('image', im2)
#cv2.imshow('inIm', hsvIm)
#cv2.imwrite('ChosePixels.png', initialImage)
#cv2.imwrite('HSVImg.png', hsvIm)

plainBot = cv2.imread(botFile)
cv2.imshow('Botview', plainBot)

#cv2.waitKey(0)
#cv2.destroyAllWindows()

#white + red +





