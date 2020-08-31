import cv2
import math
import random
import numpy as np
import os

class imageShape:

    #Constructor recibe parámetro de imagen
    def __init__(self, height, width):
        self.height=height
        self.width=width

    #Método creación y almacenamiento de imagen
    def generateShape (self):
        #Creación fondo negro
        image = np.zeros((self.height, self.width, 3), np.uint8)
        #Generación número aleatorio
        num = random.randrange(4)
        self.shape = image.copy()

        #Triangulo
        if num==0:
            #Determinación centroide de la figura
            Cx = int(self.width / 2)
            Cy = int(self.height / 2)
            #Cálculo lado
            side = min(self.width, self.height) / 2
            #Cálculo altura
            l = math.sqrt(side ** 2 - (side / 2) ** 2)
            #Generación puntos
            pt1 = (Cx, int(Cy - ((2 * l) / 3)))
            pt2 = (int(Cx + (side / 2)), int(Cy + (l / 3)))
            pt3 = (int(Cx - (side / 2)), int(Cy + (l / 3)))
            #Concatenación puntos
            triangle_cnt = np.array([pt1, pt2, pt3])
            #Creación contorno de la figura
            self.shape = cv2.drawContours(image, [triangle_cnt], 0, (255, 255, 0), -1)
            self.name = 'triangle'
            #cv2.imshow("image", self.shape)
            #cv2.waitKey()

        #Cuadrado
        if num==1:
            # Determinación centroide de la figura
            Cx = int(self.width / 2)
            Cy = int(self.height / 2)
            #Cálculo lado
            side = min(self.width, self.height) / 2
            #Generación puntos
            pt1 = (int(Cx - (side / 2)), int(Cy + (side / 2)))
            #pt2 = (int(Cx + (side / 2)), int(Cy + (side / 2)))
            #pt3 = (int(Cx - (side / 2)), int(Cy - (side / 2)))
            pt4 = (int(Cx + (side / 2)), int(Cy - (side / 2)))
            #Creación contorno del cuadrado
            image = cv2.rectangle(image, pt1, pt4, (255, 255, 0), -1)
            #Rotación de la figura
            rotation=  cv2.getRotationMatrix2D((Cx, Cy), 45, 1)
            #Transformación imagen fuente con matriz específica
            self.shape =  cv2.warpAffine(image, rotation, (self.width, self.height))
            self.name = 'square'
            #cv2.imshow("image", self.shape)
            #cv2.waitKey()

        # Rectangulo
        if num==2:
            #Determinación centroide de la figura
            Cx = int(self.width / 2)
            Cy = int(self.height / 2)
            #Cálculo lado horizontal
            sideX = int(self.width / 2)
            #Cálculo lado vertical
            sideY = int(self.height / 2)
            #Generación puntos
            pt1 = (int(Cx - (sideX / 2)), int(Cy + (sideY / 2)))
            pt4 = (int(Cx + (sideX / 2)), int(Cy - (sideY / 2)))
            #Creación contorno del rectangulo
            self.shape= cv2.rectangle(image, pt1, pt4, (255, 255, 0), -1)
            self.name = 'rectangle'
            #cv2.imshow("image", self.shape)
            #cv2.waitKey()

        #Circulo
        if num==3:
            #Determinación centroide de la figura
            Cx = int(self.width / 2)
            Cy = int(self.height / 2)
            #Cálculo radio
            radius = int(min(self.width, self.height) / 4)
            #Creación contorno del circulo
            self.shape=cv2.circle(image, (Cx, Cy), radius, (255, 255, 0), -1)
            self.name = 'circle'
            #cv2.imshow("image", image)
            #cv2.waitKey()

    #Método visualización
    def showShape (self):
        #Comprobación existencia del atributo dentro del objeto
        # Caso en el que exista una imagen disponible
        if hasattr(self, 'shape')==True:
            cv2.imshow("image", self.shape)
            #Visualización figura durante 5 segundos
            cv2.waitKey(5000)
        #Caso contrario
        else:
            #Generación fondo negro
            self.shape= np.zeros((self.height, self.width, 3), np.uint8)
            #self.name= 'none'
            cv2.imshow("image", self.shape)
            cv2.waitKey()

    #Método retorna nombre e imagen generada
    def getShape (self):
        self.name
        self.shape
        return self.name, self.shape

    #Método clasificación de figuras
    def whatShape(self, imagen):
        #Conversión imagen a escala de grises
        image_gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        #Umbralización intensidad de pixeles
        ret, ibw_shapes = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        #Determinación contornos
        contours, hierarchy = cv2.findContours(ibw_shapes, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for idx, i in enumerate(contours):
            if idx == 0:
                #Cálculo perimetro de contorno
                perimeter = cv2.arcLength(contours[0], True)
                #Apróximación valor epsilon
                epsilon = 0.04 * perimeter
                #Cálculo momento del poligono
                approx = cv2.approxPolyDP(contours[0], epsilon, True)
                #Dibujo contorno
                cv2.drawContours(imagen, [approx], 0, (0, 0, 255), 3)
                #Visaluzación imagen con contornos de prueba
                #cv2.imshow("Prueba", imagen)
                #cv2.waitKey(5000)
                #Evaluar número de vertices según la aproximación resultante
                if len(approx) == 3:
                    #Al tener tres vertices se reconoce como un triangulo
                    return "Triangle"
                elif len(approx) == 4:
                    #Al tener cuatro vertices podría ser un cuadrado o rectangulo
                    #Dibujar una aproximación rectangular al rededor de una imagen binaria
                    (x, y, w, h) = cv2.boundingRect(approx)
                    #División entre el ancho y largo de la aproximación
                    ar = w / float(h)
                    #Determinación intervalo argumento típico de un cuadrado
                    if (ar > 0.95) and (ar < 1.05):
                        return "Square"
                    else:
                    #Caso referente a un valor de argumento distinto
                        return "Rectangle"
                #Caso referente al número vertices distinto
                else:
                    return "Circle"