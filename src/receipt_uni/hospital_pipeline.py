from receipt_uni.info.extract_info_from_Others import (
    extract_column_from_Others,
    extract_info_from_Others
)
from receipt_uni.info.extract_info_from_NTU import (
    # extract_info_from_NTU,
    # extract_column_from_NTU,
    extract_column_custom_NTU
)
from receipt_uni.info.extract_info_from_CCH import (
    extract_info_from_CCH,
    extract_column_from_CCH,
    is_numeric
)
from receipt_uni.info.extract_info_from_CG import (
    extract_info_from_CG,
    during_hos_from_text_CG,
    date_info_from_text_CG,
    confirm_scope_identity,
    check_details_CG,
    depaerment_from_text_CG,
)
from receipt_uni.info.extract_info_from_CMH import (
    extract_info_from_CMH,
    extract_column_from_CMH
)
# from receipt_uni.info.extract_info_from_NCKU import (
#     extract_info_from_NCKU,
#     during_hos_from_text_NCKU,
#     date_info_from_text_NCKU,
#     confirm_scope_identity,
#     check_details,
#     depaerment_from_text_NCKU,
# )
from receipt_uni.info.extract_info_from_TVGH import (
    extract_info_from_TVGH,
    extract_column_from_TVGH,
)
from receipt_uni.info.extract_info_from_TCGH import (
    extract_info_from_TCGH,
    extract_column_from_TCGH,
)
from receipt_uni.info.extract_info_from_TCGH_puli import (
    extract_info_from_TCGH_puli,
    extract_column_from_TCGH_puli,
)
from receipt_uni.info.extract_info_from_KVGH import (
    extract_info_from_KVGH,
    extract_column_from_KVGH,
    extract_sect_from_KVGH,
    check_type_KVGH
)
from receipt_uni.info.extract_info_from_ChiMei import (
    extract_column_from_ChiMei,
    extract_info_from_ChiMei,
    extract_sect_from_ChiMei
)
# from receipt_uni.info.extract_info_from_KMU import (
#     extract_info_from_KMU,
#     extract_column_from_KMU,
# )
from receipt_uni.convert_df_to_api_format import (
    replace_mark,
    update_dict_with_regex_pattern
)
from yolov7_detect import detect
from receipt_uni.crop_image_from_label import crop_image_from_label_stage2
from receipt_uni.get_hospital_info import (
    hospital_info_from_NTU,
    hospital_info_from_CCH,
    hospital_info_from_CG,
    hospital_info_from_CMH,
    hospital_info_from_TVGH,
    hospital_info_from_TCGH,
    hospital_info_from_TCGH_puli,
    hospital_info_from_KMU,
    hospital_info_from_KVGH,
    hospital_info_from_NCKU,
    hospital_info_from_ChiMei
)
from receipt_uni.ocr_methods import (
    get_ocr_table_line_result,
    get_ocr_sentence_border_result,
    get_ocr_sentence_bi_border_result,
    get_ocr_sentence_result
)
import pandas as pd
import re
from abc import ABC, abstractmethod
import json


class HospitalPipeline(ABC):
    """
    Abstract class defining methods for processing hospital data pipeline.
    """
    @abstractmethod
    def get_ocr_result(self, img, ocr) -> str:
        """
        Abstract method for processing an image and returning the result in JSON format.

        Args:
            img: Data representing the image.
            ocr: The OCR Model being used.

        Returns:
            str: Result in string format.
        """
        pass

    @abstractmethod
    def crop_from_label(self, img, yolo_stage2, opt, key, thr=0.45):
        """
        Crop image regions based on YOLO results.

        Args:
            img: Processed image.
            yolo_stage2: Results after second stage YOLO model image processing.
            opt: Options.
            key: Key for different hospitals.
            thr: Threshold parameter (default: 0.45).
        """
        pass

    @abstractmethod
    def preprocess_data(self, rs_ocr):
        """
        Preprocess data.

        Args:
            rs_ocr: Data from OCR result.
        """
        pass

    @abstractmethod
    def text_info(self, rs_ocr, field_data):
        """
        Process text information.

        Args:
            rs_ocr: Data from OCR result.
            field_data: Field data.
        """
        pass

    @abstractmethod
    def table_info(self, rs_ocr_range, field_data, dict4, ocr):
        """
        Process table information.

        Args:
            rs_ocr_range: Range information from OCR result.
            field_data: Field data.
            dict4: Dictionary.
            ocr: OCR related information.
        """
        pass

    @abstractmethod
    def check_if_details(self, rs_ocr):
        """
        Check if there are details available.

        Args:
            rs_ocr: Data from OCR result.
        """
        pass

    @abstractmethod
    def detail_info(self, rs_ocr, field_data):
        """
        Process detailed information.

        Args:
            rs_ocr: Data from OCR result.
            field_data: Field data.
        """
        pass

    @abstractmethod
    def extract_column_json(self, text, field_data):
        """
        Extract column data from JSON-formatted text.

        Args:
            text (str): The JSON-formatted text.
            field_data (dict): A dictionary to store the extracted data.

        Returns:
            dict: The updated field data dictionary.
        """
        pass

    @abstractmethod
    def extract_column_customization(self, text, field_data):
        """
        Extract column data with customization.

        Args:
            text (str): The input text.
            field_data (dict): A dictionary to store the extracted data.

        Returns:
            dict: The updated field data dictionary.
        """
        pass

    @abstractmethod
    def extract_table_column_json(self, text, field_data):
        """
        Extract column data from JSON-formatted text in table.

        Args:
            text (str): The JSON-formatted text.
            field_data (dict): A dictionary to store the extracted data.

        Returns:
            dict: The updated field data dictionary.
        """
        pass

    @abstractmethod
    def extract_hospital_name(self, rs_ocr, field_data):
        """
        Extract hospital name from OCR results.

        Args:
            rs_ocr (numpy.ndarray): The OCR results.
            field_data (dict): A dictionary to store the extracted data.

        Returns:
            dict: The updated field data dictionary.
        """
        pass


class Others_Pipeline(HospitalPipeline):
    def crop_from_label(self, img, yolo_stage2, opt, key, thr=0.45):
        pass

    def preprocess_data(self, rs_ocr):
        return re.sub('[a-zA-Z]', '', rs_ocr)

    def text_info(self, rs_ocr, field_data):
        field_data = self.extract_hospital_name(rs_ocr, field_data)
        field_data = self.extract_column_customization(rs_ocr, field_data)
        field_data = self.extract_column_json(rs_ocr, field_data)
        # extract_column_from_Others(rs_ocr,field_data)
        return pd.DataFrame(field_data)

    def table_info(self, rs_ocr_range, field_data, dict4, ocr):
        return field_data

    def check_if_details(self, rs_ocr):
        return False

    def detail_info(self, rs_ocr, field_data):
        pass

    def extract_column_json(self, text, field_data):
        with open('./receipt_uni/config/regex_Others.txt', 'r') as f:
            field_regex_map = json.load(f)
        return update_dict_with_regex_pattern(
            text, field_data, field_regex_map)

    def extract_column_customization(self, text, field_data):
        return extract_info_from_Others(text, field_data)

    def extract_table_column_json(self, text, field_data):
        pass

    def extract_hospital_name(self, text, field_data):
        return field_data


class NTU_Pipeline(HospitalPipeline):
    def get_ocr_result(self, img, ocr) -> str:
        return replace_mark(get_ocr_sentence_result(img, ocr=ocr))

    def crop_from_label(self, img, yolo_stage2, opt, key, thr=0.45):
        label2 = detect(im0s=img, model=yolo_stage2, opt=opt)
        return crop_image_from_label_stage2(img, label2, key, thr=0.45)

    def preprocess_data(self, rs_ocr):
        return rs_ocr

    def text_info(self, rs_ocr, field_data):
        field_data = self.extract_hospital_name(rs_ocr, field_data)
        field_data = self.extract_column_json(rs_ocr, field_data)
        field_data = self.extract_column_customization(rs_ocr, field_data)
        return pd.DataFrame(field_data)

    def table_info(self, rs_ocr_range, field_data, dict4, ocr):
        rs_table = get_ocr_table_line_result(
            dict4, border=[0.48, 0.75], ocr=ocr)
        rs_table = replace_mark(rs_table)
        # table_columns = extract_column_from_NTU(rs_table)
        table_columns = self.extract_table_column_json(rs_table)
        return pd.concat([table_columns, field_data], axis=0)

    def check_if_details(self, rs_ocr):
        return False

    def detail_info(self, rs_ocr, field_data):
        pass

    def extract_column_json(self, text, field_data):
        with open('./receipt_uni/config/regex_NTU.txt', 'r') as f:
            field_regex_map = json.load(f)
        return update_dict_with_regex_pattern(
            text, field_data, field_regex_map)

    def extract_column_customization(self, text, field_data):
        return extract_column_custom_NTU(text, field_data)

    def extract_table_column_json(self, text):
        field_data = {'欄位名稱': [], 'ocr辨識結果': []}
        with open('./receipt_uni/config/regex_NTU_table.txt', 'r') as f:
            field_regex_map = json.load(f)
        with open('./receipt_uni/config/regex_NTU_table_part.txt', 'r') as f:
            field_part_regex_map = json.load(f)
        index = text.find('部份負擔')
        ex_index = text.find('基本部分負擔')
        if index != -1:
            if ex_index != -1:
                return pd.DataFrame(
                    update_dict_with_regex_pattern(
                        text, field_data, field_regex_map))
            else:
                return pd.DataFrame(
                    update_dict_with_regex_pattern(
                        text, field_data, field_part_regex_map))
        else:
            return pd.DataFrame(
                update_dict_with_regex_pattern(
                    text, field_data, field_regex_map))

    def extract_hospital_name(self, text, field_data):
        if '醫院名稱' not in field_data['欄位名稱']:
            return hospital_info_from_NTU(text[:50], field_data)
        else:
            return field_data


class CG_Pipeline(HospitalPipeline):
    def get_ocr_result(self, img, ocr) -> str:
        return replace_mark(get_ocr_sentence_result(img, ocr=ocr))

    def crop_from_label(self, img, yolo_stage2, opt, key, thr=0.45):
        pass

    def preprocess_data(self, rs_ocr):
        return rs_ocr.replace('31日', ' 31日')

    def text_info(self, rs_ocr, field_data):
        # hospital_info_from_CG(rs_ocr[:50],field_data) if '醫院名稱' not in field_data['欄位名稱'] else None
        field_data = self.extract_hospital_name(rs_ocr, field_data)
        rs_ocr_range = confirm_scope_identity(rs_ocr, field_data)
        field_data = self.extract_column_json(rs_ocr_range, field_data)
        field_data = self.extract_column_customization(
            rs_ocr, rs_ocr_range, field_data)
        return pd.DataFrame(field_data)

    def table_info(self, rs_ocr_range, field_data, dict4, ocr):
        return field_data

    def check_if_details(self, rs_ocr):
        return check_details_CG(rs_ocr)

    def detail_info(self, rs_ocr, field_data):
        field_data['欄位名稱'].append('項目名稱')
        field_data['ocr辨識結果'].append(0)
        hospital_info_from_CG(
            rs_ocr[:50], field_data) if '醫院名稱' not in field_data['欄位名稱'] else None
        date_info_from_text_CG(rs_ocr, field_data)
        field_data['欄位名稱'].append('社保身份')
        field_data['ocr辨識結果'].append('自費')
        return pd.DataFrame(field_data)

    def extract_column_json(self, text, field_data):
        with open('./receipt_uni/config/regex_CG.txt', 'r') as f:
            field_regex_map = json.load(f)
        return update_dict_with_regex_pattern(
            text, field_data, field_regex_map)

    def extract_column_customization(self, text, text_range, field_data):
        field_data = during_hos_from_text_CG(text_range, field_data)
        field_data = extract_info_from_CG(text_range, field_data)
        field_data = depaerment_from_text_CG(text, field_data)
        field_data = date_info_from_text_CG(text, field_data)
        return field_data

    def extract_table_column_json(self, text, field_data):
        pass

    def extract_hospital_name(self, text, field_data):
        if '醫院名稱' not in field_data['欄位名稱']:
            return hospital_info_from_CG(text[:50], field_data)
        else:
            return field_data


class CCH_Pipeline(HospitalPipeline):

    def get_ocr_result(self, img, ocr) -> str:
        return replace_mark(get_ocr_sentence_result(img, ocr=ocr))

    def crop_from_label(self, img, yolo_stage2, opt, key, thr=0.45):
        label2 = detect(im0s=img, model=yolo_stage2, opt=opt)
        dict4 = crop_image_from_label_stage2(img, label2, key, thr=0.45)
        return dict4

    def preprocess_data(self, rs_ocr):
        return rs_ocr

    def text_info(self, rs_ocr, field_data):
        # hospital_info_from_CCH(rs_ocr[:50],field_data) if '醫院名稱' not in field_data['欄位名稱'] else None
        # field_data = extract_info_from_CCH(rs_ocr,field_data)
        field_data = self.extract_hospital_name(rs_ocr, field_data)
        field_data = self.extract_column_json(rs_ocr, field_data)
        field_data = self.extract_column_customization(rs_ocr, field_data)
        return pd.DataFrame(field_data)

    def table_info(self, rs_ocr_range, field_data, dict4, ocr):
        rs_table = get_ocr_table_line_result(
            dict4, border=[0.43, 0.75], ocr=ocr)
        rs_table = replace_mark(rs_table)
        # rs = extract_column_from_CCH(rs_table)
        rs = self.extract_table_column_json(rs_table)
        return pd.concat([field_data, rs], axis=0)

    def check_if_details(self, rs_ocr):
        return False

    def detail_info(self, rs_ocr, field_data):
        pass

    def extract_column_json(self, text, field_data):
        with open('./receipt_uni/config/regex_CCH.txt', 'r') as f:
            field_regex_map = json.load(f)
        field_name_count = {}
        field_name_val = {}

        for field_name, regex_pattern in field_regex_map.items():

            match = re.search(regex_pattern, text)
            matches_dup = re.finditer(regex_pattern, text)

            if match is not None:
                field_data['欄位名稱'].append(field_name)
                field_data['ocr辨識結果'].append(match.group(1))
            # 檢查重複項目欄位
            for match_dup in matches_dup:
                if field_name not in field_name_count:
                    field_name_count[field_name] = 1
                    if is_numeric(match_dup.group(1)):
                        field_name_val[field_name] = int(match_dup.group(1))
                    else:
                        field_name_val[field_name] = match_dup.group(1)
                else:
                    field_name_count[field_name] += 1
                    if is_numeric(match_dup.group(1)):
                        num = int(match_dup.group(1))
                        field_name_val[field_name] += num
                    else:
                        field_name_val[field_name] = match_dup.group(1)
            if field_name_count.get(field_name, 0) > 1:
                field_data['ocr辨識結果'][-1] = str(field_name_val[field_name])
        return field_data

    def extract_column_customization(self, text, field_data):
        return extract_info_from_CCH(text, field_data)

    def extract_table_column_json(self, text):
        field_data = {'欄位名稱': [], 'ocr辨識結果': []}
        with open('./receipt_uni/config/regex_CCH_table.txt', 'r') as f:
            field_regex_map = json.load(f)
        return pd.DataFrame(
            update_dict_with_regex_pattern(
                text, field_data, field_regex_map))

    def extract_hospital_name(self, text, field_data):
        if '醫院名稱' not in field_data['欄位名稱']:
            return hospital_info_from_CCH(text[:50], field_data)
        else:
            return field_data


class CMH_Pipeline(HospitalPipeline):

    def crop_from_label(self, img, yolo_stage2, opt, key, thr=0.45):
        label2 = detect(im0s=img, model=yolo_stage2, opt=opt)
        dict4 = crop_image_from_label_stage2(img, label2, key, thr=0.45)
        return dict4

    def preprocess_data(self, rs_ocr):
        return rs_ocr

    def text_info(self, rs_ocr, field_data):
        hospital_info_from_CMH(
            rs_ocr[:50], field_data) if '醫院名稱' not in field_data['欄位名稱'] else None
        extract_info_from_CMH(rs_ocr, field_data)
        return x_df

    def table_info(self, rs_ocr_range, field_data, dict4, ocr):
        rs_table = get_ocr_table_line_result(
            dict4, border=[0.48, 0.75], ocr=ocr)
        rs_table = replace_mark(rs_table)
        # print('rs_table=',rs_table)
        rs = extract_column_from_CMH(rs_table)
        return pd.concat([field_data, rs], axis=0)

    def check_if_details(self, rs_ocr):
        return False

    def detail_info(self, rs_ocr, field_data):
        pass


class TVGH_Pipeline(HospitalPipeline):
    def crop_from_label(self, img, yolo_stage2, opt, key, thr=0.45):
        pass

    def preprocess_data(self, rs_ocr):
        return rs_ocr

    def text_info(self, rs_ocr, field_data):
        hospital_info_from_TVGH(
            rs_ocr[:50], field_data) if '醫院名稱' not in field_data['欄位名稱'] else None
        border_rs = get_ocr_sentence_border_result(
            img, ocr, border=0.45, comparison=1)
        extract_column_from_TVGH(border_rs, field_data)
        extract_info_from_TVGH(rs_ocr, field_data)
        return pd.DataFrame(field_data)

    def table_info(self, rs_ocr_range, field_data, dict4, ocr):
        return field_data

    def check_if_details(self, rs_ocr):
        return False

    def detail_info(self, rs_ocr, field_data):
        pass


class KVGH_Pipeline(HospitalPipeline):
    def crop_from_label(self, img, yolo_stage2, opt, key, thr=0.45):
        pass

    def preprocess_data(self, rs_ocr):
        return re.sub('[a-zA-Z]', '', rs_ocr)

    def text_info(self, rs_ocr, field_data):
        hospital_info_from_KVGH(
            rs_ocr, field_data) if '醫院名稱' not in field_data['欄位名稱'] else None
        extract_sect_from_KVGH(rs_ocr, field_data)
        if check_type_KVGH(rs_ocr) == 'A':
            border_rs = get_ocr_sentence_border_result(
                img, ocr, border=0.5, comparison=0)
            index = border_rs.find("合計")
            if index != -1:
                border_rs_range = border_rs[:index]
                extract_column_from_KVGH(
                    border_rs_range.replace(
                        '/', ''), field_data)
            else:
                extract_column_from_KVGH(
                    border_rs.replace(
                        '/', ''), field_data)
            extract_info_from_KVGH(rs_ocr, field_data, type='A')
        else:
            border_rs = get_ocr_sentence_bi_border_result(
                img, ocr, left=0.25, right=0.63)
            border_rs_range = re.sub('[a-zA-Z]', '', border_rs)
            x = extract_column_from_KVGH(border_rs_range, field_data)
            y = extract_info_from_KVGH(rs_ocr, field_data, type='B')
        return pd.DataFrame(field_data)

    def table_info(self, rs_ocr_range, field_data, dict4, ocr):
        return field_data

    def check_if_details(self, rs_ocr):
        return False

    def detail_info(self, rs_ocr, field_data):
        pass


class NCKU_Pipeline(HospitalPipeline):
    def crop_from_label(self, img, yolo_stage2, opt, key, thr=0.45):
        pass

    def preprocess_data(self, rs_ocr):
        return re.sub('[a-zA-Z]', '', rs_ocr)

    def text_info(self, rs_ocr, field_data):
        hospital_info_from_NCKU(
            rs_ocr[:50], field_data) if '醫院名稱' not in field_data['欄位名稱'] else None
        x = during_hos_from_text_NCKU(rs_ocr_range, field_data)
        y = extract_info_from_NCKU(rs_ocr_range, field_data)
        w = depaerment_from_text_NCKU(rs_ocr, field_data)
        z = date_info_from_text_NCKU(rs_ocr, field_data)
        return pd.DataFrame(field_data)

    def table_info(self, rs_ocr_range, field_data, dict4, ocr):
        return field_data

    def check_if_details(self, rs_ocr):
        return False

    def detail_info(self, rs_ocr, field_data):
        pass


class ChiMei_Pipeline(HospitalPipeline):
    def crop_from_label(self, img, yolo_stage2, opt, key, thr=0.45):
        pass

    def preprocess_data(self, rs_ocr):
        return re.sub('[a-zA-Z]', '', rs_ocr)

    def text_info(self, rs_ocr, field_data):
        hospital_info_from_ChiMei(
            rs_ocr, field_data) if '醫院名稱' not in field_data['欄位名稱'] else None
        border_rs = get_ocr_sentence_bi_border_result(
            img, ocr, left=0.4, right=0.78)
        border_rs_range = re.sub('[a-zA-Z]', '', border_rs)
        x = extract_column_from_ChiMei(border_rs_range, field_data)
        y = extract_info_from_ChiMei(rs_ocr_range, field_data)
        return pd.DataFrame(field_data)

    def table_info(self, rs_ocr_range, field_data, dict4, ocr):
        return field_data

    def check_if_details(self, rs_ocr):
        return False

    def detail_info(self, rs_ocr, field_data):
        pass


class TCGH_Pipeline(HospitalPipeline):
    def crop_from_label(self, img, yolo_stage2, opt, key, thr=0.45):
        pass

    def preprocess_data(self, rs_ocr):
        return rs_ocr

    def text_info(self, rs_ocr, field_data):
        decimal_receipt_pattern = re.compile(r'繳\s*費\s*\證\s*明')
        decimal_match = re.search(decimal_receipt_pattern, rs_ocr)
        is_decimal = bool(decimal_match)
        label2 = detect(im0s=img, model=yolo_stage2, opt=opt)
        dict4 = crop_image_from_label_stage2(img, label2, key, thr=0.45)
        hospital_info_from_TCGH(
            rs_ocr[:50], field_data) if '醫院名稱' not in field_data['欄位名稱'] else None
        extract_info_from_TCGH(rs_ocr, field_data)
        if '門診醫療' in rs_ocr:
            rs_table = get_ocr_table_line_result(
                dict4, border=[0.19, 0.49], ocr=ocr)
        else:
            rs_table = get_ocr_table_line_result(
                dict4, border=[0.43, 0.77], ocr=ocr)
        rs_table = replace_mark(rs_table)
        rs = extract_column_from_TCGH(rs_table, is_decimal)
        exist = '合計' in rs['欄位名稱'].values
        if exist:
            index_of_total_amount = rs[rs['欄位名稱'] == '合計'].index[0]
            total_amount = rs['ocr辨識結果'][index_of_total_amount]
            if '總金額' not in field_data['欄位名稱']:
                field_data['欄位名稱'].append('總金額')
                field_data['ocr辨識結果'].append(total_amount)
            else:
                index_of_total_amount_field_data = field_data['欄位名稱'].index(
                    '總金額')
                field_data['ocr辨識結果'][index_of_total_amount_field_data] = total_amount
            rs.drop(rs[rs['欄位名稱'] == '合計'].index, inplace=True)
            # combined_df = pd.DataFrame(x)
        x_df = pd.DataFrame(field_data)
        combined_df = pd.concat([x_df, rs], axis=0)
        return pd.DataFrame(combined_df)

    def table_info(self, rs_ocr_range, field_data, dict4, ocr):
        return field_data

    def check_if_details(self, rs_ocr):
        return False

    def detail_info(self, rs_ocr, field_data):
        pass


class TCGH_puli_Pipeline(HospitalPipeline):
    def crop_from_label(self, img, yolo_stage2, opt, key, thr=0.45):
        pass

    def preprocess_data(self, rs_ocr):
        return rs_ocr

    def text_info(self, rs_ocr, field_data):
        hospital_info_from_TCGH_puli(
            rs_ocr[:50], field_data) if '醫院名稱' not in field_data['欄位名稱'] else None
        border_rs = get_ocr_sentence_border_result(
            img, ocr, border=0.45, comparison=1)
        x = extract_column_from_TCGH_puli(border_rs, field_data)
        y = extract_info_from_TCGH_puli(rs_ocr, field_data)
        return pd.DataFrame(field_data)

    def table_info(self, rs_ocr_range, field_data, dict4, ocr):
        return field_data

    def check_if_details(self, rs_ocr):
        return False

    def detail_info(self, rs_ocr, field_data):
        pass


hospital_key = {
    'Others': Others_Pipeline,
    'NTU': NTU_Pipeline,
    'CCH': CCH_Pipeline,
    'CG': CG_Pipeline,
    'CMH': CMH_Pipeline,
    'TVGH': TVGH_Pipeline,
    'TCGH': TCGH_Pipeline,
    'TCGH_puli': TCGH_puli_Pipeline,
    'KVGH': KVGH_Pipeline,
    # 'NCKU':NCKU_pipeline,
    'ChiMei': ChiMei_Pipeline,
    # 'PTVH':PTVH_pipeline
}


def select_key(key: str) -> callable:
    """
    Select and return the function corresponding to the given key.

    Args:
        key (str): The key used to select the function.

    Yields:
        Callable: The selected function.
    """
    return hospital_key.get(key)()


def select_pipeline(
        field_data: dict,
        key: str,
        img,
        ocr,
        yolo_stage2,
        opt) -> callable:
    """
    Select and process the pipeline based on the key.

    Args:
        field_data (dict): The dictionary containing field data.
        key (str): The key used to select the pipeline.
        img: The input image.
        rs_ocr (str): The OCR result string.
        ocr: The OCR model.
        yolo_stage2: The YOLO stage 2 model.
        opt: Additional options.

    Yields:
        Callable: The selected function.
    """
    pipeline = select_key(key)
    return process_pipeline(
        pipeline,
        field_data,
        key,
        img,
        ocr,
        yolo_stage2,
        opt)


def process_pipeline(
        pipeline,
        field_data: dict,
        key: str,
        img,
        ocr,
        yolo_stage2,
        opt) -> pd.DataFrame:
    """
    Process the selected pipeline.

    Args:
        pipeline: The selected pipeline object.
        field_data (dict): The dictionary containing field data.
        key (str): The key used to select the pipeline.
        img: The input image.
        ocr: The OCR model.
        yolo_stage2: The YOLO stage 2 model.
        opt: Additional options.

    Yields:
        pd.DataFrame: The updated field data DataFrame.
    """
    rs_ocr = pipeline.get_ocr_result(img, ocr)
    if pipeline.check_if_details(rs_ocr):
        return pipeline.detail_info(rs_ocr, field_data)
    dict4 = pipeline.crop_from_label(img, yolo_stage2, opt, key)
    rs_ocr_range = pipeline.preprocess_data(rs_ocr)
    field_data = pipeline.text_info(rs_ocr_range, field_data)
    field_data = pipeline.table_info(rs_ocr_range, field_data, dict4, ocr)
    return field_data
