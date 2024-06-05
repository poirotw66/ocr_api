import re
from datetime import datetime

def transfer_date(input_date_str):
    year = int(input_date_str[:3]) + 1911 
    month = int(input_date_str[4:6])
    day = int(input_date_str[7:9])
    output_date_str = "{:04d}/{:02d}/{:02d}".format(year, month, day)
    return output_date_str
def extract_column_from_TCGH_puli(text, field_data):
    #print('text1:',text)
    field_regex_map = {
        # '事故者姓名': r'[姓 ]?名([^ ]+)',
        # '病歷號': r'病[ ]?歷[ ]?號([^ ]+)',
        '掛號費': r'[^\u4e00-\u9fff]*掛\s*號\w*\s*(\d+)',
        '伙食費': r'[^\u4e00-\u9fff]*[伙似]食\w*\s*(\d+)',
        '證明書費': r'[^\u4e00-\u9fff]*[證証]明書\w*\s*(\d+)',
        '診察費': r'[^\u4e00-\u9fff]*診察\w*\s*(\d+)',
        '藥費': r'[^\u4e00-\u9fff]*藥費\w*\s*(\d+)',
        '檢驗費': r'[^\u4e00-\u9fff]*檢[驗檢]\w*\s*(\d+)',
        'X光費': r'[^\u4e00-\u9fff]*X光\w*\s*(\d+)',
        '內檢費': r'[^\u4e00-\u9fff]*內檢\w*\s*(\d+)',
        '注射技術費': r'[^\u4e00-\u9fff]*注射技術\w*\s*(\d+)',
        '處理費': r'[^\u4e00-\u9fff]*處[理蓮]\w*\s*(\d+)',
        '材料費': r'\b材料費?\b\s*(\d+)',
        '特殊材料': r'[^\u4e00-\u9fff]*特[殊辣]材料\w*\s*(\d+)',
        '物理治療費': r'[^\u4e00-\u9fff]*物理治\w*\s*(\d+)',
        '手術費': r'[^\u4e00-\u9fff]*手術\w*\s*(\d+)',
        '血液救濟金': r'[^\u4e00-\u9fff]*血液救濟\w*\s*(\d+)',
        '治療費': r'[^\u4e00-\u9fff]* 治療\w*\s*(\d+)',
        '麻醉費': r'[^\u4e00-\u9fff]*麻醉\w*\s*(\d+)',
        '血費': r'[^\u4e00-\u9fff]*[血無]費\w*\s*(\d+)',
        '口服顆粒': r'[^\u4e00-\u9fff]*口服顆\w*\s*(\d+)',
        '口服藥水': r'[^\u4e00-\u9fff]*口服藥\w*\s*(\d+)',
        '體檢費': r'[^\u4e00-\u9fff]*體檢\w*\s*(\d+)',
        '放射治療費': r'[^\u4e00-\u9fff]*放射治療\w*\s*(\d+)',
        '人工腎臟費': r'[^\u4e00-\u9fff]*腎臟\w*\s*(\d+)',
        '牙科材料費': r'[^\u4e00-\u9fff]*[牙芽穿]科\w*\s*(\d+)',
        '假牙材料費': r'[^\u4e00-\u9fff]*假牙\w*\s*(\d+)',
        '矯正材料費': r'[^\u4e00-\u9fff]*矯[正追]\w*\s*(\d+)',
        '證書費': r'[^\u4e00-\u9fff]*證書\w*\s*(\d+)',
        '病房費': r'[^\u4e00-\u9fff]*病房\w*\s*(\d+)',
        '病床費': r'[^\u4e00-\u9fff]*病床\w*\s*(\d+)',
        '膳食費': r'[^\u4e00-\u9fff]*膳食\w*\s*(\d+)',
        '醫師費': r'[^\u4e00-\u9fff]*醫師費\s*(\d+)',
        '護理費': r'[^\u4e00-\u9fff]*護[理連]\w*\s*(\d+)',
        '接生費': r'[^\u4e00-\u9fff]*接生\w*\s*(\d+)',
        '嬰兒費': r'[^\u4e00-\u9fff]*嬰兒\w*\s*(\d+)',
        '雜項費': r'[^\u4e00-\u9fff]*雜項\w*\s*(\d+)',
        '藥師服務費': r'[^\u4e00-\u9fff]*[藥樂][師帥]服務\w*\s*(\d+)',
        '諮詢費': r'[^\u4e00-\u9fff]*諮詢\w*\s*(\d+)',
        #'住院部分負擔(急性)1-30日': r'[^\u4e00-\u9fff]*住?院?部分[負貧]擔\s*\(?急性\s*\)?\s*1-30\w*\s*(\d+)',
        #'住院部分負擔(急性)1-30日': r'[^\u4e00-\u9fff]*1-30日\w*\s*(\d+)',
        #'住院部分負擔(急性)31-60日': r'[^\u4e00-\u9fff]*31-60日\w*\s*(\d+)',
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
    
    search_pat = r'[^\u4e00-\u9fff]*住?院?部分[負食貧]擔\s*\(?急性\s*\)?\s*'
    search_pat1 = r'[^\u4e00-\u9fff]*1-30日\w*\s*(\d+)'
    search_pat2 = r'[^\u4e00-\u9fff]*31-60日\w*\s*(\d+)'
    search_case = re.search(search_pat,text)
    search_case1 = re.search(search_pat1,text)
    search_case2 = re.search(search_pat2,text)
    if search_case and search_case1:
        field_data['欄位名稱'].append('住院部分負擔(急性)1-30日')
        field_data['ocr辨識結果'].append(search_case1.group(1))
    
    if search_case and search_case2:
        field_data['欄位名稱'].append('住院部分負擔(急性)31-60日')
        field_data['ocr辨識結果'].append(search_case2.group(1))
        
      
    
    
    return field_data

def extract_info_from_TCGH_puli(text,field_data):
    #print('text2:',text)
    info_regex_map ={
        #'總金額':r'[實責費][收用]合計\w*\s*[,：:。;；,、]?\s*(\d+)',
        '總金額':r'[實責費][收用]合計金?額?\s*[,：:。;；,、]?\s*(\d+)',
        '就診科別':r'科\s*別\s+(\w+)',
        '社保身份':r'身[分份]\s+(.+?)(?=\s+[\u4e00-\u9fa5]+|$)'
    }
    for field_name, regex_pattern in info_regex_map.items():
        match = re.search(regex_pattern, text)
        if match is not None:
            field_data['欄位名稱'].append(field_name)
            field_data['ocr辨識結果'].append(match.group(1))
            
    date_range_match = re.search(r'[住在]院\w*期間[:：、‧]?\s*(\d{3}/\d{2}/\d{2})\s*[至]?\s*(\d{3}/\d{2}/\d{2})' , text)
    date_range_match2_start =  re.search(r'[住在]院期間[:：、‧]?\s*(\d{3}/\d{2}/\d{2})\s*',text)
    date_range_match2_end = re.search(r'收款日期[:：、‧]?\s*(\d{3}/\d{2}/\d{2})\s*',text)
    date_matches = re.findall(r'(20\d{2}-\d{2}-\d{2})',text)
    # iden_matches = re.findall(r'重大傷病|健保|重大傷病|健堡|離島',text)
    # if iden_matches:
    #     field_data['欄位名稱'].append('社保身份')
    #     field_data['ocr辨識結果'].append('健保')
    if date_range_match:
        field_data['欄位名稱'].append('住院起日')
        date_start=transfer_date(date_range_match.group(1))
        date_end=transfer_date(date_range_match.group(2))   
        date_obj1 = datetime.strptime(date_start, "%Y/%m/%d")
        date_obj2 = datetime.strptime(date_end, "%Y/%m/%d")
        formatted_date1 = date_obj1.strftime("%Y/%m/%d")
        formatted_date2 = date_obj2.strftime("%Y/%m/%d")
        field_data['ocr辨識結果'].append(formatted_date1)
        field_data['欄位名稱'].append('住院迄日')
        field_data['ocr辨識結果'].append(formatted_date2)
    if date_range_match == None and date_range_match2_start:
        field_data['欄位名稱'].append('住院起日')
        date_start=transfer_date(date_range_match2_start.group(1))
        date_obj1 = datetime.strptime(date_start, "%Y/%m/%d")
        formatted_date1 = date_obj1.strftime("%Y/%m/%d")
        field_data['ocr辨識結果'].append(formatted_date1)
    if date_range_match == None and date_range_match2_end:
        field_data['欄位名稱'].append('住院迄日')
        date_end=transfer_date(date_range_match2_end.group(1)) 
        date_obj2 = datetime.strptime(date_end, "%Y/%m/%d")
        formatted_date2 = date_obj2.strftime("%Y/%m/%d")
        field_data['ocr辨識結果'].append(formatted_date2)
    return field_data
