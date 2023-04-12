# ICNEA
[![codecov](https://codecov.io/gh/Juerodriguez/icnea/branch/master/graph/badge.svg?token=CS77QAL0ZB)](https://codecov.io/gh/Juerodriguez/icnea)

Icnea como todo proyecto de ML esta compuesto por dos etapas, una etapa de entrenamiento donde se construye el
modelo, y otra etapa de inferencia donde se pone a prueba el modelo

## Sistema de modelado, TRAINING UTILS

Para el entreamiento se eligio el algoritmo de YOLOv8, para el mismo se utilizará el repositorio de ultralitycs,
el cual se usara en opción dockerizada para evitar descargar las dependencias en nuestro entorno. Las intrucciones
del mismo se encuentran en: 

- https://github.com/Juerodriguez/icnea/tree/master/training_utils


## Sistema de inferencia, Servidor 

El sistema de inferencia fue desarrollada con FastApi devido a su grado de integracion con operacion asincronas y la facilidad de implementación de un API REST.

![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)



Para levantar el servidor el sistema esta automatizado para esto se necesita tener instalado Docker junto a sus dependencias para integrarlo con CUDA.

Para instalar las dependencias de CUDA para docker se debe ejecutar las instrucciones indicadas en training utils.


Una vez instalado las dependencias de Docker se puede ejecutar docker compose con el siguiente comando:

```
docker compose up
```

Para acceder a la documentación de los endpoints se debe acceder a la dirección:

- http://127.0.0.1/docs

![endpoints](https://user-images.githubusercontent.com/73370773/231500122-e8b7a4e4-e251-440a-9549-56a1e7ebf369.png)

## Sistema de Representacion de datos, Interfaz Web

La interfaz web es servida en con el servidor de inferencia mediante Jinja2 un motor de plantilla, para acceder se debe entrar en la dirección.

- "http://127.0.0.1/main"

