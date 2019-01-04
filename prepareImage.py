from PIL import Image, ImageDraw
from pprint import pprint as pp
import numpy as np
import collections
import time

def prepare(pathToImage):
    image = Image.open(pathToImage)
    try:
        image = contrast(image)
        image = cutEdges(image)
        image = removeNoiseOnBorder(image)
        image = cutEdges(image)
        image = removeNoise(image)
        image = cutEdges(image)
        image = image.resize((32,32))
        # image.show()
    except Exception:
        print("-" * 20)
        print(pathToImage)
        exit()
    image.save("../prepare/" + pathToImage[9:])
    return list(image.getdata())

def contrast(image):
    image = image.convert("L")
    width = image.size[0]
    height = image.size[1]
    pixs = image.load()
    draw = ImageDraw.Draw(image)

    for i in range(width):
        for j in range(height):
            if np.mean(pixs[i, j]) < 220:
                draw.point((i, j), 0)
            else:
                draw.point((i, j), 255)

    return image

def cutEdges(image):
    width = image.size[0]
    height = image.size[1]
    pixs = np.array(image.getdata()).reshape(height, width)
    arrayX = [index for index, item in enumerate(np.mean(pixs, axis=0)) if item < 255]
    arrayY = [index for index, item in enumerate(np.mean(pixs, axis=1)) if item < 255]
    X1, Y1 = (min(arrayX), min(arrayY))
    X2, Y2 = (max(arrayX), max(arrayY))
    image = image.crop((X1, Y1, X2 + 1, Y2 + 1))

    return image


def removeNoise(image):
    radius = 4
    width = image.size[0]+2
    height = image.size[1]+2

    newImage = Image.new("1", (width, height), 255)
    newImage.paste(image, (1,1))
    image = newImage
    pixs = image.load()
    draw = ImageDraw.Draw(image)

    for row in range(width):
        for col in range(height):
            if pixs[row, col] == 255:
                continue
            else:
                for r in reversed(range(1,radius)):
                    X1 = row - r if row - r >= 0 else 0
                    X2 = row + r if row + r < width else width - 1
                    Y1 = col - r if col - r >= 0 else 0
                    Y2 = col + r if col + r < height else height - 1
                    rectangle = (X1, Y1, X2+1, Y2+1)
                    one_piece = image.crop(rectangle)
                    if not checkBlackOnBoreder(one_piece):
                        draw.rectangle(rectangle, fill="white")
                        break
    return image

def removeNoiseOnBorder(image):
    offset = 11
    width = image.size[0]+2
    height = image.size[1]+2

    newImage = Image.new("1", (width, height), 255)
    newImage.paste(image, (1,1))
    image = newImage
    pixs = image.load()
    draw = ImageDraw.Draw(image)

    for r in reversed(range(1,offset)): # нижняя граница
        X1 = 0
        X2 = width - 1
        Y1 = height - r
        Y2 = height - 1
        rectangle = (X1, Y1, X2+1, Y2+1)
        one_piece = image.crop(rectangle)
        if not checkBlackOnBoreder(one_piece):
            draw.rectangle(rectangle, fill="white")
            break

    for r in reversed(range(1, offset)): # левая граница
        X1 = 0
        X2 = r
        Y1 = 0
        Y2 = height - 1
        rectangle = (X1, Y1, X2 + 1, Y2 + 1)
        one_piece = image.crop(rectangle)
        if not checkBlackOnBoreder(one_piece):
            draw.rectangle(rectangle, fill="white")
            break

    for r in reversed(range(1,offset)): # правая граница
        X1 = width - r
        X2 = width - 1
        Y1 = 0
        Y2 = height - 1
        rectangle = (X1, Y1, X2+1, Y2+1)
        one_piece = image.crop(rectangle)
        if not checkBlackOnBoreder(one_piece):
            draw.rectangle(rectangle, fill="white")
            break

    # for r in reversed(range(1,offset)): # верхняя граница закомментирован, т.к. может убрать часть буквы ц "й" и "ё"
    #     X1 = 0
    #     X2 = width - 1
    #     Y1 = 0
    #     Y2 = r
    #     rectangle = (X1, Y1, X2+1, Y2+1)
    #     one_piece = image.crop(rectangle)
    #     if not checkBlackOnBoreder(one_piece):
    #         draw.rectangle(rectangle, fill="white")
    #         break

    return image

def checkBlackOnBoreder(image):
    pixs = image.load()
    width = image.size[0]
    height = image.size[1]
    for row in range(width):
        if pixs[row,0] == 0:
            return True
    for row in range(width):
        if pixs[row, height-1] == 0:
            return True
    for col in range(height):
        if pixs[0, col] == 0:
            return True
    for col in range(height):
        if pixs[width-1, col] == 0:
            return True

    return False

def convertToBits(pixels):
    bits = np.zeros(len(pixels))
    for index, pixel in enumerate(pixels):
        if np.mean(pixel) > 220:
            bits[index] = 1
        else:
            bits[index] = 0
    # counter = collections.Counter(bits)
    # pp(counter)

    return bits
