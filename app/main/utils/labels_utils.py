from ..config import Settings

config = Settings()


def read_classes() -> list:
    classesfile = config.CLASSES_PATH
    with open(classesfile, 'rt') as f:  # Obtener las clases a predecir
        classes = f.read().rstrip('\n').split('\n')
    return classes


def create_dicts_from_labels() -> dict:
    classes = read_classes()
    dict = {}
    for keys in classes:
        dict[keys] = False
    return dict
