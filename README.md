# Receipt OCR API

使用 PaddleOCR + YOLOv7 + 自訂正則化流程，自動解析台灣各大醫院的住院/門診收據，輸出成 API 友善的 JSON 結構。The project focuses on end-to-end receipt normalization so downstream systems can consume clean structured data without knowing the image-specific quirks.

## 系統概覽 Overview
- 針對「是否含表格」自動切換兩階段 YOLO 偵測與專屬欄位解析管線。
- 結合 UVDoc unwarp、陰影/歪斜校正與 PaddleOCR，降低掃描品質差異帶來的誤差。
- 針對常見醫院（台大、長庚、彰基、榮總、奇美…）建立客製化正則表達式與欄位抽取程式。
- 產生含 `nhi/admissionDate/receivedAmount/items` 的 JSON，方便串接既有的財務或醫療資訊系統。

## Processing Pipeline
![Pipeline](ocr_pipeline.jpg)

1. 影像讀取與前處理：自動判斷正反向、UVDoc 展平、陰影與噪聲抑制 (`receipt_uni/ocr_methods.py`, `correct_skew_eliminate_shadows.py`, `deskew_image.py`, `UVDoc/` 模組)。
2. YOLO Stage 1：從背景偵測出收據區域 (`yolov7_detect.py`)。
3. (必要時) 再次校正與切割 (`crop_image_from_label.py`)。
4. OCR：以 PaddleOCR (det + rec) 取得全文結果，並根據關鍵字 (`hospital_key.txt`) 判斷醫院類別。
5. 決定是否存在表格，若有則啟用 YOLO Stage 2 偵測表格區塊。
6. 進入對應的 `HospitalPipeline` (`receipt_uni/hospital_pipeline.py`)：針對醫院特性做欄位正則化、表格欄位補強 (`receipt_uni/info/*.py`, `receipt_uni/config/regex_*.txt`)。
7. `convert_df_to_api_format.py` 轉成標準 JSON，並由 `generate_json_result` 印出結果。

新增醫院的邏輯與現有管線一致：判斷是否含表格 → 針對欄位撰寫 regex + 自訂抽取程式。

## Project Layout
```
.
├── README.md
├── src/
│   ├── run.py                  # 主要進入點
│   ├── Makefile                # make create => python run.py
│   ├── yolov7_detect.py        # YOLOv7 推論與模型載入
│   ├── receipt_uni/
│   │   ├── config/             # 醫院關鍵字、API map、欄位 regex
│   │   ├── config.py           # CLI 參數定義
│   │   ├── ocr_methods.py      # OCR 輔助函式、影像旋正
│   │   ├── hospital_pipeline.py# 各醫院資料處理流程
│   │   ├── info/               # 醫院欄位解析邏輯
│   │   ├── convert_df_to_api_format.py
│   │   └── correct_skew_eliminate_shadows.py 等影像處理工具
│   ├── models/, utils/         # YOLOv7 依賴
│   └── UVDoc/                  # 票據展平模型 (skew model)
└── *.png                       # 示意輸出圖
```

## Requirements
- Python 3.9+（建議使用虛擬環境）
- CUDA GPU（選用，但 PaddleOCR + YOLO 建議使用 GPU）
- 主要套件：`paddleocr`, `paddlepaddle-gpu`, `torch`, `torchvision`, `opencv-python-headless`, `numpy`, `pandas`, `Pillow`, `scikit-image`, `tqdm`, `PyYAML`
- 權重檔：  
  - PaddleOCR det/rec & 字典 (`./weights/ch_PP-OCRv4_det`, `./weights/tw_PP-OCRv3_rec`, `230802_v2_common_dict.txt`)  
  - YOLO Stage 1/2 (`yolo_stage1_best.pt`, `yolo_stage2_best.pt`)  
  - UVDoc 展平模型 (`UVDoc_best.pkl`)

## Installation
```bash
cd src
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
# GPU 版 PaddlePaddle (依 CUDA 版本調整)
pip install paddlepaddle-gpu==2.6.1.post119 -f https://www.paddlepaddle.org.cn/whl/linux/mkl/avx/stable.html
# 其餘依賴
pip install paddleocr torch torchvision torchaudio opencv-python-headless numpy pandas pillow scikit-image tqdm PyYAML
```
下載上述模型權重後放在 `src/weights/`，或透過 CLI 覆寫對應的路徑參數。

## Running Locally
### Quick start
```bash
cd src
make        # 預設 IMG/GPU 可在 Makefile 中調整
```

### Custom inference
```bash
python run.py \
  --input /path/to/receipt.jpg \
  --device 0 \
  --stage1-weight ./weights/yolo_stage1_best.pt \
  --stage2-weight ./weights/yolo_stage2_best.pt \
  --det-model-dir ./weights/ch_PP-OCRv4_det \
  --rec-model-dir ./weights/tw_PP-OCRv3_rec
```
常用參數來自 `receipt_uni/config.py`：

| Flag | 說明 |
| --- | --- |
| `--uvdoc-weight` | UVDoc 展平模型 |
| `--ocr-keyword` | 醫院關鍵字對照 (`hospital_key.txt`) |
| `--api-code` | 醫院 API 代碼 (`hospital_api_map.txt`) |
| `--img-size`, `--conf-thres`, `--iou-thres` | YOLO 推論設定 |
| `--view-img`, `--save-txt` | YOLO 偵測輸出控制 |

## Output Format
`generate_json_result` 會印出下列格式，並以檔案名稱為 key：
```
"23080115660001_006!@!300014.jpg" : {
    'nhi': 'Y',
    'admissionDate': '2023/07/09',
    'dischargeDate': '2023/07/17',
    'hospitalName': '彰化基督教醫療財團法人彰化基督教醫院',
    'dept': '胃腸肝膽內科',
    'receivedAmount': '12540',
    'items': {
        '預繳行動支付': '16254',
        '麻醉費': '330',
        '病房費': '10800',
        '膳食費': '90',
        '證明書費': '1000'
    }
},
```

## Hospital-specific Pipelines
- `receipt_uni/hospital_pipeline.py` 定義 `HospitalPipeline` 抽象類別與每家醫院的實作（NTU/CCH/CG/KVGH/ChiMei…）。
- `receipt_uni/info/*.py` 內含醫院專屬的欄位判定、欄位合併邏輯。
- `receipt_uni/config/regex_*.txt` 儲存欄位 vs regex mapping；若同欄位可能出現多次（如各項費用），可在 pipeline 中額外加總或客製處理。

### 新增醫院的建議流程
1. 在 `receipt_uni/config/hospital_key.txt` 加入醫院名稱關鍵字與對應 key。
2. 於 `receipt_uni/info/` 新增資料解析程式 & regex mapping (`regex_<HOSP>.txt`、`regex_<HOSP>_table.txt`)。
3. 在 `hospital_pipeline.py` 實作新 class，包含 `get_ocr_result`、`crop_from_label`、`text_info`、`table_info` 等方法。
4. 視需要調整 `hospital_api_map.txt` 以對應 API 代碼。

## 模組對照 (Quick Reference)
- `run.py`：整體流程協調、CLI 參數解析。
- `receipt_uni/ocr_methods.py`：OCR 前後處理、旋正、切割、表格文本抽取。
- `correct_skew_eliminate_shadows.py` / `deskew_image.py` / `shadow()`：影像前處理。
- `UVDoc/`：使用 UVDoc 模型修正 scan / 拍照造成的透視與彎曲。
- `yolov7_detect.py` + `models/`, `utils/`：YOLOv7 推論工具。
- `convert_df_to_api_format.py`：欄位標準化與 JSON 輸出。
- `get_hospital_info.py`：醫院關鍵字匹配、API 代碼轉換。

## 範例 (Samples)
### 台大收據 (NTU)
![NTU receipt](ntu1_image.png)
```
"台大收據1.jpg" : {
    'nhi': 'Y',
    'admissionDate': '2023/07/19',
    'dischargeDate': '2023/07/23',
    'hospitalName': '國立臺灣大學醫學院附設醫院',
    'dept': '骨科部',
    'receivedAmount': '84327',
    'items': {
        '藥費': '251',
        '治療處置費': '520',
        '材料費': '69006',
        '證明書費': '150',
        '病房費': '14400'
    }
},
```

### 長庚收據 (CG)
![CG receipt](cg1_image.png)
```
"長庚收據1.jpg" : {
    'nhi': 'Y',
    'admissionDate': '2023/07/28',
    'dischargeDate': '2023/07/28',
    'hospitalName': '林口長庚紀念醫院',
    'dept': '一般外科系',
    'receivedAmount': '20610',
    'items': {
        '住院部分負擔': '4651',
        '藥品費': '553',
        '材料費': '5520',
        '處置費': '9886'
    }
},
```

### 彰基收據 (CCH)
![CCH receipt](ck1_image.png)
```
"彰基收據1.jpg" : {
    'nhi': 'Y',
    'admissionDate': '2023/07/21',
    'dischargeDate': '2023/07/27',
    'hospitalName': '彰化基督教醫療財團法人彰化基督教醫院',
    'dept': '耳鼻喉暨頭頸部',
    'receivedAmount': '49430',
    'items': {
        '藥費': '1349',
        '材料費': '41919',
        '治療處置費': '650',
        '部分負擔': '5512'
    }
},
```

---
如需串接成 API 或延伸支援新的醫院，請依「Hospital-specific Pipelines」段落調整設定，即可快速擴充整體系統。