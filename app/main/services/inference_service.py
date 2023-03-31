import cv2
import numpy as np
from typing import List

from ..config import Settings
from ..schemas.prediction_schema import Frame, Coordinate, Prediction
from ..schemas.timer_schema import Timer
from ..services.redis_client_service import save_cache, delete_all_cache
from ..utils.timer_utils import start_timer, finish_timer

settings = Settings()


def draw_label(im, label, x, y):
    """
    Draw text onto image at location.

    :param im:
    :param label:
    :param x:
    :param y:
    :return:
    """
    # Get text size.
    text_size = cv2.getTextSize(label,
                                settings.OPENCVCONFIG.TEXT_PARAMETERS.FONT_FACE,
                                settings.OPENCVCONFIG.TEXT_PARAMETERS.FONT_SCALE,
                                settings.OPENCVCONFIG.TEXT_PARAMETERS.THICKNESS)
    dim, baseline = text_size[0], text_size[1]
    # Use text size to create a BLACK rectangle.
    cv2.rectangle(im, (x, y), (x + dim[0], y + dim[1] + baseline), (0, 0, 0), cv2.FILLED)
    # Display text inside the rectangle.
    cv2.putText(im, label, (x, y + dim[1]),
                settings.OPENCVCONFIG.TEXT_PARAMETERS.FONT_FACE,
                settings.OPENCVCONFIG.TEXT_PARAMETERS.FONT_SCALE,
                settings.OPENCVCONFIG.COLORS.YELLOW,
                settings.OPENCVCONFIG.TEXT_PARAMETERS.THICKNESS,
                cv2.LINE_AA)


def pre_process(input_image, net):
    """
    This function run the inference in the image with the models.

    :param input_image:
    :param net:
    :return: output raw predictions
    """
    # Create a 4D blob from a frame.

    input_image = cv2.resize(input_image, (640, 640))
    blob = cv2.dnn.blobFromImage(input_image, 1 / 255,
                                 (settings.OPENCVCONFIG.CONSTANTS.INPUT_WIDTH,
                                  settings.OPENCVCONFIG.CONSTANTS.INPUT_HEIGHT),
                                 [0, 0, 0], 1, crop=False)

    # Sets the input to the network.
    net.setInput(blob)

    # Run the forward pass to get output of the output layers.
    outputs = net.forward()
    return outputs


def post_process(input_image, outputs, classes: List[str], timer: Timer, frames_to_redis):
    """
    This function post process the predictions, it discards redundant and bad detections,
     then draw the boxes and labels, finally, at last save results in cache.

    :param timer:
    :param input_image:
    :param outputs:
    :param classes:
    :return:
    """
    # Lists to hold respective values while unwrapping.
    class_ids = []
    boxes = []
    scores = []
    input_image = cv2.resize(input_image, (640, 640))
    [height, width, _] = input_image.shape
    length = max((height, width))
    scale = length / 640
    # Rows.
    outputs = np.array([cv2.transpose(outputs[0])])
    rows = outputs.shape[1]

    # Iterate through detections.
    for i in range(rows):
        classes_scores = outputs[0][i][4:]
        (minScore, maxScore, minClassLoc, (x, maxClassIndex)) = cv2.minMaxLoc(classes_scores)
        if maxScore >= 0.40:
            box = [
                outputs[0][i][0] - (0.5 * outputs[0][i][2]), outputs[0][i][1] - (0.5 * outputs[0][i][3]),
                outputs[0][i][2], outputs[0][i][3]]
            boxes.append(box)
            scores.append(maxScore)
            class_ids.append(maxClassIndex)

    result_boxes = cv2.dnn.NMSBoxes(boxes, scores, 0.45, 0.5)

# Perform non maximum suppression to eliminate redundant, overlapping boxes with lower confidences.
    for i in range(len(result_boxes)):
        index = result_boxes[i]
        box = boxes[index]
        label = "{}:{:.2f}".format(classes[class_ids[index]], scores[index])
        cv2.rectangle(input_image, (round(box[0] ), round(box[1] )),
                      (round((box[0] + box[2]) ), round((box[1] + box[3]) )),
                      settings.OPENCVCONFIG.COLORS.BLUE,
                      3 * settings.OPENCVCONFIG.TEXT_PARAMETERS.THICKNESS)
        
        draw_label(input_image, label, round(box[0] * scale), round(box[1] * scale))

        # Save predictions to Redis
        if timer.flag1:
            timer.timer_limit_start_save = start_timer(30)
            timer.flag1 = False
        if finish_timer(timer.timer_limit_start_save):
            if timer.flag2:
                timer.timer_limit_end_save = start_timer(10)
                timer.flag2 = False
            coordinate = Coordinate(left=box[0], top=box[1], width=box[2], height=box[3])
            singular_frame = Frame(coordinate=coordinate, label=classes[class_ids[index]])
            frames_to_redis.append(singular_frame.dict())

            result_timer_trigger = "Guardado en proceso..."

            if finish_timer(timer.timer_limit_end_save):
                delete_all_cache(key="prediction")
                save_cache(Prediction(
                    frame=frames_to_redis))
                frames_to_redis.clear()
                timer.flag1 = True
                timer.flag2 = True
                result_timer_trigger = "Guardado finalizado"
    class_ids.clear()
    boxes.clear()
    scores.clear()
    # input_image = cv2.resize(input_image, (1080, 640))
    return input_image


# Serving model
async def inference(net, frame, classes: List[str], timer: Timer, frames_to_redis):
    """
    This function should process the frame taken two arguments, net who is the model and image, so with this predict
    the objects inside.

    :param frames_to_redis:
    :param timer:
    :param net:
    :param frame:
    :param classes:
    :return: frame with prediction
    """
    # -----------------------------------------------------------
    # Process Image.
    detections = pre_process(frame, net)
    img = post_process(frame.copy(), detections, classes, timer, frames_to_redis)
    """    # Get performance about each object predicted and show it inside.
    t, _ = net.getPerfProfile()
    label = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())
    cv2.putText(img, label, (20, 40), settings.OPENCVCONFIG.TEXT_PARAMETERS.FONT_FACE,
                settings.OPENCVCONFIG.TEXT_PARAMETERS.FONT_SCALE,
                (0, 0, 255), settings.OPENCVCONFIG.TEXT_PARAMETERS.THICKNESS, cv2.LINE_AA)"""
    return img
