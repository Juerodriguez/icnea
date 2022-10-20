# ICNEA

1- Descomprimir el zip en el repositorio

2- Correr el script split_data.py


```bash
python3 split_data.py
```

Este script divide los datos de images y labels en datos para el train y validation con una proporcion de 80/20


3- Docker Containar

```bash
sudo docker pull ultralytics/yolov5:latest

```

En la misma ruta del repositorio crear el contenedor, debe ser aqui por el comando PWD que lo creara donde este posicionada la linea de comando.

```bash
sudo docker run --name icnea_yolov5 -it -v $PWD:/icnea --gpus all ultralytics/yolov5:latest

```

Mover el archivo data_tools.yaml al directorio de yolov5 dentro del contenedor en /usr/src/app/data

```bash
cd /icnea/
cp data_tools.yaml /usr/src/app/data/

```

Descargar el premodelo que vas a entrenar y moverlo a /usr/src/app/ ;Seleccionarlo desde https://github.com/ultralytics/yolov5#pretrained-checkpoints

```bash
python train.py --img 640 --batch 8 --epochs <cantidad de epochs ej:20> --data data/data_tools.yaml --weights <modelo a entrenar ej:yolov5m.pt> 

```

EXTRAS: MANEJANDO DOCKER

Para iniciar un contenedor creado

```bash
sudo docker start icnea_yolov5

```

Luego ejecutar el docker y usar bash dentro del mismo


```bash
sudo docker exec -it icnea_yolov5 bash

```




python train.py --img 640 --batch 8 --epochs 20 --data data/data_tools.yaml --weights yolov5m.pt 
