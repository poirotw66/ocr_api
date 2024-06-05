import re
from datetime import datetime

def extract_column_from_TVGH(text, field_data):
    field_regex_map = {
        # '事故者姓名': r'[姓 ]?名([^ ]+)',
        # '病歷號': r'病[ ]?歷[ ]?號([^ ]+)',
        '掛號費': r'[^\u4e00-\u9fff]*掛\s*號\w*\s*(\d+)',
        '診察費': r'[^\u4e00-\u9fff]*診察\w*\s*(\d+)',
        '藥費': r'[^\u4e00-\u9fff]*藥費\w*\s*(\d+)',
        '檢驗費': r'[^\u4e00-\u9fff]*檢[驗檢]\w*\s*(\d+)',
        'X光費': r'[^\u4e00-\u9fff]*X光\w*\s*(\d+)',
        '內檢費': r'[^\u4e00-\u9fff]*內檢\w*\s*(\d+)',
        '注射技術費': r'[^\u4e00-\u9fff]*注射技術\w*\s*(\d+)',
        '處理費': r'[^\u4e00-\u9fff]*處[理蓮]\w*\s*(\d+)',
        '材料費': r'[^\u4e00-\u9fff]*材料\w*\s*(\d+)',
        '特殊材料費': r'[^\u4e00-\u9fff]*特[殊辣]材料\w*\s*(\d+)',
        '物理治療費': r'[^\u4e00-\u9fff]*物理治\w*\s*(\d+)',
        '手術費': r'[^\u4e00-\u9fff]*手術\w*\s*(\d+)',
        '治療費': r'[^\u4e00-\u9fff]* 治療\w*\s*(\d+)',
        '麻醉費': r'[^\u4e00-\u9fff]*麻醉\w*\s*(\d+)',
        '血費': r'[^\u4e00-\u9fff]*[血無]費\w*\s*(\d+)',
        '體檢費': r'[^\u4e00-\u9fff]*體檢\w*\s*(\d+)',
        '放射治療費': r'[^\u4e00-\u9fff]*放射治療\w*\s*(\d+)',
        '人工腎臟費': r'[^\u4e00-\u9fff]*腎臟\w*\s*(\d+)',
        '牙科材料費': r'[^\u4e00-\u9fff]*[牙芽穿]科\w*\s*(\d+)',
        '假牙材料費': r'[^\u4e00-\u9fff]*假牙\w*\s*(\d+)',
        '矯正材料費': r'[^\u4e00-\u9fff]*矯[正追]\w*\s*(\d+)',
        '證書費': r'[^\u4e00-\u9fff]*證書\w*\s*(\d+)',
        '病房費': r'[^\u4e00-\u9fff]*病房\w*\s*(\d+)',
        '膳食費': r'[^\u4e00-\u9fff]*膳食\w*\s*(\d+)',
        '醫師費': r'[^\u4e00-\u9fff]*醫師費\s*(\d+)',
        '護理費': r'[^\u4e00-\u9fff]*護[理連]\w*\s*(\d+)',
        '接生費': r'[^\u4e00-\u9fff]*接生\w*\s*(\d+)',
        '嬰兒費': r'[^\u4e00-\u9fff]*嬰兒\w*\s*(\d+)',
        '雜項費': r'[^\u4e00-\u9fff]*雜項\w*\s*(\d+)',
        '藥師服務費': r'[^\u4e00-\u9fff]*[藥樂][師帥]服務\w*\s*(\d+)',
        '諮詢費': r'[^\u4e00-\u9fff]*諮詢\w*\s*(\d+)',
        '30天內部分負擔': r'[^\u4e00-\u9fff]*30天\w*\s*(\d+)',
        '31天-60天部分負擔': r'[^\u4e00-\u9fff]*31天-60\w*\s*(\d+)',
        '61天以上部分負擔': r'[^\u4e00-\u9fff]*61天\w*\s*(\d+)',
        
        '住院門診預收':r'住院門診\w*\s*(\d+)',
        '預存抵繳':r'預存\w*\s*(\d+)',
        '預繳金額':r'預繳[金全]額\w*\s*(\d+)',
        '預繳行動支付':r'預繳行動\w*\s*(\d+)',
        '預繳現金':r'預繳現[金全]\w*\s*(\d+)',
        '預繳醫指付':r'預繳醫\w*\s*(\d+)',
        '已繳金額':r'已繳[金全]額\w*\s*(\d+)',
        '繳納現金':r'繳納現[金全]\w*\s*(\d+)',
        # '信用卡':r'信用卡\w*\s*(\d+)',
        '已退金額':r'已退\w*\s*(\d+)',
        '保險金抵繳':r'保險[金全]抵繳\w*\s*(\d+)',
        '保險金抵扣':r'保險[金全]抵扣\w*\s*(\d+)',
        '振興券':r'振興券\w*\s*(\d+)',
        '補助金額':r'補助\w*\s*(\d+)',
        '優待金額':r'優待\w*\s*(\d+)',
        # '總金額':r'新[臺台][幣警]\s*(\d+)',
        # '社保身份':r'身分\s+(.+?)(?=\s+[\u4e00-\u9fa5]+|$)'
    }

    for field_name, regex_pattern in field_regex_map.items():
        match = re.search(regex_pattern, text)
        if match is not None:
            field_data['欄位名稱'].append(field_name)
            field_data['ocr辨識結果'].append(match.group(1))


def extract_info_from_TVGH(text,field_data):
    info_regex_map ={
        '總金額':r'新[臺台][幣警]\s*(\d+)',
        '就診科別':r'科\s*別\s+(\w+)',
        '社保身份':r'身分\s+(.+?)(?=\s+[\u4e00-\u9fa5]+|$)'
    }
    for field_name, regex_pattern in info_regex_map.items():
        match = re.search(regex_pattern, text)
        if match is not None:
            field_data['欄位名稱'].append(field_name)
            field_data['ocr辨識結果'].append(match.group(1))
            
    date_range_match = re.search(r'(\d{4}-\d{2}-\d{2})\s?[至]?\s?(\d{4}-\d{2}-\d{2})', text)
    date_matches = re.findall(r'(20\d{2}-\d{2}-\d{2})',text)
    # iden_matches = re.findall(r'重大傷病|健保|重大傷病|健堡|離島',text)
    # if iden_matches:
    #     field_data['欄位名稱'].append('社保身份')
    #     field_data['ocr辨識結果'].append('健保')

    if date_range_match:
        date_obj1, date_obj2=0, 0
        try:
            date_obj1 = datetime.strptime(date_range_match.group(1), "%Y%m%d")
            formatted_date1 = date_obj1.strftime("%Y/%m/%d")
            date_obj2 = datetime.strptime(date_range_match.group(2), "%Y%m%d")
            formatted_date2 = date_obj2.strftime("%Y/%m/%d")
        except ValueError:
            pass
        field_data['欄位名稱'].append('住院起日')
        if date_obj1!=0:
            field_data['ocr辨識結果'].append(formatted_date1)
        else:
            field_data['ocr辨識結果'].append(date_range_match.group(1))
        
        field_data['欄位名稱'].append('住院迄日')
        if date_obj2!=0:
            field_data['ocr辨識結果'].append(formatted_date2)
        else:
            field_data['ocr辨識結果'].append(date_range_match.group(2))
    elif date_matches and len(date_matches)>=2:
        date_obj1, date_obj2=0, 0
        try:
            date_obj1 = datetime.strptime(date_matches[0], "%Y%m%d")
            formatted_date1 = date_obj1.strftime("%Y/%m/%d")
            date_obj2 = datetime.strptime(date_matches[0], "%Y%m%d")
            formatted_date2 = date_obj2.strftime("%Y/%m/%d")
        except ValueError:
            pass
        field_data['欄位名稱'].append('住院起日')
        if date_obj1!=0:
            field_data['ocr辨識結果'].append(formatted_date1)
        else:
            field_data['ocr辨識結果'].append(date_matches[0])
        
        field_data['欄位名稱'].append('住院迄日')
        if date_obj2!=0:
            field_data['ocr辨識結果'].append(formatted_date2)
        else:
            field_data['ocr辨識結果'].append(date_matches[1])
