import re
# import pandas as pd

# def extract_info_from_NTU(text,field_data):
#     """
#     extract information from NTU ocr result
#     Args:
#         - text (str): ocr result
#         - field_data: DataFrame
#     Yields:
    
#     """
#     # Define regular expressions to extract the data
#     field_regex_map = {
#         # '事故者姓名': r'姓名([^ ]+)',
#         '社保身份': r'[射身]份\s*([^ ]+)',
#         '就診科別': r'[科]?[別剔][:：]?\s*([^ ]+)',
#         '補助金額':r'補助[金全]額\s*[\u4e00-\u9fff]?\w*(\d+)',
#         # '優待金額':r'優待[金全]額\s*[\u4e00-\u9fff]?\w*?(\d+)'
#     }
#     for field_name, regex_pattern in field_regex_map.items():
#         match = re.search(regex_pattern, text)
#         if match is not None:
#             field_data['欄位名稱'].append(field_name)
#             if field_name in ['社保身份','就診科別']:
#                 field_data['ocr辨識結果'].append(match.group(1))
#             else:
#                 field_data['ocr辨識結果'].append(str(int(match.group(1))))
#     date_range_pattern = r'醫日期[:：、‧]?\s*(\d{4}/\d{2}/\d{2})[~-]?(\d{4}/\d{2}/\d{2})'
#     date_range_match = re.search(date_range_pattern, text)
#     outpatient_date_match = re.search(r'醫日\w*\s*(\d{4}/\d{2}/\d{2})',text)
#     # if outpatient_date_match:
#     #     field_data['欄位名稱'].append('就診日期')
#     #     field_data['ocr辨識結果'].append(outpatient_date_match.group(1))
#     date_matches = re.findall(r'(20\d{2}/\d{2}/\d{2})',text)
#     amount_match = re.search(r'NT\$(\d+)',text)
#     amount_match2 = re.search(r'[總聰急][金全]?額\s*[,：:。;；,、]?\s*(\d+)',text)
#     if amount_match and amount_match2 and (int(amount_match.group(1)) == int(amount_match2.group(1))):
#         field_data['欄位名稱'].append('總金額')
#         field_data['ocr辨識結果'].append(str(int(amount_match.group(1))))
#     elif amount_match:
#         field_data['欄位名稱'].append('總金額')
#         field_data['ocr辨識結果'].append(str(int(amount_match.group(1))))
#     elif amount_match2:
#         field_data['欄位名稱'].append('總金額')
#         field_data['ocr辨識結果'].append(str(int(amount_match2.group(1))))
        
#     if date_range_match:
#         field_data['欄位名稱'].append('住院起日')
#         field_data['ocr辨識結果'].append(date_range_match.group(1))
#         field_data['欄位名稱'].append('住院迄日')
#         field_data['ocr辨識結果'].append(date_range_match.group(2))
#     elif date_matches and len(date_matches)>=2:
#         field_data['欄位名稱'].append('住院起日')
#         field_data['ocr辨識結果'].append(date_matches[0])
#         field_data['欄位名稱'].append('住院迄日')
#         field_data['ocr辨識結果'].append(date_matches[1])
#     return pd.DataFrame(field_data)

def extract_column_custom_NTU(text,field_data):
    date_range_pattern = r'醫日期[:：、‧]?\s*(\d{4}/\d{2}/\d{2})[~-]?(\d{4}/\d{2}/\d{2})'
    date_range_match = re.search(date_range_pattern, text)
    outpatient_date_match = re.search(r'醫日\w*\s*(\d{4}/\d{2}/\d{2})',text)
    # if outpatient_date_match:
    #     field_data['欄位名稱'].append('就診日期')
    #     field_data['ocr辨識結果'].append(outpatient_date_match.group(1))
    date_matches = re.findall(r'(20\d{2}/\d{2}/\d{2})',text)
    amount_match = re.search(r'NT\$(\d+)',text)
    amount_match2 = re.search(r'[總聰急][金全]?額\s*[,：:。;；,、]?\s*(\d+)',text)
    if amount_match and amount_match2 and (int(amount_match.group(1)) == int(amount_match2.group(1))):
        field_data['欄位名稱'].append('總金額')
        field_data['ocr辨識結果'].append(str(int(amount_match.group(1))))
    elif amount_match:
        field_data['欄位名稱'].append('總金額')
        field_data['ocr辨識結果'].append(str(int(amount_match.group(1))))
    elif amount_match2:
        field_data['欄位名稱'].append('總金額')
        field_data['ocr辨識結果'].append(str(int(amount_match2.group(1))))
        
    if date_range_match:
        field_data['欄位名稱'].append('住院起日')
        field_data['ocr辨識結果'].append(date_range_match.group(1))
        field_data['欄位名稱'].append('住院迄日')
        field_data['ocr辨識結果'].append(date_range_match.group(2))
    elif date_matches and len(date_matches)>=2:
        field_data['欄位名稱'].append('住院起日')
        field_data['ocr辨識結果'].append(date_matches[0])
        field_data['欄位名稱'].append('住院迄日')
        field_data['ocr辨識結果'].append(date_matches[1])
    return field_data

# def extract_column_from_NTU(text):
#     """
#     defind regex map for normal receipt and self-payment receipt.

#     Args:
#         - text (str): ocr result
#     Yields:
    
#     """
#     field_data = {'欄位名稱':[],'ocr辨識結果':[]}
#     field_regex_map = {
#         # '事故者姓名': r'[姓 ]?名([^ ]+)',
#         # '病歷號': r'病[ ]?歷[ ]?號([^ ]+)',
#         '藥費': r'[^\u4e00-\u9fff]*[藥樂鍊桑][費賣炎]\w*\s*([-]?\d+)',
#         '治療處置費': r'[^\u4e00-\u9fff]*治[療瘀][處率]\w*\s*([-]?\d+)',
#         '手術費': r'[^\u4e00-\u9fff]*手術\w*\s*([-]?\d+)',
#         '材料費': r'[^\u4e00-\u9fff]*[材牙][料斜射科]\w*\s*([-]?\d+)',
#         '放射線診療費': r'[^\u4e00-\u9fff]*放[射料斜科]線\w*\s*([-]?\d+)',
#         '麻醉技術費': r'[^\u4e00-\u9fff]*麻醉技\w*\s*([-]?\d+)',
#         '檢查檢驗費': r'[^\u4e00-\u9fff]*檢查檢\w*\s*([-]?\d+)',
#         '證明書費': r'[^\u4e00-\u9fff]*[証正證輛][明萌盟]書\w*\s*([-]?\d+)',
#         '放射　化學　其他治療費': r'[^\u4e00-\u9fff]*放[射料斜科][/7]?化學[/7]?其他治療\w*\s*([-]?\d+)',
#         '血液費': r'[^\u4e00-\u9fff]*血[夜液]\w*\s*([-]?\d+)',
#         '病房費': r'[^\u4e00-\u9fff]*病房\w*\s*([-]?\d+)',
#         'ＩＣＵ病房費': r'[^\u4e00-\u9fff]*[IＩ][ ]?[CＣ][ ]?[UＵ]病房[費]?\w*\s*([-]?\d+)',
#         '診察費': r'[^\u4e00-\u9fff]*診察\w*\s*([-]?\d+)',
#         '護理費': r'[^\u4e00-\u9fff]*[護菱設]理\w*\s*([-]?\d+)',
#         '管灌膳食費': r'[^\u4e00-\u9fff]*管灌[膳曠醫賤][食養]\w*\s*([-]?\d+)',
#         '掛號費': r'[^\u4e00-\u9fff]*掛號\w*\s*([-]?\d+)',
#         '藥事服務費': r'[^\u4e00-\u9fff]*[藥樂鍊桑]事服\w*\s*([-]?\d+)',
#         '牙科治療處置費': r'[^\u4e00-\u9fff]*牙科治療處置\w*\s*([-]?\d+)',
#         '治療儀器及設施使用':r'[^\u4e00-\u9fff]*治療儀器\w*\s*([-]?\d+)',
#         '基本部分負擔（代收）': r'[^\u4e00-\u9fff]*基本部\w*\s*(\d+)',
#         '藥品部分負擔（代收）': r'[^\u4e00-\u9fff]*藥品部\w*\s*(\d+)',
#     }
#     field_part_regex_map = {
#         '藥費部份負擔': r'[^\u4e00-\u9fff]*[藥樂鍊桑][費賣炎]\w*\s*(\d+)',
#         '治療處置費部份負擔': r'[^\u4e00-\u9fff]*治[療瘀][處率]\w*\s*(\d+)',
#         '手術費部份負擔': r'[^\u4e00-\u9fff]*手術\w*\s*(\d+)',
#         '材料費部份負擔': r'[^\u4e00-\u9fff]*[材牙][射料斜科]\w*\s*(\d+)',
#         '放射線診療費部份負': r'[^\u4e00-\u9fff]*放[射料斜科]線\w*\s*(\d+)',
#         '麻醉技術費部份負擔': r'[^\u4e00-\u9fff]*麻醉技\w*\s*(\d+)',
#         '檢查檢驗費部份負擔': r'[^\u4e00-\u9fff]*檢[查奪]檢驗\w*\s*(\d+)',
#         '證明書費部份負擔': r'[^\u4e00-\u9fff]*[証正][明萌]書\w*\s*(\d+)',
#         '放射　化學　其他治療費部份負擔': r'[^\u4e00-\u9fff]*放[射料斜科][/7]?化學[/7]?其他\w*\s*(\d+)',
#         '血液費部份負擔': r'[^\u4e00-\u9fff]*血[液夜]\w*\s*(\d+)',
#         '病房費部份負擔': r'[^\u4e00-\u9fff]*病[房穿]\w*\s*(\d+)',
#         'ＩＣＵ病房費部份負': r'[^\u4e00-\u9fff]*[IＩ][ ]?[CＣ][ ]?[UＵ]病房\w*\s* (\d+)',
#         '診察費部份負擔': r'[^\u4e00-\u9fff]*診察\w*\s*(\d+)',
#         '護理費部份負擔': r'[^\u4e00-\u9fff]*[護菱設]理\w*\s*(\d+)',
#         '管灌膳食費部份負擔': r'[^\u4e00-\u9fff]*管灌[膳曠醫賤][食養]\w*\s*(\d+)',
#         '藥事服務費部份負擔': r'[^\u4e00-\u9fff]*[藥樂鍊桑]事服\w*\s*(\d+)',
#         '牙科治療處置費部份負擔': r'[^\u4e00-\u9fff]*牙科治療處置\w*\s*(\d+)',
#     }
    
#     index = text.find('部份負擔')
#     ex_index = text.find('基本部分負擔')
#     if index !=-1:
#         if ex_index !=-1:
#             field_data=df_fill_in(text,field_data,field_regex_map)
#         else:
#             field_data=df_fill_in(text,field_data,field_part_regex_map)
#     else:
#         field_data=df_fill_in(text,field_data,field_regex_map)
#     # return field_data
#     new_df = pd.DataFrame(field_data)
#     return new_df
        
# def df_fill_in(text: str,field_data,regex_map: dict):
#     """
#     find regex_pattern in text and fill in DataFrame

#     Args:
#         - text (str): ocr result
#         - field_data: DataFrame
#         - regex_map: dictionary of words matching a regex
#     Yields:
    
#     """
#     for field_name, regex_pattern in regex_map.items():
#         match = re.search(regex_pattern, text)
#         if match is not None:
#             field_data['欄位名稱'].append(field_name)
#             field_data['ocr辨識結果'].append(match.group(1))
#     return field_data



