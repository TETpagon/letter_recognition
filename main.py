import numpy as np
from pprint import pprint as pp
import os
import prepareImage as prIm
from ImageLatter import ImageLatter
from matplotlib import pyplot as plt
import time
import pickle


path_to_image_letters = "../TRAIN"

dirs = sorted(os.listdir(path_to_image_letters))

sample = {}

for dir in dirs:
    # dir = "у"
    sample[dir] = []
    files = os.listdir(path_to_image_letters+"/"+dir)
    amountFiles = len(files)
    for index, file in enumerate(files):
        print("Номер элемента: " + str(index+1) + " из " + str(amountFiles))
        print("Директория \"" + dir + "\" файл " + file)
        start = time.time()
        path_to_image_letter = path_to_image_letters + "/" + dir + "/" + file
        # path_to_image_letter = "../TRAIN/у/28.jpg"
        sample[dir].append(prIm.prepare(path_to_image_letter))

        print("Время затраченное на обработку: " + str(time.time() - start))
        print()

        # break
    # break
    with open("../Data/" + dir + '.pickle', 'wb') as f:
        pickle.dump(sample[dir], f)

with open("../Data/" + 'allLetters.pickle', 'wb') as f:
    pickle.dump(sample, f)