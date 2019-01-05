import pickle
from pprint import pprint as pp
import numpy as np
from PIL import Image, ImageDraw


with open("../Data/" + 'allLetters.pickle', 'rb') as f:
    sample = pickle.load(f)

for key in sample:
    arrayColors = sample[key]

    arrayColors = np.array(arrayColors)

    A = list(np.mean(arrayColors,axis=0))

    # A = [0 if color < 128 else 255 for color in A ]
    A = [0 if color < 172 else color for color in A ]

    image = Image.new("L", (32,32), 255)
    draw = ImageDraw.Draw(image)

    for i in range(32):
        for j in range(32):
            draw.point((j,i), fill=int(A.pop(0)))

    image.show()




