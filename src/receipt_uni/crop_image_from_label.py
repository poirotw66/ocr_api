import cv2
import numpy as np
from receipt_uni.correct_skew_eliminate_shadows import correct_skew_image


def find_high_conf_box(yolo_annotation_output: list) -> dict:
    """
    find the bounding box of highest cofidence.
    Args:
        - yolo_annotation_output: The output from YOLO label predictions
    Yields:
         A dict include the highest confindence bounding box.
    """
    annotations = []
    for i in yolo_annotation_output:
        parts = i.strip().split()
        if len(parts) == 6:  # Assuming each line has 6 elements
            class_id, x_center, y_center, width, height, confidences = map(
                float, parts)
            annotations.append({
                "class_id": int(class_id),
                "x_center": x_center,
                "y_center": y_center,
                "width": width,
                "height": height,
                "confidences": confidences
            })
    high_conf = 0
    high_box = []
    for annotation in annotations:
        if annotation["confidences"] > high_conf:
            high_conf = annotation["confidences"]
            high_box = annotation

    return high_box


def crop_image_from_label(img: np.ndarray, yolo_label: list) -> np.ndarray:
    """
    Crop the position according to the result of yolo.

    Args:
        - img: the processed img
        - label: the results after 1st_stage yolo model image processing

    Yields:
         Cropped image based on the detected object from YOLO label predictions.
    """
    try:
        # 讀取圖片
        w, h = img.shape[1], img.shape[0]
        # 讀取標籤文件
        max_box = find_high_conf_box(yolo_label)
        x_center, y_center, width, height = max_box["x_center"], max_box[
            "y_center"], max_box["width"], max_box["height"]
        x1 = int((x_center - width / 2) * w)
        y1 = int((y_center - height / 2) * h)
        x2 = int((x_center + width / 2) * w)
        y2 = int((y_center + height / 2) * h)

        img_roi = img[y1:y2, x1:x2]
        width = img_roi.shape[0]
        if width < 540:
            magnify = round(540 / width, 2)
            img_roi = cv2.resize(img_roi, dsize=None, fx=magnify, fy=magnify)
        return img_roi

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


def crop_image_from_label_stage2(
        img: np.ndarray,
        label: list,
        key: str,
        thr: float = 0.45) -> dict:
    """
    Crop the position according to the result of yolo.
    Args:
        - img: the processed img
        - label: the results after 2st_stage yolo model image processing
        - key: the key of different hospital
    Yields:
        Cropped image based on the detected object from stage2 YOLO label predictions.
    """
    w = img.shape[1]
    h = img.shape[0]
    output_dictionary = {}

    table_n = 0
    for line in label:
        msg = line.split(" ")
        x1 = int((float(msg[1]) - float(msg[3]) / 2) * w)  # x_center - width/2
        # y_center - height/2
        y1 = int((float(msg[2]) - float(msg[4]) / 2) * h)
        x2 = int((float(msg[1]) + float(msg[3]) / 2) * w)  # x_center + width/2
        # y_center + height/2
        y2 = int((float(msg[2]) + float(msg[4]) / 2) * h)
        # 裁剪
        img_roi = img[y1:y2, x1:x2]
        img_roi = correct_skew_image(img_roi, 'table')
        # 0_title 1_text 2_table
        if msg[0] == '2':
            save_name = f'table_{table_n}'
            table_n += 1
            length = img_roi.shape[1]
            if length < 540:
                magnify = round(540 / length, 2)
                img_roi = cv2.resize(
                    img_roi, dsize=None, fx=magnify, fy=magnify)
            output_dictionary[save_name] = img_roi
    return output_dictionary
