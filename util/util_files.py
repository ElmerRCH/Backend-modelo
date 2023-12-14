import os
import hashlib
import shutil
from enums.parametro import Parametro


def eliminar_imagen(ruta_imagen):
    if os.path.exists(ruta_imagen):
        os.remove(ruta_imagen)
    return False


def genera_hash(ruta):
    sha256_hash = hashlib.sha256()
    with open(ruta, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def crear_directorio(folder_path=Parametro.DEFAULT_PATH_SAVE_IMAGES.value, delete_exists=False):
    if folder_path is None:
        return False

    if os.path.exists(folder_path):
        if delete_exists:
            shutil.rmtree(folder_path, ignore_errors=True)
        else:
            return False
    os.makedirs(folder_path)

    return True


def move_file(path: str, new_path: str):
    return shutil.move(path, new_path)


def copy_file(path: str, copy_path: str):
    return shutil.copy(path, copy_path)


def obtener_rutas(ruta: str):
    rutas_archivos = []
    if not os.path.exists(ruta):
        print(f'El directorio {ruta} no existe')
        return rutas_archivos

    lista_archivos = os.listdir(ruta)
    for nombre_archivo in lista_archivos:
        ruta_archivo = os.path.join(ruta, nombre_archivo)
        if os.path.isfile(ruta_archivo):
            if nombre_archivo.endswith(Parametro.EXTENSIONES_PERMITIDAS.value):
                rutas_archivos.append(ruta_archivo)

    return rutas_archivos


def rename_file(filename: str, new_filename: str):
    os.rename(filename, new_filename)
    return new_filename
