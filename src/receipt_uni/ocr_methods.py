import re
import cv2
from receipt_uni.convert_df_to_api_format import (
    replace_mark
)
import numpy as np
import io
import base64
from PIL import Image


def read_image(img_path: str) -> np.array:
    """
    Read an image from the specified path.

    Args:
        img_path (str): Path to the image file.

    Returns:
        numpy.ndarray: Image data as a NumPy array in RGB format.
    """
    with open(img_path, 'rb') as image_file:
        base64_image = base64.b64encode(image_file.read()).decode()
    image_bytes = base64.b64decode(base64_image)
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    return np.array(image)


def get_forward_img(
        img: np.ndarray,
        ocr,
        rotate_count: int = 0,
        candidate: list = []) -> tuple:
    """
    Determine if the incoming image is forward or not if not convert to forward.

    Args:
        img (numpy.ndarray): The input image.
        ocr: The OCR model.
        rotate_count (int, optional): The number of times the image has been rotated. Defaults to 0.
        candidate (list, optional): List of candidate strings. Defaults to [].

    Yields:
        tuple[np.ndarray, str, float]: A tuple containing the processed image, OCR result as string, and confidence score.
    """
    result = ocr.ocr(img)
    conf, width, height = list(), list(), list()
    for _, res in enumerate(result):
        input_text = ""
        if res is not None:
            for line in res:
                width.append(line[0][0][0] - line[0][1][0])
                height.append(line[0][0][1] - line[0][3][1])
                conf.append(line[1][1])
                if line and len(line) > 1 and line[1]:
                    input_text += str(line[1][0]) + ' '
                else:
                    input_text += str(line[0])
    input_text = replace_mark(input_text)
    average_w = np.mean(width)
    average_h = np.mean(height)
    average_c = np.mean(conf)
    aspect_ratio = average_w / average_h
    candidate.append([average_c, input_text, img, aspect_ratio])
    if aspect_ratio >= 1:
        if rotate_count <= 1 and average_c <= 0.95:
            output_ROTATE_180 = cv2.rotate(img, cv2.ROTATE_180)
            rotate_count += 1
            return get_forward_img(
                output_ROTATE_180, ocr, rotate_count, candidate)
        elif rotate_count > 1 and average_c <= 0.95:
            max_sublist = max(candidate, key=lambda x: len(x[1]))
            return max_sublist[2], max_sublist[1], average_c
        else:
            return img, input_text, average_c
    elif aspect_ratio < 1:
        output_ROTATE_90_CLOCKWISE = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        candidate = []
        return get_forward_img(
            output_ROTATE_90_CLOCKWISE,
            ocr,
            rotate_count,
            candidate)


def calc_new_line_threshold(bbox_list: list) -> float:
    """
    Calculate delta-y threshold for generating new lines.

    Args:
        - bbox_list (list): list for bbox and OCR results

    Yields:
        A float value representing the new line splitting threshold
    """
    basket = list()
    for _, res in enumerate(bbox_list):
        if res is not None:
            for line in res:
                basket.append((line[0][-1][1] + line[0][-2]
                              [1] - line[0][0][1] - line[0][1][1]) / 2)
    return np.mean(basket) * 0.58


def get_ocr_sentence_result(img: np.ndarray, ocr) -> str:
    """
    Get the OCR result from the given image using the provided OCR model.

    Args:
        img (numpy.ndarray): The input image.
        ocr: The OCR model.

    Yields:
        str: The OCR result as a string.
    """
    result = ocr.ocr(img, cls=False)
    thr = calc_new_line_threshold(result)
    for _, res in enumerate(result):
        current_y = None
        rows = 0
        permutation = []
        input_text = ""
        if res is not None:
            for line in res:
                center_x = (line[0][0][0] + line[0][2][0]) / 2
                center_y = line[0][0][1]
                if current_y is not None and abs(
                        center_y - current_y) < thr:  # 15 #18
                    permutation.append((rows, center_x, line[1][0]))
                else:
                    rows += 1
                    permutation.append((rows, center_x, line[1][0]))
                    current_y = center_y
        sorted_permutation = sorted(permutation, key=lambda x: (x[0], x[1]))
        for row, x, res in sorted_permutation:
            input_text += res + " "
        input_text = replace_mark(input_text)
    return input_text


def get_ocr_sentence_border_result(
        img: np.ndarray,
        ocr,
        border: float,
        comparison: int = 1) -> str:
    """
    Get the OCR result with border.

    Args:
        img (numpy.ndarray): The input image.
        ocr: The OCR model.
        border (float): Ratio of horizontal axis coordinates.
        comparison (int, optional): Flag to determine whether to keep right (1) or left (0). Defaults to 1.

    Yields:
        str: The OCR result as a string.
    """
    result = ocr.ocr(img, cls=False)
    length = img.shape[1]
    mid = int(length * border)
    thr = calc_new_line_threshold(result)
    for idx, res in enumerate(result):
        current_y = None
        rows = 0
        permutation = []
        input_text = ""
        if res is not None:
            for line in res:
                a, b, c, d = line[0]
                center_x = (a[0] + b[0] + c[0] + d[0]) / 4
                center_y = (a[1] + b[1] + c[1] + d[1]) / 4
                if comparison:
                    if line and len(line) > 1 and line[1] and center_x > mid:
                        if current_y is not None and abs(
                                center_y - current_y) < thr:
                            permutation.append((rows, center_x, line[1][0]))
                        else:
                            rows += 1
                            permutation.append((rows, center_x, line[1][0]))
                            current_y = center_y
                else:
                    left = int(length * 0.1)
                    if line and len(
                            line) > 1 and line[1] and center_x < mid and center_x > left:
                        if current_y is not None and abs(
                                center_y - current_y) < thr:
                            permutation.append((rows, center_x, line[1][0]))
                        else:
                            rows += 1
                            permutation.append((rows, center_x, line[1][0]))
                            current_y = center_y
            sorted_permutation = sorted(
                permutation, key=lambda x: (x[0], x[1]))
            for row, x, res in sorted_permutation:
                input_text += res + " "
            input_text = replace_mark(input_text)
            input_text = re.sub('[a-zA-Z]', '', input_text)
    return input_text


def get_ocr_sentence_bi_border_result(
        img: np.ndarray,
        ocr,
        left: float,
        right: float) -> str:
    """
    Get the OCR result with borders (left & right).

    Args:
        img (numpy.ndarray): The input image.
        ocr: The OCR model.
        left (float): Ratio of horizontal axis coordinates for the left border.
        right (float): Ratio of horizontal axis coordinates for the right border.

    Yields:
        str: The OCR result as a string.
    """
    result = ocr.ocr(img, cls=False)
    length = img.shape[1]
    left = int(length * left)
    right = int(length * right)
    thr = calc_new_line_threshold(result)
    for _, res in enumerate(result):
        current_y = None
        rows = 0
        permutation = []
        input_text = ""
        if res is not None:
            for line in res:
                a, b, c, d = line[0]
                center_x = (a[0] + b[0] + c[0] + d[0]) / 4
                center_y = (a[1] + b[1] + c[1] + d[1]) / 4

                if line and len(line) > 1 and line[1] and (
                        center_x < left or center_x > right):
                    if current_y is not None and abs(
                            center_y - current_y) < thr:
                        permutation.append((rows, center_x, line[1][0]))
                    else:
                        rows += 1
                        permutation.append((rows, center_x, line[1][0]))
                        current_y = center_y
            sorted_permutation = sorted(
                permutation, key=lambda x: (x[0], x[1]))
            for row, x, res in sorted_permutation:
                input_text += res + " "
            input_text = replace_mark(input_text)
    return input_text


def get_ocr_table_line_result(step4_dict: dict, border: float, ocr) -> str:
    """
    Get OCR results for table.

    Args:
        step4_dict (dict): The dictionary containing table lines.
        border (float): Ratio of horizontal axis coordinates.
        ocr: The OCR model.

    Yields:
        str: The OCR result as a string.
    """
    field_data = {'欄位名稱': [], 'ocr辨識結果': []}
    input_text = ""
    for key in step4_dict.keys():
        key_label = key.split('_')[0]
        if key_label == 'table':
            img = step4_dict[key]
            result = ocr.ocr(img, cls=False)
            length = img.shape[1]
            left = int(length * border[0])
            right = int(length * border[1])
            thr = calc_new_line_threshold(result)
            # print('thr=',thr)
            for idx, res in enumerate(result):
                if res is not None:
                    current_y = None
                    rows = 0
                    permutation = []
                    for line in res:
                        a, b, c, d = line[0]
                        center_x = (a[0] + b[0] + c[0] + d[0]) / 4
                        center_y = (a[1] + b[1] + c[1] + d[1]) / 4

                        if line and len(line) > 1 and line[1] and (
                                center_x < left or center_x > right):
                            if current_y is not None and abs(
                                    center_y - current_y) < thr:
                                permutation.append(
                                    (rows, center_x, line[1][0]))
                            else:
                                rows += 1
                                permutation.append(
                                    (rows, center_x, line[1][0]))
                                current_y = center_y

                    sorted_permutation = sorted(
                        permutation, key=lambda x: (x[0], x[1]))
                    for row, x, res in sorted_permutation:
                        input_text += res + " "

    return input_text


def contains_spaces_and_no_numbers(string: str) -> bool:
    """
    Check if the string contains spaces but no numbers.

    Args:
        string (str): The input string.

    Yields:
        bool: True if the string contains spaces but no numbers, otherwise False.
    """
    # Check if the string contains spaces
    if re.search(r'\s', string):
        # Check if the string contains no numbers
        if not re.search(r'\d', string):
            return True
    return False