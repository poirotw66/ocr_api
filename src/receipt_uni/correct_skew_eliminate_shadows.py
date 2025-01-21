import numpy as np
import cv2
from skimage.feature import canny
from skimage.transform import hough_line, hough_line_peaks, rotate
from skimage.color import rgb2gray
from skimage import draw
from skimage import io
import matplotlib.pyplot as plt


class SkewDetect:
    def __init__(
            self,
            input_file=None,
            key=None,
            sigma=1.5,
            num_peaks=15,
            thr=0.35):
        """
        Initialize the SkewDetect object.
        """
        self.input_file = input_file
        self.sigma = sigma
        self.num_peaks = num_peaks
        self.thr = thr
        self.key = key

    def get_max_freq_elem(self, arr: list) -> list:
        """
        Get the element(s) with the maximum frequency from the input list.

        Args:
            arr (list): The input list.

        Returns:
            list: List of elements with maximum frequency.
        """
        max_arr = []
        freqs = {}
        for i in arr:
            if i in freqs:
                freqs[i] += 1
            else:
                freqs[i] = 1

        sorted_keys = sorted(freqs, key=freqs.get, reverse=True)
        if sorted_keys:
            max_freq = freqs[sorted_keys[0]]

            for k in sorted_keys:
                if freqs[k] == max_freq:
                    max_arr.append(k)

        return max_arr

    def compare_sum(self, value: float) -> bool:
        """
        Compare the input value with a range.

        Args:
            value (float): The input value.

        Returns:
            bool: True if the value is between 44 and 46 (inclusive), False otherwise.
        """
        if value >= 44 and value <= 46:
            return True
        else:
            return False

    @staticmethod
    def calculate_deviation(angle: float) -> float:
        """
        Calculate the deviation of an angle from a target angle.

        Args:
            angle (float): The input angle.

        Returns:
            float: The deviation of the angle from pi/4.
        """
        angle_in_degrees = np.abs(angle)
        deviation = np.abs(np.pi / 4 - angle_in_degrees)
        return deviation

    def process_single_file(self):
        res = self.determine_skew(self.input_file)
        return res

    def add_mask(
            self,
            img: np.ndarray,
            s: float = 7.5,
            e: float = 9) -> np.ndarray:
        """
        Add a mask to the input image.

        Args:
            img (np.ndarray): The input image.
            s (float, optional): Start ratio for the mask. Defaults to 7.5.
            e (float, optional): End ratio for the mask. Defaults to 9.

        Returns:
            np.ndarray: The masked image.
        """
        mask = np.zeros_like(img)
        width, length = img.shape
        rr, cc = draw.rectangle(
            start=(width / s, 0), end=(width * e / 11, length), shape=mask.shape)  # 7.5/11
        rr = rr.astype(int)
        cc = cc.astype(int)
        mask[rr, cc] = 1
        masked_image = np.copy(img)
        masked_image[mask == 0] = 0
        return masked_image

    def determine_skew(self, img_file: np.ndarray) -> dict:
        """
        Determine the skew of the input image.

        Args:
            img_file (np.ndarray): The input image.

        Returns:
            dict: A dictionary containing information about the skew.
        """
        img = cv2.cvtColor(img_file, cv2.COLOR_BGR2RGB)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        edges = canny(img, sigma=self.sigma)
        if self.key == 'CCH':
            edges = self.add_mask(edges, 7.5, 9)  # thr=0.35
        if self.key == 'TVGH':
            edges = self.add_mask(edges, 7.5, 8)
        h, a, d = hough_line(edges)
        _, ap, _ = hough_line_peaks(
            h, a, d, threshold=self.thr * np.max(h), num_peaks=self.num_peaks)
        if len(ap) == 0:
            return {"Image File": img_file, "Message": "Bad Quality"}

        absolute_deviations = []
        for k in ap:
            slope = np.tan(k)
            if abs(slope) > 6:
                deviation = self.calculate_deviation(k)
                absolute_deviations.append(deviation)
        average_deviation = np.mean(np.rad2deg(absolute_deviations))
        ap_deg = []
        for x in ap:
            slope = np.tan(x)
            if abs(slope) > 6:
                ap_deg.append(np.rad2deg(x))

        bin_0_45 = []
        bin_45_90 = []
        bin_0_45n = []
        bin_45_90n = []

        for ang in ap_deg:

            deviation_sum = int(90 - ang + average_deviation)
            if self.compare_sum(deviation_sum):
                bin_45_90.append(ang)
                continue

            deviation_sum = int(ang + average_deviation)
            if self.compare_sum(deviation_sum):
                bin_0_45.append(ang)
                continue

            deviation_sum = int(-ang + average_deviation)
            if self.compare_sum(deviation_sum):
                bin_0_45n.append(ang)
                continue

            deviation_sum = int(90 + ang + average_deviation)
            if self.compare_sum(deviation_sum):
                bin_45_90n.append(ang)

        angles = [bin_0_45, bin_45_90, bin_0_45n, bin_45_90n]
        lmax = 0

        for j in range(len(angles)):
            angle_length = len(angles[j])
            if angle_length >= lmax:
                lmax = angle_length
                maxi = j

        if lmax:
            ans_arr = self.get_max_freq_elem(angles[maxi])
            ans_res = np.mean(ans_arr)

        else:
            ans_arr = self.get_max_freq_elem(ap_deg)
            ans_res = np.mean(ans_arr)

        data = {
            "Image File": img_file,
            "Average Deviation from pi/4": average_deviation,
            "Estimated Angle": ans_res,
            "Angle bins": angles}
        # print('data:',data)
        return data


def shadow(img: np.ndarray) -> np.ndarray:
    """
    Remove shadow from the input image.

    Args:
        img (np.ndarray): The input image.

    Yields:
        np.ndarray: The shadow-free image.
    """
    blue, green, red = cv2.split(img)
    rgb_planes = [blue, green, red]
    result_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        result_planes.append(diff_img)

    result = cv2.merge(result_planes)
    return result


def correct_skew_image(
        img: np.ndarray,
        key: str = None,
        thresold: float = 0.45) -> np.ndarray:
    """
    Corrects skew in the input image and optionally processes based on a key and threshold.

    Args:
        img (np.ndarray): The input image.
        key (str, optional): A key for processing. Defaults to None.
        threshold (float, optional): Threshold value for processing. Defaults to 0.45.

    Returns:
        np.ndarray: The processed image.
    """
    if key == 'table':
        skew_obj = SkewDetect(img, key, thr=thresold)
    else:
        skew_obj = SkewDetect(img, key)
    origin_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    res = skew_obj.process_single_file()
    angle = res['Estimated Angle']
    if np.isnan(angle):
        rot_angle = 0
    elif -45 <= angle <= 90:
        rot_angle = angle - 90
    elif -90 <= angle < -45:
        rot_angle = 90 + angle
    else:
        rot_angle = angle - 90
    rotated = rotate(
        origin_img,
        rot_angle,
        resize=True,
        mode='constant',
        cval=1.0)
    rotated_gray = rgb2gray(rotated)
    image_rotated = cv2.cvtColor(
        np.uint8(
            rotated_gray * 255),
        cv2.COLOR_RGB2BGR)
    return image_rotated
