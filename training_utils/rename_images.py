import os

cwd = os.getcwd()

print("ATENCIÓN: Asegúrese de que este script está ubicado a la altura del directorio con las imágenes, no adentro del mismo.")
print("Ingrese el nombre del directorio con imágenes a renombrar...")

collection = input()

directories = os.listdir(cwd)

if type(collection) == str:
    if collection in directories:
        for i, filename in enumerate(os.listdir(collection)):
            os.rename(cwd + "/" + collection + "/" + filename, cwd + "/" + collection + "/img" + str(i) + ".jpg")
        print("El nombre de las imágenes en el directorio << " + collection + " >> ha sido renombrado con éxito...")
    else:
        print("Directorio no encontrado")
else:
    print("Nombre corrompido")