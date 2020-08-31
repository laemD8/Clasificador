import cv2
from imageShape import *

if __name__ == '__main__':
    #Solicitar dimensiones de imagen
    height = int(input('Por favor ingrese el alto de la imagen: '))
    width = int(input('Por favor ingrese el ancho de la imagen: '))
    image = imageShape(height, width)
    #Generación figura aleatoria
    image.generateShape()
    #Visualización figura por 5 segundos
    image.showShape()
    #Obtención nombre y figura
    name, shape = image.getShape()
    #Clasificación imagen
    N=image.whatShape(shape)
    print(N)

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
