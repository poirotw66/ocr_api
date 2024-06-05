import argparse


def get_parser() -> argparse.Namespace:
    """
    Create argument parser for command line inputs.

    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='/home/PaddleOCR/datasets/Dataset_receipt/Dataset_ntu_val/23080104530H01_004!@!300017.jpg', help='input image')
    parser.add_argument('--det-model-dir', type=str, default='./weights/ch_PP-OCRv4_det', help='ppocr det model.pt path(s)')
    parser.add_argument('--rec-model-dir', type=str, default='./weights/tw_PP-OCRv3_rec', help='ppocr rec model.pt path(s)')
    parser.add_argument('--rec-char-dict-path', type=str, default='./weights/tw_PP-OCRv3_rec/230802_v2_common_dict.txt', help='ppocr char dict path(s)')
    parser.add_argument('--stage1-weight', type=str, default='./weights/yolo_stage1_best.pt', help='stage1 model.pt path(s)')
    parser.add_argument('--stage2-weight', type=str, default='./weights/yolo_stage2_best.pt', help='stage2 model.pt path(s)')
    parser.add_argument('--uvdoc-weight', type=str, default='./weights/UVDoc_best.pkl', help='uvdoc model.pkl path(s)')
    parser.add_argument('--ocr-keyword', type=str, default='./receipt_uni/config/hospital_key.txt', help='hosiptal key words file.')
    parser.add_argument('--api-code', type=str, default='./receipt_uni/config/hospital_api_map.txt', help='the key correspoding to the hospital name')
    parser.add_argument('--source', type=str, default='inference/images', help='source') 
    parser.add_argument('--img-size', type=int, default=640, help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='IOU threshold for NMS')
    parser.add_argument('--device', default='0', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='display results')
    parser.add_argument('--save-txt', action='store_true', default=True, help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', default=True, help='save confidences in --save-txt labels')
    parser.add_argument('--nosave', action='store_true', default=True, help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--project', default='receipt', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    parser.add_argument('--no-trace', action='store_true', default=True, help='don`t trace model')
    opt = parser.parse_args()
    return opt
