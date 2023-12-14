from enum import Enum

class Rutas(Enum):
    EXTENSIONES_PERMITIDAS = ('jpg', 'png', 'jpeg')
    TYPE_EXTENSION = EXTENSIONES_PERMITIDAS[0]
    DEFAULT_PATH_MOUNT = 'imagenes'
    
    