# ICNEA

Icnea como todo proyecto de ML esta compuesto por dos etapas, una etapa de entrenamiento donde se construye el
modelo, y otra etapa de inferencia donde se pone a prueba el modelo

## TRAINING UTILS

Para el entreamiento se eligio el algoritmo de YOLOv5, para el mismo se utilizara el repositorio de ultralitycs,
el cual se usara en opcion dockerizada para evitar descargar las dependencias en nuestro entorno. Las intrucciones
del mismo se encuentran en:


## INFERENCE APLICATION

La aplicacion de inferencia fue desarrollada con FastApi devido a su grado de integracion con operacion asincronas.

Python 3.10

Instalar los requerimientos
```
pip install -r requirements.txt
```

Correr el programa
```
uvicorn run:app --reload
```

Optimizador AdamW
```
python train.py --img 640 --batch 8 --epochs 80 --optimizer AdamW --data data/data_tools.yaml --weights yolov5m.pt --cache disk
```


