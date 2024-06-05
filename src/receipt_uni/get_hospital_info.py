import re
import json


def get_hospital_key(rs_ocr: str, config) -> str:
    """
    Give the key according to the name of the hospital.

    Args:
        - rs_ocr (list): the ocr results 

    Yields:
        A key representing the hospital
    """
    with open(config, 'r') as f:
        hospital_dict = json.load(f)
    rs_ocr = rs_ocr.replace(" ", "")
    for term, key in hospital_dict.items():
        if term in rs_ocr:
            return key
    return 'Others'


def get_hospital_key_api(hospCode: str, field_data: dict, config: str, store: int=0) -> str:
    """
    Get the key corresponding to the hospital name passed via API.

    Args:
        hospCode (str): Hospital code.
        field_data (dict): Field data.
        config (str): Path to the hospital code configuration file.
        store (int, optional): Store flag. Defaults to 0.

    Returns:
        str: Key representing the hospital.
    """
    with open(config, 'r') as f:
        hospital_map = json.load(f)
    for hospital_name, hospital_code in hospital_map.items():
        if hospital_code[0] == hospCode:
            if store == 1:
                field_data['欄位名稱'].append('醫院名稱')
                field_data['ocr辨識結果'].append(hospital_name)
            return hospital_code[1]
    return 'NULL'


def compare_hospital_key(key_ocr, ocr_conf, key_input, hospCode, field_data):
    """
    Compare the OCR result key with the key passed by the API.

    Args:
        key_ocr (str): Key extracted from OCR.
        ocr_conf (float): Confidence score of the OCR result.
        key_input (str): Key passed by the API.
        hospCode (str): Hospital code.
        field_data (dict): Field data.

    Returns:
        str: The final key chosen after comparison.
    """
    if key_ocr is not None and ocr_conf >= 0.9:
        key = key_ocr
    elif (key_ocr is None and key_input is not None) or ocr_conf < 0.9:
        key = key_input
        get_hospital_key_api(hospCode, field_data, store=1)
    else:
        key = key_ocr
    return key


def hospital_info_from_CCH(text, field_data):
    """
    Get detailed name of CCH
    """
    hospital_regex_map = {
        '彰化基督教醫療財團法人漢銘基督教醫院': r'[漢漠][銘鉻]',
        '彰化基督教醫療財團法人二林基督教醫院': r'[二2]\s*林',
        '彰化基督教醫療財團法人南投基督教醫院': r'南投',
        '彰化基督教醫療財團法人雲林基督教醫院': r'雲林',
        '彰化基督教醫療財團法人鹿港基督教醫院': r'[塵鹿]?[港巷卷弮]|LUKANG',
        '彰化基督教醫療財團法人員林基督教醫院': r'[員賣]林',
        '彰化基督教醫療財團法人彰化基督教兒童醫院': r'兒童',
        '彰化基督教醫療財團法人彰化基督教醫院': r'[彰]?[化花]?',
    }
    for hospital_name, key in hospital_regex_map.items():
        if re.search(key, text):
            field_data['欄位名稱'].append('醫院名稱')
            field_data['ocr辨識結果'].append(hospital_name)
            break  # 如果找到匹配的醫院名稱，停止搜索
    return field_data


def hospital_info_from_NTU(text, field_data):
    """
    Get detailed name of NTU
    """
    hospital_regex_map = {
        '國立臺灣大學醫學院附設醫院新竹臺大分院生醫醫院': r'生[醫醬]?',
        '國立臺灣大學醫學院附設醫院新竹臺大分院新竹醫院': r'新竹',
        '國立臺灣大學醫學院附設醫院竹東分院': r'竹東',
        '國立臺灣大學醫學院附設醫院雲林分院': r'雲林',
        '國立臺灣大學醫學院附設醫院癌醫中心分院': r'院癌',
        '國立臺灣大學醫學院附設醫院北護分院': r'北護',
        '國立臺灣大學醫學院附設醫院金山分院': r'金山',
        '國立臺灣大學醫學院附設醫院兒童醫院': r'兒童',
        '國立臺灣大學醫學院附設醫院': r'[臺]?[灣]?'
    }
    
    for hospital_name, key in hospital_regex_map.items():
        if re.search(key, text):
            field_data['欄位名稱'].append('醫院名稱')
            field_data['ocr辨識結果'].append(hospital_name)
            break  # 如果找到匹配的醫院名稱，停止搜索
    return field_data


def hospital_info_from_CG(text, field_data):
    """
    Get detailed name of CG
    """
    hospital_regex_map = {
        '長庚醫療財團法人高雄長庚紀念醫院': r'高[雄]?',
        '長庚醫療財團法人嘉義長庚紀念醫院': r'嘉[義識]?',
        '長庚醫療財團法人桃園長庚紀念醫院': r'桃園',
        '長庚醫療財團法人基隆長庚紀念醫院': r'基[隆墜障]?',
        '長庚醫療財團法人鳳山長庚紀念醫院': r'鳳山',
        '長庚醫療財團法人雲林長庚紀念醫院': r'雲林',
        '長庚醫療財團法人台北長庚紀念醫院': r'[台倉][北]?',
        '長庚醫療財團法人林口長庚紀念醫院': r'[林外]?[口仁]?|長庚'
    }
    for hospital_name, key in hospital_regex_map.items():
        if re.search(key, text):
            field_data['欄位名稱'].append('醫院名稱')
            field_data['ocr辨識結果'].append(hospital_name)
            break  # 如果找到匹配的醫院名稱，停止搜索
    return field_data


def hospital_info_from_CMH(text, field_data):
    """
    Get detailed name of CMH
    """
    hospital_regex_map = {
        '中國醫藥大學兒童醫院': r'兒[瑩童章壺壹董旁萱]?',
        '中國醫藥大學北港附設醫院': r'[北兆]港',
        '中國醫藥大學新竹附設醫院': r'新竹|[Ss]INC[NH]U',
        '中國醫藥大學附設醫院臺北分院': r'臺北',
        '中國醫藥大學附設醫院': r'[中]?[國]?'
    }
    for hospital_name, key in hospital_regex_map.items():
        if re.search(key, text):
            field_data['欄位名稱'].append('醫院名稱')
            field_data['ocr辨識結果'].append(hospital_name)
            break  # 如果找到匹配的醫院名稱，停止搜索
    return field_data


def hospital_info_from_TVGH(text, field_data):
    """
    Get detailed name of TVGH
    """
    hospital_regex_map = {
        '臺北榮民總醫院': r'[台臺]北',
    }
    for hospital_name, key in hospital_regex_map.items():
        if re.search(key, text):
            field_data['欄位名稱'].append('醫院名稱')
            field_data['ocr辨識結果'].append(hospital_name)
            break  # 如果找到匹配的醫院名稱，停止搜索
    return field_data


def hospital_info_from_KVGH(text, field_data):
    """
    Get detailed name of KVGH
    """
    hospital_regex_map = {
        '高雄榮民總醫院': r'高雄',
    }
    for hospital_name, key in hospital_regex_map.items():
        if re.search(key, text):
            field_data['欄位名稱'].append('醫院名稱')
            field_data['ocr辨識結果'].append(hospital_name)
            break  # 如果找到匹配的醫院名稱，停止搜索
    return field_data


def hospital_info_from_TCGH(text, field_data):
    """
    Get detailed name of TCGH
    """
    hospital_regex_map = {
        '臺中榮民總醫院': r'[臺宜]?[m]?\s*[中染][榮]?[民]?|[臺宜]?[r]?[m]?\s*榮民',
    }
    for hospital_name, key in hospital_regex_map.items():
        if re.search(key, text):
            field_data['欄位名稱'].append('醫院名稱')
            field_data['ocr辨識結果'].append(hospital_name)
            break  # 如果找到匹配的醫院名稱，停止搜索
    return field_data


def hospital_info_from_TCGH_puli(text, field_data):
    """
    Get detailed name of TCGH
    """
    hospital_regex_map = {
        '臺中榮總埔里分院': r'埔里|臺中榮總埔?里',
    }
    for hospital_name, key in hospital_regex_map.items():
        if re.search(key, text):
            field_data['欄位名稱'].append('醫院名稱')
            field_data['ocr辨識結果'].append(hospital_name)
            break  # 如果找到匹配的醫院名稱，停止搜索
    return field_data


def hospital_info_from_KMU(text, field_data):
    """
    Get detailed name of KMU
    """
    hospital_regex_map = {
        '高雄市立大同醫院': r'大同',
    }
    for hospital_name, key in hospital_regex_map.items():
        if re.search(key, text):
            field_data['欄位名稱'].append('醫院名稱')
            field_data['ocr辨識結果'].append(hospital_name)
            break  # 如果找到匹配的醫院名稱，停止搜索
    return field_data


def hospital_info_from_NCKU(text, field_data):
    """
    Get detailed name of NCKU
    """
    hospital_regex_map = {
        '國立成功大學醫學院附設醫院': r'成功',
    }
    for hospital_name, key in hospital_regex_map.items():
        if re.search(key, text):
            field_data['欄位名稱'].append('醫院名稱')
            field_data['ocr辨識結果'].append(hospital_name)
            break  # 如果找到匹配的醫院名稱，停止搜索
    return field_data


def hospital_info_from_ChiMei(text, field_data):
    """
    Get detailed name of ChiMei
    """
    hospital_regex_map = {
        '奇美醫療財團法人柳營奇美醫院': r'柳營|Liouying',
        '奇美醫療財團法人佳里奇美醫院': r'佳里|Chiali',
        '奇美醫療財團法人奇美醫院': r'[奇]?',
    }
    for hospital_name, key in hospital_regex_map.items():
        if re.search(key, text):
            field_data['欄位名稱'].append('醫院名稱')
            field_data['ocr辨識結果'].append(hospital_name)
            break  # 如果找到匹配的醫院名稱，停止搜索
    return field_data