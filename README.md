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


EXTRAS: MANEJANDO DOCKER

Para iniciar un contenedor creado

```bash
sudo docker start icnea_yolov5

```

Luego ejecutar el docker y usar bash dentro del mismo


```bash
sudo docker excec -it icnea_yolov5 bash

```
