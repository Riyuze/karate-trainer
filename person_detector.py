import cv2
import numpy as np
import tensorflow as tf
from yolov3.utils import Load_Yolo_model, image_preprocess, postprocess_boxes, nms
from yolov3.configs import *
import os

def import_images(path):
    images = []

    for image in os.listdir(path):
        f = os.path.join(path, image)

        if os.path.isfile(f):
            images.append(f)

    return images

def crop(image, bboxes):
    for bbox in bboxes:
        coor = np.array(bbox[:4], dtype=np.int32)
        class_ind = int(bbox[5])
        (x1, y1), (x2, y2) = (coor[0], coor[1]), (coor[2], coor[3])

        # crop image if person
        if class_ind == 0:
            cropped_image = image[y1-50:y2+50, x1-50:x2+50]
            return cropped_image
        
    return None

def detect_and_crop_image(Yolo, image_path, output_path, input_size=416, show=False, score_threshold=0.3, iou_threshold=0.45):
    original_image = cv2.imread(image_path)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    image_data = image_preprocess(np.copy(original_image), [
                                  input_size, input_size])
    image_data = image_data[np.newaxis, ...].astype(np.float32)

    if YOLO_FRAMEWORK == "tf":
        pred_bbox = Yolo.predict(image_data)
    elif YOLO_FRAMEWORK == "trt":
        batched_input = tf.constant(image_data)
        result = Yolo(batched_input)
        pred_bbox = []
        for key, value in result.items():
            value = value.numpy()
            pred_bbox.append(value)

    pred_bbox = [tf.reshape(x, (-1, tf.shape(x)[-1])) for x in pred_bbox]
    pred_bbox = tf.concat(pred_bbox, axis=0)

    bboxes = postprocess_boxes(
        pred_bbox, original_image, input_size, score_threshold)
    bboxes = nms(bboxes, iou_threshold, method='nms')

    image = crop(original_image, bboxes)
    # CreateXMLfile("XML_Detections", str(int(time.time())), original_image, bboxes, read_class_names(CLASSES))

    if output_path != '':
        cv2.imwrite(output_path, image)
    if show:
        # Show the image
        cv2.imshow("Predicted image", image)
        # Load and hold the image
        cv2.waitKey(0)
        # To close the window after the required kill value was provided
        cv2.destroyAllWindows()

    return image
    
def person_detector(path):
    images = import_images(path)

    yolo = Load_Yolo_model()

    image_path = os.path.join('./cropped_pose', path.split('\\')[1])
    if not os.path.exists(image_path):
        os.makedirs(image_path)

        for image in images:
            detect_and_crop_image(yolo, image, os.path.join('./cropped_pose', image.split('\\')[1], image.split('\\')[2]), show=False)
