from ..utils import labels_utils


def presence(data) -> dict:

    classes_count: dict = labels_utils.create_dicts_from_labels()
    classes_response: dict = labels_utils.create_dicts_from_labels()

    for dicts in data:
        if "frame" in dicts:
            frames = dicts["frame"]
            for frame in frames:
                classes_count[frame["label"]] += 1
    for dicts in data:
        if "frames_count" in dicts:
            for key in classes_count.keys():
                if classes_count[key] >= int(dicts["frames_count"] / 2):
                    classes_response[key] = True
    return classes_response
