from fastapi import FastAPI, UploadFile, Form, File, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from enums.rutas import Rutas
from pydantic import BaseModel
from util.util_images import *
import cv2
import os
import modelo
#import schedule
import asyncio

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

#model = modelo.cargar_modelo()
model = modelo.cargar_modelo_adi()

app.add_middleware(
    
    CORSMiddleware,
    allow_origins=["http://localhost:8500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/probar-modelo")
async def recibir_imagen(image: UploadFile):
    
    with open(image.filename, "wb") as file:
        file.write(image.file.read())
    img = cv2.imread(image.filename)

    dict_clases = modelo.peticiones(img, model)
    img = marcar_regiones(img,dict_clases)
    ruta = f'static/{image.filename}'
    
    cv2.imwrite(ruta,img)
    os.remove(image.filename)
    print(FileResponse(ruta))
    return image.filename

async def my_background_task():
    while True:
        print("Ejecutando tarea cada 10 segundos...")
        clean_static_folder()
        # Tu lógica aquí
        # Pausa de 5 segundos
        await asyncio.sleep(500)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(my_background_task())