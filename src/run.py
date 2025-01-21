import io
import base64
import argparse
import cv2
from paddleocr import PaddleOCR
import os
import re
from receipt_uni.ocr_methods import (
    get_forward_img,
    read_image
)
from yolov7_detect import detect, load_model
from receipt_uni.crop_image_from_label import crop_image_from_label

from receipt_uni.correct_skew_eliminate_shadows import correct_skew_image, shadow
from receipt_uni.deskew_image import deskew
from receipt_uni.get_hospital_info import (
    get_hospital_key
)
from receipt_uni.hospital_pipeline import select_pipeline
from receipt_uni.convert_df_to_api_format import (
    convert_df_to_api_format,
    replace_mark,
    generate_json_result
)
from receipt_uni.config import get_parser
from UVDoc.UVDoc_demo import unwarp_img
from UVDoc.utils import IMG_SIZE, determine_scan_img, load_skew_model
import logging
logging.disable(logging.DEBUG)  
logging.disable(logging.WARNING)  
import time

if __name__ == "__main__":
    start = time.time()
    opt = get_parser()
    
    yolo_stage1 = load_model(opt, weights=opt.stage1_weight)
    yolo_stage2 = load_model(opt, weights=opt.stage2_weight)
    skew_model = load_skew_model(ckpt_path=opt.uvdoc_weight)
    ocr = PaddleOCR(det_model_dir=opt.det_model_dir,
                    rec_model_dir=opt.rec_model_dir, rec_char_dict_path=opt.rec_char_dict_path,
                    use_gpu=True, det_db_unclip_ratio=1.8,
                    det_db_score_mode='slow', det_db_thresh=0.1,
                    det_db_box_thresh=0.6, show_log=False, use_angle_cls=False)
    
    read_img = read_image(opt.input)
    is_scan = False
    
    # pre block
    forward_img, ocr_result, ocr_conf = get_forward_img(read_img, ocr, rotate_count=0, candidate=[])
    if not determine_scan_img(forward_img):
        forward_img = unwarp_img(forward_img, IMG_SIZE, skew_model)
        is_scan = True
    shadow_img = shadow(forward_img)

    field_data = {'欄位名稱': [], 'ocr辨識結果': []}
    hospital_key = get_hospital_key(ocr_result, opt.ocr_keyword)
    img_bgr = cv2.cvtColor(shadow_img, cv2.COLOR_RGB2BGR)
    label_stage1 = detect(im0s=img_bgr, model=yolo_stage1, opt=opt)
    img_stage1 = crop_image_from_label(img_bgr, label_stage1)
    if hospital_key == "KVGH" or is_scan:
        img_processed = img_stage1
    else:
        img_processed = deskew(img_stage1)

    # process block
    combined_df = select_pipeline(field_data, hospital_key, img_processed, ocr, yolo_stage2, opt)
    # post-process block
    generate_json_result(combined_df, opt.input)
    end = time.time()
    print(f"Processing completed.({(end - start)}s)")
