# ICNEA

1- Descomprimir el zip en el repositorio

2- Correr el script split_data.py


```bash
python3 split_data.py
```

Este script divide los datos de images y labels en datos para el train y validation con una proporcion de 80/20


3- Docker Container

```bash
sudo docker pull ultralytics/yolov5:v6.2 

```

En la misma ruta del repositorio crear el contenedor, debe ser aqui por el comando PWD que lo creara donde este posicionada la linea de comando.

```bash
sudo docker run --name icnea_yolov5 -it -v $PWD:/icnea --gpus all --shm-size=8gb ultralytics/yolov5:v6.2

```

Mover el archivo data_tools.yaml al directorio de yolov5 dentro del contenedor en /usr/src/app/data

```bash
cd /icnea/
cp data_tools.yaml /usr/src/app/data/

```

Descargar el premodelo que vas a entrenar y moverlo a /usr/src/app/
Seleccionarlo desde https://github.com/ultralytics/yolov5#pretrained-checkpoints
Mover el .pt descargado a la carpeta /usr/src/app/

```
cp <modelo a entrenar ej:yolov5m.pt> /usr/src/app/
```

Para iniciar el entrenamiento se usa el siguiente comando que tiene un batch de 8. Primero nos movemos a la carpeta donde está el .pt
```
cd /usr/src/app/
```
Luego ejecutamos el los siguientes comandos:
```bash
export CLEAR_OFFLINE_MODE=1
python train.py --img 640 --batch 8 --epochs <cantidad de epochs ej:20> --data data/data_tools.yaml --weights <modelo a entrenar ej:yolov5m.pt> 

```

Luego de entrenarlo Validarlo

```bash
python val.py --weights runs/train/<n° de experimento>/weights/best.pt --data data/data_tools.yaml --batch 8 --img 640 --half

```
Por ultimo, cuando tengamos nuestro mejor modelo entrenado lo transformaremos en el formato ONNX para asi poder utilizarlo en la inferencia.
Esto lo haremos con el script export.py

```bash
python export.py --weights runs/<n° de experimento>/weights/best.pt --include onnx
```

## EXTRAS: MANEJANDO DOCKER

Para iniciar un contenedor creado

```bash
sudo docker start icnea_yolov5

```

Luego ejecutar el docker y usar bash dentro del mismo


```bash
sudo docker exec -it icnea_yolov5 bash

```

## EXPERIMENTOS CON OPTIMIZADORES

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


