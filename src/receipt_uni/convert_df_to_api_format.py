import re
import numpy as np
import pandas as pd
import os


def convert_df_to_api_format(rs: pd.DataFrame) -> dict:
    """
    Convert DataFrame to API format dictionary.

    Args:
        rs (pd.DataFrame): DataFrame for OCR results.

    Returns:
        The dict for api.
    """
    result_dic = {}
    rs = rs.T
    rs = rs.reset_index(drop=True)
    rs.columns = rs.iloc[0]
    rs = rs[1:].reset_index(drop=True)
    nhi = 'N' if re.search('自費|民眾', get_value(rs, '社保身份')) else 'Y'
    result_dic['nhi'] = nhi
    result_dic['admissionDate'] = get_value(rs, '住院起日')
    result_dic['dischargeDate'] = get_value(rs, '住院迄日')
    result_dic['hospitalName'] = get_value(rs, '醫院名稱')
    result_dic['dept'] = get_value(rs, '就診科別')
    result_dic['receivedAmount'] = get_value(rs, '總金額')
    column_list = list(rs.columns)
    for i in ['身分證號', '姓名', '社保身份', '住院起日', '住院迄日', '醫院名稱', '就診科別', '總金額']:
        if i in column_list:
            column_list.remove(i)
    rs = rs[column_list]
    if not rs.empty:
        item = rs.to_dict(orient='records')[0]
        check_and_convert(item)
        result_dic['items'] = item
    else:
        result_dic['items'] = {'項目名稱': '0'}
    return result_dic


def check_and_convert(item: list) -> list:
    """
    Check if the type is str. If not, convert it to str.

    Args:
        item (list): The input list to be checked and converted.

    Returns:
        list: The modified list where non-str elements are converted to str.
    """
    for key, value in item.items():
        if not isinstance(value, str):
            if isinstance(value, (np.float32, np.float64, float)):
                item[key] = str(value)
            elif isinstance(value, (np.int32, np.int64, int)):
                item[key] = str(value)
            else:
                raise TypeError(f"{key} 的值 {value} 不是 str 型態")
    return item


def get_value(rs: list, columns: str) -> str:
    """
    Get columns value.

    Args:
        - rs: All of the coolumns.
        - columns: The column name.
    Yields:
        The precessed text.
    """
    try:
        return rs[columns][0]
    except BaseException:
        return ''


def replace_mark(text: str) -> str:
    """
    Replacement of special symbols.

    Args:
        - text: The input text.

    Yields:
        The precessed text.
    """
    str = re.sub('[：:。；;,、{}\\[\\]﹝﹞★‧【】…！!·*「，>\'\\#＊?<"\\%ˋ()@.]', '', text)
    return str


def transfer_date(input_date_str: str) -> str:
    """
    Transfer the date of ROC to the date of the West.

    Args:
        - input_date_str: The input text.

    Yields:
        The date of the West.
    """
    year = int(input_date_str[:3]) + 1911
    month = int(input_date_str[4:6])
    day = int(input_date_str[7:9])
    output_date_str = "{:04d}/{:02d}/{:02d}".format(year, month, day)
    return output_date_str


def update_dict_with_regex_pattern(
        text: str,
        field_data: pd.DataFrame,
        regex_map: dict) -> dict:
    """
    Find regex patterns in text and fill in DataFrame.

    Args:
        text (str): OCR result.
        field_data (pd.DataFrame): DataFrame to fill in.
        regex_map (dict): Dictionary of words matching a regex pattern.

    Yields:
        dict: Updated dictionary.
    """
    for field_name, regex_pattern in regex_map.items():
        match = re.search(regex_pattern, text)
        if match is not None:
            field_data['欄位名稱'].append(field_name)
            field_data['ocr辨識結果'].append(match.group(1))
    return field_data


def generate_json_result(datafame, img) -> str:
    """
    Generate a JSON result based on the provided DataFrame and image path.

    Args:
        datafame (pd.DataFrame): DataFrame containing OCR recognition results.
        img (str): Path to the image.

    Returns:
        str: JSON result containing recognition information.
    """
    mask1 = (datafame["ocr辨識結果"] != '0') & \
            (datafame["ocr辨識結果"] != '00') & \
            (datafame["ocr辨識結果"] != '')
    datafame_filtered = datafame[mask1]
    result_dic = convert_df_to_api_format(rs=datafame_filtered)
    result = {"returnCode": 0, "result": result_dic}
    i_base = os.path.basename(img)
    print('"' + i_base + '"', ':', result_dic, ',')
    return result
