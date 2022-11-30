

def test():
    classes = "classes.txt"
    with open(classes, "rt") as f:
        classesfile = f.read().rstrip('\n').split('\n')
    print(classesfile)


if __name__ == "__main__":
    test()
