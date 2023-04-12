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

4- Preparar Docker para integrar la tarjeta grafica al contenedor y asi entrenar con la misma.

```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
      && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
      && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
            sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
            sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```
```bash
sudo apt update

```

```bash
sudo apt install -y nvidia-docker2

```

```bash
sudo systemctl restart docker

```


5- Descargar la imagen de yolo-v8 para Docker:

```bash
sudo docker pull ultralytics/ultralytics:latest 
```

6- En la misma ruta del repositorio o directorio con los datos, crear el contenedor. Debe ser aqui por el comando PWD que lo creara donde este posicionada la linea de comando:

```bash
sudo docker run --name YOLOV8 -it -v $PWD:/shared_directory --gpus all --shm-size=8gb ultralytics/ultralytics:latest
```
Gracias al comando "-v" se comparte el directorio con las etiquetas, con el contenedor de yolo-v8

7- Entrar en la carpeta compartida "/shared_directory" que se encuentra en la raíz del contenedor 
```bash
cd /shared_directory/
```

8- Descargar el premodelo que vas a entrenar desde "https://github.com/ultralytics/ultralytics" o en su defecto "https://github.com/ultralytics/assets/releases"; y luego colocarlo en la carpeta compartida con el contenedor docker creado (docker_yolov8). Links a la descarga directa de los modelos:
"m": https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8m.pt
"s": https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s.pt

9- Para iniciar el entrenamiento se usa el siguiente comando:
```bash
yolo detect train model=yolov8s.pt data=data_tools.yaml batch=48 v5loader=True device=\'0,1\' epochs=150
```

10- Luego de entrenarlo se debe verificar su correcta dectección con los datos de testeo:
```bash
yolo predict task=detect model=/icnea/best40.onnx imgsz=640 source=/icnea/video_tools_all.mp4 save=True

```
NOTA: el video_tools_all.mp4 debe ser añadido a la carpeta compartida con el contenedor de YOLOV8.

10- Por ultimo, cuando tengamos nuestro mejor modelo entrenado lo transformaremos en el formato ONNX para asi poder utilizarlo en la inferencia:
```bash
yolo export model=/icnea/train<n° de train>/weights/best.pt format=onnx opset=12
```

## Manejando docker

Para iniciar un contenedor creado
```bash
sudo docker start YOLOV8

```

Luego ejecutar el docker y usar bash dentro del mismo
```bash
sudo docker exec -it YOLOV8 bash

```
