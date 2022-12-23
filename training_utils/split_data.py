import os
import shutil
import random


def create_dirs(directories):
    """ Esta funcion permite crear los directorios necesarios para el entrenamiento de los datos
    
    return: 
         - La ruta absoluta del nuevo directorio creado de train images
         - La ruta absoluta del nuevo directorio creado de train labels
         - La ruta absoluta del directorio donde se encuentran las imagenes
         - La ruta absoluta del directorio donde se encuentran las etiquetas
    
    """
    absolute_path = os.getcwd()
    directory_images_train_relative = "data/images/train"
    directory_images_val_relative = "data/images/val"
    directory_label_train_relative = "data/labels/train"
    directory_label_val_relative = "data/labels/val"
    directories["path_images"] = os.path.join(absolute_path, "images")
    directories["path_labels"] = os.path.join(absolute_path, "labels")
    
    directories["train_directories"]["images"] = os.path.join(absolute_path, directory_images_train_relative)
    directories["validate_directories"]["images"] = os.path.join(absolute_path, directory_images_val_relative)
    directories["train_directories"]["labels"] = os.path.join(absolute_path, directory_label_train_relative)
    directories["validate_directories"]["labels"] = os.path.join(absolute_path, directory_label_val_relative)

    os.makedirs(directories["train_directories"]["images"], exist_ok=True)
    os.makedirs(directories["validate_directories"]["images"], exist_ok=True)
    os.makedirs(directories["train_directories"]["labels"], exist_ok=True)
    os.makedirs(directories["validate_directories"]["labels"], exist_ok=True)
    
    return directories
    

def split_data(directories):
    """ Con esta funcion movemos los archivos desde el directorio de las imagenes y etiquetas descomprimidas, dividiendo
    	en datos de entrenamiento y datos de validacion de acuerdo a la proporcion 80/20, train/val
    
    return: 
         
    
    """
    list_data = []
    list_data = os.listdir(directories["path_images"])
    for i in range(int(len(list_data)*0.8)):
        train_data = random.choice(list_data)
        list_data.pop(list_data.index(train_data))

        path_image_single = os.path.join(directories["path_images"], train_data)
        path_image_single_jpg = os.path.join(directories["train_directories"]["images"], train_data)
        train_data_txt = train_data.replace("jpg", "txt")
        path_label_single = os.path.join(directories["path_labels"], train_data_txt)
        path_label_single_txt = os.path.join(directories["train_directories"]["labels"], train_data_txt)

        shutil.move(path_image_single, path_image_single_jpg)
        shutil.move(path_label_single, path_label_single_txt)
    
    for val_data in list_data:
        path_images_single = os.path.join(directories["path_images"], val_data)
        path_images_single_jpg = os.path.join(directories["validate_directories"]["images"], val_data)
        val_data_txt = val_data.replace("jpg", "txt")
        path_labels_single = os.path.join(directories["path_labels"], val_data_txt)
        path_labels_single_txt = os.path.join(directories["validate_directories"]["labels"], val_data_txt)

        shutil.move(path_images_single, path_images_single_jpg)
        shutil.move(path_labels_single, path_labels_single_txt)
        
    os.rmdir(directories["path_images"])
    os.rmdir(directories["path_labels"])


if __name__ == '__main__':

    directories = {"train_directories": {"images": "", "labels": ""},
                   "validate_directories": {"images": "", "labels": ""},
                   "path_images": "",
                   "path_labels": "",
                  }
               
    split_data(create_dirs(directories))



