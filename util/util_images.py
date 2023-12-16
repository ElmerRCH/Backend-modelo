import cv2
import numpy as np
import os
import glob

def recorte_centro_manual(image):
    ancho = image.shape[1]
    x1 = ancho // 3
    x2 = (ancho // 3) * 2
    return image[0:image.shape[0], x1:x2]



def marcar_votos(centro, x1, y1, x2, y2, color, copia_centro):
    opacidad = 0.5
    cv2.rectangle(centro, (x1, y1), (x2, y2), color, -1)
    votos_marcados = cv2.addWeighted(copia_centro, 1 - opacidad, centro, opacidad, 0)

    return votos_marcados


def valida_coordenadas(x1, x2, y1, y2):
    return (x1 + y1 + x2 + y2) != 0


def leer_qr(qr):
    detect = cv2.QRCodeDetector()
    valor_qr, _, _ = detect.detectAndDecode(qr)

    return valor_qr if valor_qr else None


def peticiones_template(ruta_template, imagen, umbral=0.8):
    template = []
    try:
        template = carga_imagen(ruta_template)
        template_gray = aplicar_escala_grises(template)
        image_gray = aplicar_escala_grises(imagen)
        res = cv2.matchTemplate(image_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        return template, np.where(res >= umbral)
    except Exception:
        return template, []


def carga_imagen(ruta):
    return cv2.imread(ruta)


def aplicar_escala_grises(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def aplicar_tratamiento(img, re_size=(640, 640)):
    img = aplicar_escala_grises(img)
    img = cv2.GaussianBlur(img, (5, 5), cv2.BORDER_DEFAULT)
    img = cv2.resize(img, re_size)
    return img

def obten_puntos_rectangulo(clase, dict_clases):
    x1, y1, x2, y2 = 0, 0, 0, 0
    
    if clase in dict_clases:
        x1 = round(dict_clases[clase][0][0])
        y1 = round(dict_clases[clase][0][1])
        x2 = round(dict_clases[clase][0][2])
        y2 = round(dict_clases[clase][0][3])
    
    return x1, y1, x2, y2

def marcar_regiones(img,dict_clases):

    for i in dict_clases:
        x1, y1, x2, y2 = obten_puntos_rectangulo(i, dict_clases)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
        print('x1, y1, x2, y2',x1, y1, x2, y2)
    return img


def clean_static_folder():
    print('Borrando.......')
    static_folder = 'static'
    image_extensions = ['jpg', 'png', 'jpeg']

    files_to_delete = []
    for ext in image_extensions:
        files_to_delete.extend(glob.glob(os.path.join(static_folder, f'*.{ext}')))

    for file_path in files_to_delete:
        try:
            os.remove(file_path)
            print(f'Archivo eliminado: {file_path}')
        except Exception as e:
            print(f'Error al eliminar archivo {file_path}: {e}')

def hola_mundo():
    print('ola..........')