import re
import pandas as pd
import numpy as np
from datetime import datetime

def extract_info_from_TCGH(text,field_data):
    #print('tex1',text)
    # Define regular expressions to extract the data
    field_regex_map = {
        # '事故者姓名': r'姓名([^ ]+)',
        '社保身份': r'[射身]份\s*([^ ]+)',
        '就診科別': r'[就住]?[院醫]?[科][別剔分][:：]?\s*([^ ]+)',
        #'應收金額':r'應收[金全]額\s*[\u4e00-\u9fff]?\w*(\d+)',
        # '優待金額':r'優待[金全]額\s*[\u4e00-\u9fff]?\w*?(\d+)'
    }
    for field_name, regex_pattern in field_regex_map.items():
        match = re.search(regex_pattern, text)
        if match is not None:
            field_data['欄位名稱'].append(field_name)
            if field_name in ['社保身份','就診科別']:
                field_data['ocr辨識結果'].append(match.group(1))
            else:
                field_data['ocr辨識結果'].append(str(int(match.group(1))))
    #date_range_pattern = r'住院期間[-:：、‧]?\s*(\d{4}-\d{2}-\d{2}\s*[至]?\s*(\d{4}-\d{2}-\d{2})'
    date_range_pattern = r'[住在]院期間[:：、‧]?\s*(\d{4}-\d{2}-\d{2})\s*[至]?\s*(\d{4}-\d{2}-\d{2})'
    date_range_pattern2 = r'就診日期[::：、‧]?\s*(\d{4}/\d{2}/\d{2})'
    date_range_match = re.search(date_range_pattern, text)
    date_range_pattern3 = r'[住在]院期間[:：、‧]?\s*(\d{4}-\d{2}-\d{2})\s*'
    date_range_match2 = re.search(date_range_pattern2, text)
    date_range_match3 = re.search(date_range_pattern3, text)

    #amount_match = re.search(r'NT\$(\d+)',text)
    amount_match2 = re.search(r'[應費][收用][金全總]?額\w*\s*[,：:。;；,、]?\s*(\d+)',text)
    #if amount_match and amount_match2 and (int(amount_match.group(1)) == int(amount_match2.group(1))):
        #field_data['欄位名稱'].append('總金額')
        #field_data['ocr辨識結果'].append(str(int(amount_match.group(1))))
    #elif amount_match:
        #field_data['欄位名稱'].append('總金額')
        #field_data['ocr辨識結果'].append(str(int(amount_match.group(1))))
    if amount_match2:
        field_data['欄位名稱'].append('總金額')
        field_data['ocr辨識結果'].append(str(int(amount_match2.group(1))))

    if date_range_match:
        field_data['欄位名稱'].append('住院起日')
        date_start = date_range_match.group(1)
        date_end= date_range_match.group(2)
        date_obj1 = datetime.strptime(date_start, "%Y-%m-%d")
        date_obj2 = datetime.strptime(date_end, "%Y-%m-%d")
        formatted_date1 = date_obj1.strftime("%Y/%m/%d")
        formatted_date2 = date_obj2.strftime("%Y/%m/%d")
        field_data['ocr辨識結果'].append(formatted_date1)
        field_data['欄位名稱'].append('住院迄日')
        field_data['ocr辨識結果'].append(formatted_date2)
    if date_range_match == None and date_range_match3:
        field_data['欄位名稱'].append('住院起日')
        date_start = date_range_match3.group(1)
        date_obj1 = datetime.strptime(date_start, "%Y-%m-%d")
        formatted_date1 = date_obj1.strftime("%Y/%m/%d")
        field_data['ocr辨識結果'].append(formatted_date1)
    if date_range_match2:
         field_data['欄位名稱'].append('住院起日')
         date_start = date_range_match2.group(1)
         date_obj1 = datetime.strptime(date_start, "%Y/%m/%d")
         formatted_date1 = date_obj1.strftime("%Y/%m/%d")
         field_data['ocr辨識結果'].append(formatted_date1)
    return field_data
            
def extract_column_from_TCGH(text,is_decimal):
    print('text2',text)
    field_data = {'欄位名稱':[],'ocr辨識結果':[]}
    field_regex_map = {
        # '事故者姓名': r'[姓 ]?名([^ ]+)',
        # '病歷號': r'病[ ]?歷[ ]?號([^ ]+)',
        '掛號費': r'[^\u4e00-\u9fff]*掛\s*號\w*\s*(\d+)',
        '診察費': r'[^\u4e00-\u9fff]*診察\w*\s*(\d+)',
        '藥費': r'[^\u4e00-\u9fff]*藥費\w*\s*(\d+)',
        '檢驗費': r'[^\u4e00-\u9fff]*檢[驗檢]\w*\s*(\d+)',
        'X光費': r'[^\u4e00-\u9fff]*X光\w*\s*(\d+)',
        '內檢費': r'[^\u4e00-\u9fff]*內檢\w*\s*(\d+)',
        '技術費': r'[^\u4e00-\u9fff]*技術\w*\s*(\d+)',
        '注射技術費': r'[^\u4e00-\u9fff]*注射技術\w*\s*(\d+)',
        '處理費': r'[^\u4e00-\u9fff]*處[理蓮]\w*\s*(\d+)',
        '注射處置費': r'[^\u4e00-\u9fff]*注射處置\w*\s*(\d+)',
        '材料費': r'\b材料費?\b\s*(\d+)',
        '特殊材料費': r'[^\u4e00-\u9fff]*特[殊辣]材料\w*\s*(\d+)',
        '藥品部分負擔': r'[^\u4e00-\u9fff]*藥品部[份分]\w*\s*(\d+)',
        '特殊材料費(手術用)': r'[^\u4e00-\u9fff]*特[殊辣]材料費\s*\(手術用\)\w*\s*(\d+)',
        '治療材料費(手術用)': r'[^\u4e00-\u9fff]*治療處置費\s*\(手術用\)\w*\s*(\d+)',
        '物理治療費': r'[^\u4e00-\u9fff]*物理治\w*\s*(\d+)',
        '手術費': r'[^\u4e00-\u9fff]*手術\w*\s*(\d+)',
        '會診診查費': r'[^\u4e00-\u9fff]*會診診查\w*\s*(\d+)',
        '超音波檢查費': r'[^\u4e00-\u9fff]*超音波檢查\w*\s*(\d+)',
        '內視鏡檢查費': r'[^\u4e00-\u9fff]*內視鏡檢查\w*\s*(\d+)',
        '心電圖檢查費': r'[^\u4e00-\u9fff]*心電圖檢查\w*\s*(\d+)',
        '腦電波檢查費': r'[^\u4e00-\u9fff]*腦電波\w*\s*(\d+)',
        '肺功能檢查費': r'[^\u4e00-\u9fff]*肺功能檢查\w*\s*(\d+)',
        '心導管檢查費': r'[^\u4e00-\u9fff]*心導管檢查\w*\s*(\d+)',
        '核醫檢查費': r'[^\u4e00-\u9fff]*核醫檢查\w*\s*(\d+)',
        '病理檢驗費': r'[^\u4e00-\u9fff]*病理檢驗\w*\s*(\d+)',
        '復健治療費': r'[^\u4e00-\u9fff]*復健治療\w*\s*(\d+)',
        '治療費': r'[^\u4e00-\u9fff]* 治療費\w*\s*(\d+)',
        '一般材料費': r'[^\u4e00-\u9fff]*一?般材料\w*\s*(\d+)',
        '治療處置費': r'[^\u4e00-\u9fff]* 治療[處麻][置曾]\w*\s*(\d+)',
        '麻醉費': r'[^\u4e00-\u9fff]*麻醉\w*\s*(\d+)',
        '血費': r'[^\u4e00-\u9fff]*[血無]費\w*\s*(\d+)',
        '體檢費': r'[^\u4e00-\u9fff]*體檢\w*\s*(\d+)',
        '放射治療費': r'[^\u4e00-\u9fff]*放射治療\w*\s*(\d+)',
        '人工腎臟費': r'[^\u4e00-\u9fff]*腎臟\w*\s*(\d+)',
        '藥事服務費': r'[^\u4e00-\u9fff]*藥事服\w*\s*(\d+)',
        '牙科材料費': r'[^\u4e00-\u9fff]*[牙芽穿]科\w*\s*(\d+)',
        '假牙材料費': r'[^\u4e00-\u9fff]*假牙\w*\s*(\d+)',
        '麻醉材料費': r'[^\u4e00-\u9fff]*麻醉材料\w*\s*(\d+)',
        '矯正材料費': r'[^\u4e00-\u9fff]*矯[正追]\w*\s*(\d+)',
        '證書費': r'[^\u4e00-\u9fff]*證書\w*\s*(\d+)',
        #'病房費': r'[^\u4e00-\u9fff]*病房費\s*\ (\d+)',
        '病房費': r'[^\u4e00-\u9fff]?病房費\w*\s*(\d+)',
        '血液費': r'[^\u4e00-\u9fff]*[血t]液費\w*\s*(\d+)',
        '膳食費': r'[^\u4e00-\u9fff]*[膳騙肘][食養]\w*\s*(\d+)',
        '醫師費': r'[^\u4e00-\u9fff]*醫師費\s*(\d+)',
        '醫療影像上傳費': r'[^\u4e00-\u9fff]*醫療影像上傳\s*(\d+)',
        '代收電話費': r'[^\u4e00-\u9fff]*代收電話\w*\s*(\d+)',
        '護理費': r'[^\u4e00-\u9fff]*護[理連]\w*\s*(\d+)',
        '接生費': r'[^\u4e00-\u9fff]*接生\w*\s*(\d+)',
        '嬰兒費': r'[^\u4e00-\u9fff]*嬰兒\w*\s*(\d+)',
        '雜項費': r'[^\u4e00-\u9fff]*雜項\w*\s*(\d+)',
        '藥師服務費': r'[^\u4e00-\u9fff]*[藥樂][師帥]服務\w*\s*(\d+)',
        '諮詢費': r'[^\u4e00-\u9fff]*諮詢\w*\s*(\d+)',
        '部分負擔': r'\b部[份分]負擔\b\s*(\d+)(?!\s*-\s*\d+)',
        '部分負擔30日內': r'[^\u4e00-\u9fff]*[部音]分[負貧]擔30日\w*\s*(\d+)',
        '部分負擔30-60日內': r'[^\u4e00-\u9fff]*30-60日\w*\s*(\d+)',
        '部分負擔61日以上': r'[^\u4e00-\u9fff]*61日以上\w*\s*(\d+)',
        '部分負擔(急性)30日內': r'[^\u4e00-\u9fff]*部分[負貧]擔\s*\(急性\s*\)1-30日內\s*(\d+)',
        '住院門診預收':r'住院門診\w*\s*(\d+)',
        '預存抵繳':r'預存\w*\s*(\d+)',
        '預繳金額':r'預繳[金全]額\w*\s*(\d+)',
        '預繳行動支付':r'預繳行動\w*\s*(\d+)',
        '預繳現金':r'預繳現[金全]\w*\s*(\d+)',
        '預繳醫指付':r'預繳醫\w*\s*(\d+)',
        '已繳金額':r'已繳[金全]額\w*\s*(\d+)',
        '繳納現金':r'繳納現[金全]\w*\s*(\d+)',
        '已退金額':r'已退\w*\s*(\d+)',
        '保險金抵繳':r'保險[金全]抵繳\w*\s*(\d+)',
        '保險金抵扣':r'保險[金全]抵扣\w*\s*(\d+)',
        '振興券':r'振興券\w*\s*(\d+)',
        '補助金額':r'補助\w*\s*(\d+)',
        '優待金額':r'優待\w*\s*(\d+)',
        '合計': r'[^\u4e00-\u9fff]*合?計\w*\s*(\d+)(?!\s*-\s*\d+)',

    }
    #single_bed_pattern = r'病房費\s*\(單人房(\d+)天\s*\)\s*[\s()]*\s*(\d+)\s*'
    #double_bed_pattern = r'病房費\s*\(雙人房(\d+)天\s*\)\s*[\s()]*\s*(\d+)\s*'
    single_bed_pattern = r'病房費[ (c]*[單暈][人大]房(\d+)天\s*\)\s*[\s()]*\s*(\d+)'
    #single_bed_pattern = r'病房費\s*(?:\((單人房)?(\d+)天\s*\))?\s*(\d+)'
    double_bed_pattern = r'病房費[ (c]*雙人房(\d+)天\s*\)\s*[\s()]*\s*(\d+)'
    #date_cost_pattern_1_30 = r'1-30天\s*\d+\s*(\d+)'
    #date_cost_pattern_31_60 = r'31-60天\s*\d+\s*(\d+)'
    #date_cost_pattern_61up = r'61天以上\s*\d+\s*(\d+)'
    #
    #date_cost_matches_1_30 = re.search(date_cost_pattern_1_30,text)
    #date_cost_matches_31_60 = re.search(date_cost_pattern_31_60,text)  
    #date_cost_matches_61up = re.search(date_cost_pattern_61up,text) 
    
    single_bed_matches = re.search(single_bed_pattern, text)
    double_bed_matches = re.search(double_bed_pattern, text)

    if single_bed_matches is not None and is_decimal:
        days = single_bed_matches.group(1)
        cost = single_bed_matches.group(2)
        field_data['欄位名稱'].append(f'病房費(單人房{days}天)')
        field_data['ocr辨識結果'].append(cost[:-1])
    elif single_bed_matches is not None and not is_decimal:
        days = single_bed_matches.group(1)
        cost = single_bed_matches.group(2)
        field_data['欄位名稱'].append(f'病房費(單人房{days}天)')
        field_data['ocr辨識結果'].append(cost)
    if double_bed_matches is not None and is_decimal:
        days = double_bed_matches.group(1)
        cost = double_bed_matches.group(2)
        field_data['欄位名稱'].append(f'病房費(雙人房{days}天)')
        field_data['ocr辨識結果'].append(cost[:-1])
    elif double_bed_matches is not None and not is_decimal:
        days = double_bed_matches.group(1)
        cost = double_bed_matches.group(2)
        field_data['欄位名稱'].append(f'病房費(雙人房{days}天)')
        field_data['ocr辨識結果'].append(cost)
        
    '''
    if date_cost_matches_1_30 is not None:
        field_data['欄位名稱'].append('部分負擔(1至30天)')
        field_data['ocr辨識結果'].append(date_cost_matches_1_30.group(1))
    if date_cost_matches_31_60 is not None:
        field_data['欄位名稱'].append('部分負擔(31至60天)')
        field_data['ocr辨識結果'].append(date_cost_matches_31_60.group(1))
    if date_cost_matches_61up is not None:
        field_data['欄位名稱'].append('部分負擔(61天以上)')
        field_data['ocr辨識結果'].append(date_cost_matches_61up.group(1))
    '''
    if is_decimal:
        for field_name, regex_pattern in field_regex_map.items():
            match = re.search(regex_pattern, text)
            if match is not None:
                field_data['欄位名稱'].append(field_name)
                field_data['ocr辨識結果'].append(match.group(1)[:-1])
    else:
        for field_name, regex_pattern in field_regex_map.items():
            match = re.search(regex_pattern, text)
            if match is not None:
                field_data['欄位名稱'].append(field_name)
                field_data['ocr辨識結果'].append(match.group(1))
        
   
    new_df = pd.DataFrame(field_data)
    return new_df
