

def presence(data):

    clases_count = {
        "Coping saw": 0,
        "Drill": 0,
        "Hammer": 0,
        "Pliers": 0,
        "Scissors": 0,
        "Screwdriver": 0,
        "Spanner": 0,

    }
    clases_response = {
        "Coping saw": False,
        "Drill": False,
        "Hammer": False,
        "Pliers": False,
        "Scissors": False,
        "Screwdriver": False,
        "Spanner": False,

    }

    for dicts in data:
        if "frame" in dicts:
            frames = dicts["frame"]
            for frame in frames:
                clases_count[frame["label"]] += 1
    for dicts in data:
        if "frames_count" in dicts:
            for key in clases_count.keys():
                if clases_count[key] >= int(dicts["frames_count"] / 2):
                    clases_response[key] = True
    return clases_response
