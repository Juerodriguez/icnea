import cv2
import numpy as np
from ..config import Settings
import time

settings = Settings()


def draw_label(im, label, x, y):
    """Draw text onto image at location."""
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
    # Create a 4D blob from a frame.
    blob = cv2.dnn.blobFromImage(input_image, 1 / 255,
                                 (settings.OPENCVCONFIG.CONSTANTS.INPUT_WIDTH,
                                  settings.OPENCVCONFIG.CONSTANTS.INPUT_HEIGHT),
                                 [0, 0, 0], 1, crop=False)

    # Sets the input to the network.
    net.setInput(blob)
    # Run the forward pass to get output of the output layers.
    outputs = net.forward(net.getUnconnectedOutLayersNames())
    return outputs


def post_process(input_image, outputs, classes):
    # Lists to hold respective values while unwrapping.
    class_ids = []
    confidences = []
    boxes = []
    # Rows.
    rows = outputs[0].shape[1]
    image_height, image_width = input_image.shape[:2]
    # Resizing factor.
    x_factor = image_width / settings.OPENCVCONFIG.CONSTANTS.INPUT_WIDTH
    y_factor = image_height / settings.OPENCVCONFIG.CONSTANTS.INPUT_HEIGHT
    # Iterate through detections.
    for r in range(rows):
        row = outputs[0][0][r]
        confidence = row[4]
        # Discard bad detections and continue.
        if confidence >= settings.OPENCVCONFIG.CONSTANTS.CONFIDENCE_THRESHOLD:
            classes_scores = row[5:]
            # Get the index of max class score.
            class_id = np.argmax(classes_scores)
            #  Continue if the class score is above threshold.
            if classes_scores[class_id] > settings.OPENCVCONFIG.CONSTANTS.SCORE_THRESHOLD:
                confidences.append(confidence)
                class_ids.append(class_id)
                cx, cy, w, h = row[0], row[1], row[2], row[3]
                left = int((cx - w / 2) * x_factor)
                top = int((cy - h / 2) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)
                box = np.array([left, top, width, height])
                boxes.append(box)
# Perform non maximum suppression to eliminate redundant, overlapping boxes with lower confidences.
    indices = cv2.dnn.NMSBoxes(boxes, confidences,
                               settings.OPENCVCONFIG.CONSTANTS.CONFIDENCE_THRESHOLD,
                               settings.OPENCVCONFIG.CONSTANTS.NMS_THRESHOLD)
    for i in indices:
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        # Draw bounding box.
        cv2.rectangle(input_image, (left, top), (left + width, top + height),
                      settings.OPENCVCONFIG.COLORS.BLUE,
                      3*settings.OPENCVCONFIG.TEXT_PARAMETERS.THICKNESS)
        # Class label.
        label = "{}:{:.2f}".format(classes[class_ids[i]], confidences[i])
        # Draw label.
        draw_label(input_image, label, left, top)
    return input_image


# Serving model
async def inference(net, frame, classes):
    """
    This function should process the frame taken two arguments, net who is the model and image, so with this predict
    the objects inside.

    :param net:
    :param frame:
    :param classes:
    :return: frame with prediction
    """
    # -----------------------------------------------------------
    # Process Image.
    detections = pre_process(frame, net)
    img = post_process(frame.copy(), detections, classes)
    # Get performance about each object predicted and show it inside.
    t, _ = net.getPerfProfile()
    label = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())
    cv2.putText(img, label, (20, 40), settings.OPENCVCONFIG.TEXT_PARAMETERS.FONT_FACE,
                settings.OPENCVCONFIG.TEXT_PARAMETERS.FONT_SCALE,
                (0, 0, 255), settings.OPENCVCONFIG.TEXT_PARAMETERS.THICKNESS, cv2.LINE_AA)
    return img
