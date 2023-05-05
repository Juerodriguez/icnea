# ICNEA
[![codecov](https://codecov.io/gh/Juerodriguez/icnea/branch/master/graph/badge.svg?token=CS77QAL0ZB)](https://codecov.io/gh/Juerodriguez/icnea)

Icnea es un proyecto desarrollado para alcanzar la titulación en Ingenieria Mecatronica en la Universidad Nacional de La Rioja, consiste en la deteccion de herramientas en un tablero utilizado como maqueta de un entorno laboral, en el se debe detectar presencia de las herramientas y su correcto ordenamiento en la misma. Las herramientas a detectar son: 

- Drill/Taladro.
- Spanner/Llave.
- Screwdriver/Destornillador.
- Plier/Pinza.
- Hammer/Martillo.
- Box/Caja.

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

![Panel_control](https://user-images.githubusercontent.com/73370773/236558888-c7ac7ff4-0c97-4230-8d07-943d7357f9a1.png)


## Contacto de los autores

Si quieres contribuir, aprender o tienes alguna idea para desarrollar y tienes alguna duda puedes contactarnos a los siguientes correos:

- rodriguezjuanelias19@gmail.com
- gramajogonzalo@gmail.com

