from ImageLatter import ImageLatter
import os

class RepositoryImage:

    def __init__(self):
        self.__pathToLettors = "../TRAIN"
        self.ALLOWED_LETTERS = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п',
                                'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']


    def addImage(self, image: ImageLatter):
        pass

    def getImages(self, filter):
        if filter['letters']:
            arrayImages = self.getImage()
        pass

    def getImage(self, filter):
        pass

