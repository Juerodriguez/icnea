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
**NOTA:** si por alguna razón el entrenamiento es detenido, con el comando `python train.py --resume` se puede reanudar fácilmente. No debe pasarse nigún otro parámetro, ya que automáticamenete reanuda el entrenamiento desde last.pt. Si se deséa especificar un last.pt en específico añadir `runs/exp0/weights/last.pt` luego del anterior comando.


9- Luego de entrenarlo Validarlo
```bash
python val.py --weights runs/train/<n° de experimento>/weights/best.pt --data data/data_tools.yaml --batch 8 --img 640 --half

```

10- Por ultimo, cuando tengamos nuestro mejor modelo entrenado lo transformaremos en el formato ONNX para asi poder utilizarlo en la inferencia.
Esto lo haremos con el script export.py

```bash
python export.py --weights runs/<nombre del experimento>/weights/best.pt --include onnx --opset 12 --batch-size 8
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

## Entrenamientos y rendimientos

1. Primer entrenamiento:
```
python train.py --img 640 --batch 8 --epochs 20 --data data/data_tools.yaml --weights yolov5s.pt

```
Resultado:
```
20 epochs completed in 1.609 hours.
Optimizer stripped from runs/train/exp/weights/last.pt, 14.4MB
Optimizer stripped from runs/train/exp/weights/best.pt, 14.4MB

Validating runs/train/exp/weights/best.pt...
Fusing layers... 
Model summary: 157 layers, 7034398 parameters, 0 gradients, 15.8 GFLOPs
                 Class     Images  Instances          P          R      mAP50   mAP50-95: 100%|██████████| 59/59 [00:23<00:00,  2.49it/s]
                   all        935       1551      0.217      0.258      0.201     0.0962
                   Box        935        209      0.383      0.392       0.33      0.194
            Coping saw        935        102     0.0467     0.0196     0.0341     0.0164
                 Drill        935        129     0.0676     0.0543     0.0503     0.0266
                Hammer        935        121       0.15      0.149     0.0531     0.0235
                Pliers        935        193      0.179      0.135      0.127      0.056
              Scissors        935        141      0.239      0.539      0.371      0.185
           Screwdriver        935        340      0.246      0.356      0.197     0.0831
               Spanner        935        112      0.106     0.0536     0.0638     0.0286
                Worker        935        204      0.534      0.623       0.58      0.253
Results saved to runs/train/exp
```

2. Segundo entrenamiento:
```
python train.py --img 640 --batch 8 --epochs 40 --data data/data_tools.yaml --weights yolov5s.pt
```
Resultado:
```
40 epochs completed in 3.249 hours.
Optimizer stripped from runs/train/exp2/weights/last.pt, 14.4MB
Optimizer stripped from runs/train/exp2/weights/best.pt, 14.4MB

Validating runs/train/exp2/weights/best.pt...
Fusing layers... 
Model summary: 157 layers, 7034398 parameters, 0 gradients, 15.8 GFLOPs
                 Class     Images  Instances          P          R      mAP50   mAP50-95: 100%|██████████| 59/59 [00:23<00:00,  2.49it/s]
                   all        935       1551      0.217      0.258      0.201     0.0962
                   Box        935        209      0.383      0.392       0.33      0.194
            Coping saw        935        102     0.0467     0.0196     0.0341     0.0164
                 Drill        935        129     0.0676     0.0543     0.0503     0.0266
                Hammer        935        121       0.15      0.149     0.0531     0.0235
                Pliers        935        193      0.179      0.135      0.127      0.056
              Scissors        935        141      0.239      0.539      0.371      0.185
           Screwdriver        935        340      0.246      0.356      0.197     0.0831
               Spanner        935        112      0.106     0.0536     0.0638     0.0286
                Worker        935        204      0.534      0.623       0.58      0.253
Results saved to runs/train/exp2
```

3. Tercer entrenamiento YOLO V8:
```
yolo detect train data=coco128.yaml model=yolov8n.pt epochs=100 imgsz=640
```
Resultado:
```

```

