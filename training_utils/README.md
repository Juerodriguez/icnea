# Entrenamiento

## Preparación de las imágenes ha etiquetar
Antes de realizar el entrenamiento, se debe conseguir las imagenes con los objetos que queremos detectar (por lo menos 500 imágenes por objeto). Luego, para poder hacer un etiquetado de forma mas comoda y legible, se recomienda ejecutar el script "rename_images.py" para renombrar las imagenes y obtener nombres cortos con nombre. Para esto se debe copiar y pegar el script mencionado a la altura del directorio que ocntiene las imagenes y luego ejecutarlo:

```bash
python3 rename_images.py
```

## Preparación del dataset
Luego de realizar el correspondiente etiquetado de las imagenes y luego de exportar el .zip para YOLO:

1- Descomprimir el .zip en el repositorio u otra carpeta determinada

2- copiar el script "split_data.py" en la carpeta descomprimida

3- Correr el script split_data.py:

```bash
python3 split_data.py
```
Este script divide los datos de images y labels en datos para el train y validation con una proporcion de 80/20

3- Descargar la imagen de yolo-v5 para Docker:

```bash
sudo docker pull ultralytics/yolov5:v6.2 
```

4- En la misma ruta del repositorio o directorio con los datos, crear el contenedor. Debe ser aqui por el comando PWD que lo creara donde este posicionada la linea de comando:

```bash
sudo docker run --name icnea_yolov5 -it -v $PWD:/icnea --gpus all --shm-size=8gb ultralytics/yolov5:v6.2
```
Gracias al comando "-v" se comparte el directorio con las etiquetas, con el contenedor de yolo-v5

5- Mover el archivo data_tools.yaml al directorio de yolov5 dentro del contenedor en /usr/src/app/data
```bash
cd /icnea/
cp data_tools.yaml /usr/src/app/data/
```

6- Descargar el premodelo que vas a entrenar desde https://github.com/ultralytics/yolov5#pretrained-checkpoints y luego colocarlo en la carpeta compartida con el contenedor docker creado.

7- Mover el .pt descargado a la carpeta /usr/src/app/
```bash
cp <modelo a entrenar ej:yolov5m.pt> /usr/src/app/
```

8- Para iniciar el entrenamiento se usa el siguiente comando que tiene un batch de 8. Primero nos movemos a la carpeta donde está el .pt
```bash
cd /usr/src/app/
```
Luego ejecutamos el los siguientes comandos:
```bash
export CLEAR_OFFLINE_MODE=1
python train.py --img 640 --batch 8 --epochs <cantidad de epochs ej:20> --data data/data_tools.yaml --weights <modelo a entrenar ej:yolov5m.pt> 
```

9- Luego de entrenarlo Validarlo
```bash
python val.py --weights runs/train/<n° de experimento>/weights/best.pt --data data/data_tools.yaml --batch 8 --img 640 --half

```

10- Por ultimo, cuando tengamos nuestro mejor modelo entrenado lo transformaremos en el formato ONNX para asi poder utilizarlo en la inferencia.
Esto lo haremos con el script export.py

```bash
python export.py --weights runs/<nombre del experimento>/weights/best.pt --include onnx --opset 12
```

## Manejando docker

Para iniciar un contenedor creado
```bash
sudo docker start icnea_yolov5

```

Luego ejecutar el docker y usar bash dentro del mismo
```bash
sudo docker exec -it icnea_yolov5 bash

```

## Ejemplos de experimentos con distintos optimizadores

Para lograr una comparación entre los distintos optimizadores ejecutar:

Optimizador SGD (por defecto)
```
python train.py --img 640 --batch 8 --epochs 80 --data data/data_tools.yaml --weights yolov5m.pt --cache disk
```

Optimizador Adam
```
python train.py --img 640 --batch 8 --epochs 80 --optimizer Adam --data data/data_tools.yaml --weights yolov5m.pt --cache disk
```

Optimizador AdamW
```
python train.py --img 640 --batch 8 --epochs 80 --optimizer AdamW --data data/data_tools.yaml --weights yolov5m.pt --cache disk
```
