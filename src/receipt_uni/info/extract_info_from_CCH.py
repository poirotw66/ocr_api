import re
import pandas as pd
def is_numeric(input_str):
    return input_str.isdigit()

def transfer_date(input_date_str):
    year = int(input_date_str[:3]) + 1911 
    month = int(input_date_str[4:6])
    day = int(input_date_str[7:9])
    output_date_str = "{:04d}/{:02d}/{:02d}".format(year, month, day)
    return output_date_str

def extract_info_from_CCH(text,field_data):
    # field_regex_map = {
    #     # '事故者姓名': r'姓名([^ ]+)',
    #     '社保身份': r'就[醫醬酉馨]?身份([^ ]+)',
    #     # '住院起日': r'[入人][院完玩]日[期其共]?\s*(\d{3}\s*/\s*\d{2}\s*/\s*\d{2})',
    #     # '住院迄日': r'[出日 ][院完玩]日[期其共]?[:：]?\s*(\d{3}\s*/\s*\d{2}\s*/\s*\d{2})',
    #     # '就診科別': r'院[科]?別\s*([^ ]+)',
    #     '住院門診預收':r'住院門診預收\s*[\u4e00-\u9fff]?\w*?(\d+)',
    #     '預存抵繳':r'預存抵繳\s*[\u4e00-\u9fff]?\w*?(\d+)',
    #     '已繳金額':r'已繳[金全]額\s*[\u4e00-\u9fff]?\w*?(\d+)',
    #     '已退金額':r'已退[金全]額\s*[\u4e00-\u9fff]?\w*?(\d+)',
    #     '保險金抵繳':r'保險[金全]抵繳\s*[\u4e00-\u9fff]?\w*?(\d+)',
    #     '保險金抵扣':r'保險[金全]抵扣\s*[\u4e00-\u9fff]?\w*?(\d+)',
    #     '振興券':r'振興券\s*[\u4e00-\u9fff]?\w*?(\d+)',
    #     '補助金額':r'補助[金全]額\s*[\u4e00-\u9fff]?\w*?(\d+)',
    #     # '優待金額':r'優待[金全]額\s*[\u4e00-\u9fff]?\w*?(\d+)',
    #     '預繳行動支付': r'[^\u4e00-\u9fff]*[預續]繳行動支付\s*(\d+)',
    #     '預繳醫指付': r'[^\u4e00-\u9fff]*[預續]繳醫\w*\s*(\d+)',
    #     '預繳信卡': r'[^\u4e00-\u9fff]*[預續]繳信\w*\s*(\d+)',
    #     '預繳現金': r'預[繳線]現[金全]\w*\s*(\d+)'
    # }

#     field_name_count = {}
#     field_name_val = {}
    
#     for field_name, regex_pattern in field_regex_map.items():
       
#         match = re.search(regex_pattern, text)
#         matches_dup = re.finditer(regex_pattern, text)
        
#         if match is not None:
#             field_data['欄位名稱'].append(field_name)
#             field_data['ocr辨識結果'].append(match.group(1))
#         #檢查重複項目欄位
#         for match_dup in matches_dup:
#             if field_name not in field_name_count:
#                 field_name_count[field_name] = 1
#                 if is_numeric(match_dup.group(1)):
#                     field_name_val[field_name] = int(match_dup.group(1))
#                 else:
#                     field_name_val[field_name] = match_dup.group(1)
#             else:
#                 field_name_count[field_name] += 1  
#                 if is_numeric(match_dup.group(1)):
#                     num  = int(match_dup.group(1))
#                     field_name_val[field_name]+=num
#                 else:
#                     field_name_val[field_name] = match_dup.group(1)
#         if field_name_count.get(field_name, 0) > 1:
#               field_data['ocr辨識結果'][-1] = str(field_name_val[field_name])
    dapart_a_match=re.search(r'院[科]?別\s*([^ ]+)',text)
    dapart_b_match=re.search(r'[醫醬酉馨][科]?別\s*([^ ]+)',text)
    if dapart_a_match:
        field_data['欄位名稱'].append('就診科別')
        field_data['ocr辨識結果'].append(dapart_a_match.group(1))
    elif dapart_b_match:
        field_data['欄位名稱'].append('就診科別')
        field_data['ocr辨識結果'].append(dapart_b_match.group(1))
    date_start_match=re.search(r'[入人][院完玩]日[期其共]?\s*(\d{3}\s*/\s*\d{2}\s*/\s*\d{2})',text)
    if date_start_match:
        field_data['欄位名稱'].append('住院起日')
        date_start=transfer_date(date_start_match.group(1))
        field_data['ocr辨識結果'].append(date_start)
        # field_data['ocr辨識結果'].append(date_start_match.group(1))
    date_end_match=re.search(r'[出日 ][院完玩]日[期其共]?[:：]?\s*(\d{3}\s*/\s*\d{2}\s*/\s*\d{2})',text)
    if date_end_match:
        field_data['欄位名稱'].append('住院迄日')
        date_end=transfer_date(date_end_match.group(1))
        field_data['ocr辨識結果'].append(date_end)
        # field_data['ocr辨識結果'].append(date_end_match.group(1))
    outpatient_date_match = re.search(r'就診日\w*\s*(\d{3}\s*/\s*\d{2}\s*/\s*\d{2})',text)
    if outpatient_date_match:
        field_data['欄位名稱'].append('就診日期')
        outpatient_date=transfer_date(outpatient_date_match.group(1))
        field_data['ocr辨識結果'].append(outpatient_date)
    reduce_match = re.search(r'優待金額\s*[\u4e00-\u9fff]*?\w*?(\d+)', text)
    total_cost_match =  re.search(r'費用總額\s*[\u4e00-\u9fff]?\w*?(\d+)', text)
    total_cost2_match =  re.search(r'繳納[金全]額\s*[\u4e00-\u9fff]?\w*?(\d+)', text)
    outpatient_cost_match = re.search(r'現[金全]繳\w*\s*(\d+)', text)
    outpatient_cost2_match = re.search(r'自付額\w*\s*(\d+)', text)
    if total_cost_match and reduce_match:
        charge = int(total_cost_match.group(1)) - int(reduce_match.group(1))
        if total_cost2_match:
            field_data['欄位名稱'].append('總金額')
            if int(total_cost2_match.group(1)) ==charge:
                field_data['ocr辨識結果'].append(charge)
            else:
                field_data['ocr辨識結果'].append(total_cost2_match.group(1))
    elif total_cost_match and total_cost2_match:
        field_data['欄位名稱'].append('總金額')
        if int(total_cost_match.group(1))== int(total_cost_match.group(1)):
            field_data['ocr辨識結果'].append(str(int(total_cost_match.group(1))))
        else:
            field_data['ocr辨識結果'].append(str(int(total_cost_match.group(1))))
    elif total_cost2_match:
        field_data['欄位名稱'].append('總金額')
        field_data['ocr辨識結果'].append(str(total_cost2_match.group(1)))
    elif outpatient_cost_match:
        field_data['欄位名稱'].append('總金額')
        field_data['ocr辨識結果'].append(str(outpatient_cost_match.group(1)))
    elif outpatient_cost2_match:
        field_data['欄位名稱'].append('總金額')
        field_data['ocr辨識結果'].append(str(outpatient_cost2_match.group(1)))
  
    return field_data

def extract_column_from_CCH(text):
    field_data = {'欄位名稱':[],'ocr辨識結果':[]}
    field_regex_map = {
        # '事故者姓名': r'[姓 ]?名([^ ]+)',
        # '病歷號': r'病[ ]?歷[ ]?號([^ ]+)',
        '手術費': r'[^\u4e00-\u9fff]*手術[費]? (\d+)',
        '麻醉費': r'[^\u4e00-\u9fff]*麻醉[費]? (\d+)',
        '治療處置費': r'[^\u4e00-\u9fff]*[治浴]療處置[費]? (\d+)',
        '病房費': r'[^\u4e00-\u9fff]*病房[費]? (\d+)',
        '放射線診察費': r'[^\u4e00-\u9fff]*放射線診察[費]? (\d+)',
        '診察費': r'[^\u4e00-\u9fff]*診察[費]? (\d+)',
        '注射技術費': r'[^\u4e00-\u9fff]*[注洋]射[技我]術[費]? (\d+)',
        '檢查費': r'[^\u4e00-\u9fff]*檢[查囊]\w*\s*(\d+)',
        '藥事服務費': r'[^\u4e00-\u9fff]*藥事服務[費]? (\d+)',
        '血液血漿費': r'[^\u4e00-\u9fff]*血[夜液]血漿[費]? (\d+)',
        '藥費': r'[^\u4e00-\u9fff]*[藥樂][費]? (\d+)',
        '材料費': r'[^\u4e00-\u9fff]*[材牙][料斜射科]\w*\s*([-]?\d+)',
        '膳食費': r'[^\u4e00-\u9fff]*[膳曠醫賤][食養][費]? (\d+)',
        '家屬膳食費': r'[^\u4e00-\u9fff]*[家蒙]屬[曠膳醫賤][食養][費]? (\d+)',
        '證明書費': r'[^\u4e00-\u9fff]*[証正證][明萌盟]\w*\s*(\d+)',
        '健保部份負擔明細': r'[^\u4e00-\u9fff]*[部爺][分芬努谷貓][負寬貧賁]\w*\s*(\d+)',
        '雜項收費': r'[^\u4e00-\u9fff]*雜項收[費]? (\d+)',
        '掛號費': r'[^\u4e00-\u9fff]*掛號[費]? (\d+)',
        '輔具費': r'[^\u4e00-\u9fff]*輔具[費]?\s*(\d+)',
        '暫繳款': r'[^\u4e00-\u9fff]*暫繳款?\s*(\d+)',
        '特別護士費': r'[^\u4e00-\u9fff]*特別護\w*\s*(\d+)',
        '救護車費': r'[^\u4e00-\u9fff]*救護\w*\s*(\d+)',
        '住院整合照護輔佐服務費': r'[^\u4e00-\u9fff]*住院整\w*\s*(\d+)'
    }
    for field_name, regex_pattern in field_regex_map.items():
        match = re.search(regex_pattern, text)
        if match is not None:
            field_data['欄位名稱'].append(field_name)
            field_data['ocr辨識結果'].append(match.group(1))
    new_df = pd.DataFrame(field_data)
    return new_df


