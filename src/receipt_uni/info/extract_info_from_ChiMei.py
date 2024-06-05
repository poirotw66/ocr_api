import re
from datetime import datetime
from receipt_uni.info.extract_info_from_CCH import transfer_date
def extract_column_from_ChiMei(text, field_data):
    field_regex_map = {
        '診察費': r'[^\u4e00-\u9fff]*診察\w*\s*(\d+)',
        '病房費': r'[^\u4e00-\u9fff]病房\w*\s*(\d+)',
        '護理費': r'[^\u4e00-\u9fff]*護[理連]\w*\s*(\d+)',
        '膳食費': r'[^\u4e00-\u9fff]*[膳膠]食\w*\s*(\d+)',
        '檢查費': r'[^\u4e00-\u9fff]*檢查\w*\s*(\d+)',
        '放射線診療費': r'[^\u4e00-\u9fff]*放射\w*\s*(\d+)',
        '治療處置費': r'[^\u4e00-\u9fff]*治療\w*\s*(\d+)',
        '血液暨處理費': r'[^\u4e00-\u9fff][血無]液\w*\s*(\d+)',
        '手術費': r'[^\u4e00-\u9fff]*手術\w*\s*(\d+)',
        '復健治療費': r'[^\u4e00-\u9fff]*復健\w*\s*(\d+)',
        '麻醉費': r'[^\u4e00-\u9fff]*麻醉\w*\s*(\d+)',
        '特殊材料費': r'[^\u4e00-\u9fff]*[特痔][殊辣]材\w*\s*(\d+)',
        '藥費': r'[^\u4e00-\u9fff]*[藥樂]費\w*\s*(\d+)',
        '藥事服務費': r'[^\u4e00-\u9fff]*[藥樂]事\w*\s*(\d+)',
        '注射技術費': r'[^\u4e00-\u9fff]*注射技\w*\s*(\d+)',
        '加護病房個人衛生費': r'[^\u4e00-\u9fff]*護病\w*\s*(\d+)',
        '其他費用': r'[^\u4e00-\u9fff]*[其共]他\w*\s*(\d+)',
        
        '證明書費': r'[^\u4e00-\u9fff]*證明\w*\s*(\d+)',
        '輸血費': r'[^\u4e00-\u9fff]*輸血\w*\s*(\d+)',
        '掛號費': r'[^\u4e00-\u9fff]*掛\s*號\w*\s*(\d+)',
        '檢驗費': r'[^\u4e00-\u9fff]*檢[驗檢]\w*\s*(\d+)',
        
        '處置費': r'[^\u4e00-\u9fff]處[置景]\w*\s*(\d+)',
        
        '特殊調劑費': r'[^\u4e00-\u9fff]*特殊調\w*\s*(\d+)',
        # '３０日以內部分負擔': r'[^\u4e00-\u9fff]*30日\w*\s*(\d+)',
        # '３１~６０日部分負擔': r'[^\u4e00-\u9fff]*31~60日\w*\s*(\d+)',
        '健保部分負擔': r'[^\u4e00-\u9fff]*健保部\w*\s*(\d+)',
        'Ｘ光費': r'[^\u4e00-\u9fff]*X光\w*\s*(\d+)',
        '內檢費': r'[^\u4e00-\u9fff]*內檢\w*\s*(\d+)',
        '處理費': r'[^\u4e00-\u9fff]*處[理蓮]\w*\s*(\d+)',
        '材料費': r'[^\u4e00-\u9fff]材料\w*\s*(\d+)',
        '物理治療費': r'[^\u4e00-\u9fff]*物理治\w*\s*(\d+)', 
        '體檢費': r'[^\u4e00-\u9fff]*體檢\w*\s*(\d+)', 
        '人工腎臟費': r'[^\u4e00-\u9fff]*腎臟\w*\s*(\d+)',
        '牙科材料費': r'[^\u4e00-\u9fff]*[牙芽穿]科\w*\s*(\d+)',
        '假牙材料費': r'[^\u4e00-\u9fff]*假牙\w*\s*(\d+)',
        '矯正材料費': r'[^\u4e00-\u9fff]*矯[正追]\w*\s*(\d+)',  
        '醫師費': r'[^\u4e00-\u9fff]*醫師費\s*(\d+)',
        '藥師費': r'[^\u4e00-\u9fff]*藥師費\s*(\d+)',  
        '接生費': r'[^\u4e00-\u9fff]*接生\w*\s*(\d+)',
        '嬰兒費': r'[^\u4e00-\u9fff]*嬰兒\w*\s*(\d+)',
        '雜項費': r'[^\u4e00-\u9fff]*雜項\w*\s*(\d+)',
        '藥師服務費': r'[^\u4e00-\u9fff]*[藥樂][師帥]服務\w*\s*(\d+)',
        '諮詢費': r'[^\u4e00-\u9fff]*諮詢\w*\s*(\d+)',
        
        # '６１天以上部分負擔': r'[^\u4e00-\u9fff]*61天\w*\s*(\d+)',
        
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
    return field_data

def extract_sect_from_ChiMei(text,field_data):
    sect_match = re.search(r"BedNo\s*([^ ]+)",text)
    if sect_match:
        target=sect_match.group(1).replace(' ','').replace('~','-').replace('一','-')
        field_data['欄位名稱'].append('就診科別')
        field_data['ocr辨識結果'].append(target.upper())

def extract_info_from_ChiMei(text,field_data):
    info_regex_map ={
        # '總金額':r'收[金全]額\s*[$]?(\d+)',
        # '就診科別':r'科\s*別\s+(\w+)',
        '社保身份':r'身分別\s*([^ ]+)',
        '部分負擔':r'部分負擔[-]?\w*\s*(\d+)',
    }
    for field_name, regex_pattern in info_regex_map.items():
        match = re.search(regex_pattern, text)
        if match is not None:
            field_data['欄位名稱'].append(field_name)
            field_data['ocr辨識結果'].append(match.group(1))
    sum_a_match = re.search(r'繳[金全查]額\w*\s*(\d+)',text)        
    if sum_a_match:
        field_data['欄位名稱'].append('總金額')
        field_data['ocr辨識結果'].append(sum_a_match.group(1))

    date_start_match=re.search(r'[就][醫醬]日[期其共]?\s*(\d{3}\s*/\s*\d{2}\s*/\s*\d{2})',text)
    date_matches=re.findall(r'[^\d\w](\d{3}\s*/\s*\d{2}\s*/\s*\d{2})',text)
    if date_start_match:
        field_data['欄位名稱'].append('住院起日')
        date_start=transfer_date(date_start_match.group(1))
        field_data['ocr辨識結果'].append(date_start)
    # elif date_matches:
    #     field_data['欄位名稱'].append('住院起日')
    #     date_start=transfer_date(date_matches[0])
    #     field_data['ocr辨識結果'].append(date_start)
    #     # field_data['ocr辨識結果'].append(date_start_match.group(1))
    date_end_match=re.search(r'[出日][院完玩][日]?[期其共]?\s*(\d{3}\s*/\s*\d{2}\s*/\s*\d{2})',text)
    if date_end_match:
        field_data['欄位名稱'].append('住院迄日')
        date_end=transfer_date(date_end_match.group(1))
        field_data['ocr辨識結果'].append(date_end)
    # elif date_matches and len(date_matches)>=2:
    #     field_data['欄位名稱'].append('住院迄日')
    #     date_end=transfer_date(date_matches[1])
    #     field_data['ocr辨識結果'].append(date_end)
    return field_data

