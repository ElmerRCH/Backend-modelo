import torch
import pandas as pd
from util.util_images import aplicar_tratamiento

def cargar_modelo(ruta_yolo='./yolov5', ruta_modelo='./yolov5/runs/train/yolov5s_results/weights/best.pt'):
    modelo = torch.hub.load(ruta_yolo, 'custom', ruta_modelo, source='local')  # local repo
    return modelo

def cargar_modelo_adi(ruta_yolo='./yolov5', ruta_modelo='./yolov5/runs/train/yolov5s_results/weights/best_adicionales.pt'):
    modelo_adi = torch.hub.load(ruta_yolo, 'custom', ruta_modelo, source='local')  # local repo
    return modelo_adi

def peticiones(img, modelo):
    
    results = None
    img_org = img
    img = aplicar_tratamiento(img)
    
    results = modelo(img) # PyTorch 2.0.1

    df_results = results.pandas().xyxy[0]
    df_results = df_results[df_results['confidence'] >= 0.7]

    w_org = img_org.shape[1]
    h_org = img_org.shape[0]

    df_results_t = pd.DataFrame()

    for index, row in df_results.iterrows():
        x_org = (row['xmin'] * w_org) / 640 # 640 x 640 tamaño del acta en YOLO
        y_org = (row['ymin'] * h_org) / 640
        w_new = ((row['xmax'] - row['xmin']) * w_org) / 640
        h_new = ((row['ymax'] - row['ymin']) * h_org) / 640

        df_results_t.at[index, 'name'] = row['name']
        df_results_t.at[index, 'xmin'] = x_org
        df_results_t.at[index, 'ymin'] = y_org
        df_results_t.at[index, 'xmax'] = w_new + df_results_t.at[index, 'xmin']
        df_results_t.at[index, 'ymax'] = h_new + df_results_t.at[index, 'ymin']

    dict_clases = {}

    for index, row in df_results_t.iterrows():

        class_name = row['name']
        dimensions = (row['xmin'], row['ymin'], row['xmax'], row['ymax'])

        if class_name not in dict_clases:
            dict_clases[class_name] = []
        dict_clases[class_name].append(dimensions)
    return dict_clases


def valida_acta(imagen, modelo):
    return len(peticiones(imagen, modelo)) >= 2
