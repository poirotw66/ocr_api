import re
from datetime import datetime

def confirm_scope_identity(text, field_data):
    index = text.find("健保")
    declare = text.find("醫師診察費")
    point = text.find("點數合計")
    field_data['欄位名稱'].append('社保身份')
    if declare !=-1 and point==-1:
        field_data['ocr辨識結果'].append('自費')
    else:
        field_data['ocr辨識結果'].append('健保')
    
    fee_text = text[:index]
    return fee_text

def extract_info_from_NCKU(text, field_data):
    #print('text1',text)
    field_regex_map = {
        # '事故者姓名': r'[姓 ]?名([^ ]+)',
        # '病歷號': r'病[ ]?歷[ ]?號([^ ]+)', 
        '病房費差額（單床）': r'[^\u4e00-\u9fff]*差額[ ]?[\(（c]?[單軍]?床[\)）]?\w*\s*(\d+)',
        '病房費差額（雙床）':r'[^\u4e00-\u9fff]*差額[ ]?[\(（c]?雙床[\)）]?\w*\s*(\d+)',
        '醫師診察費': r'[^\u4e00-\u9fff]*[醫]?師診察[費]?\w*\s*(\d+)',
        '藥品費': r'[^\u4e00-\u9fff]*藥[品晶]\w*\s*(\d+)',
        '核醫費': r'[^\u4e00-\u9fff]*核[醫醬]\w*\s*(\d+)',
        'X光費': r'[^\u4e00-\u9fff]*X光\w*\s*(\d+)',
        '注射技術費': r'[^\u4e00-\u9fff]*注射技術\w*\s*(\d+)',
        '放射線診療費': r'[^\u4e00-\u9fff]*放射線\w*\s*(\d+)',
        '材料費': r'\b材料\w*\s*(\d+)',
        '藥劑費': r'[^\u4e00-\u9fff]*藥劑\w*\s*(\d+)',
        '復健治療費': r'[^\u4e00-\u9fff]*復健\w*\s*(\d+)',
        '醫用材料費': r'[^\u4e00-\u9fff]*醫用材\w*\s*(\d+)',
        '掛號行政費': r'[^\u4e00-\u9fff]*掛號行\w*\s*(\d+)',
        '檢驗費': r'[^\u4e00-\u9fff]*檢驗\w*\s*(\d+)',
        '診察費': r'\b診察\w*\s*(\d+)',
        '血液暨處理費': r'[^\u4e00-\u9fff]*血液暨\w*\s*(\d+)',
        '血液透析費': r'[^\u4e00-\u9fff]*血液透\w*\s*(\d+)',
        '病房費': r'[^\u4e00-\u9fff]*病房\w*\s*(\d+)',
        '檢驗檢查費': r'[^\u4e00-\u9fff]*檢驗\w*\s*(\d+)',
        '衛生材料費': r'[^\u4e00-\u9fff]*衛生\w*\s*(\d+)',
        '治療處置費': r'[^\u4e00-\u9fff]*治療處\w*\s*(\d+)',
        '膳食營養費': r'[^\u4e00-\u9fff]*膳食營\w*\s*(\d+)',
        '護理費': r'[^\u4e00-\u9fff]*護理\w*\s*(\d+)',
        '處置費': r'[^\u4e00-\u9fff]*處[宜置費腎]\w*[\s\$]*(\d+)',
        '伙食費': r'[^\u4e00-\u9fff]*伙食\w*\s*(\d+)',
        #'掛號費': r'[^\u4e00-\u9fff]*掛號\w*\s*(\d+)',
        '手術費': r'[^\u4e00-\u9fff]*手術\w*\s*(\d+)',
        '麻醉費': r'[^\u4e00-\u9fff]*麻醉\w*\s*(\d+)',
        '門（急）診費': r'[^\u4e00-\u9fff]*門[\s\w]*[\(（]?急[\) ]?診\w*\s*(\d+)',
        '其他費用': r'[^\u4e00-\u9fff]*[其共]?他\w*\s*(\d+)',
        '證明書費': r'[^\u4e00-\u9fff]*證[明萌]書\w*\s*(\d+)',
        '暫繳款':r'[^\u4e00-\u9fff]*暫繳款\w*\s*(\d+)',
        # '住院門診預收':r'住院門診預收\s*[\u4e00-\u9fff]?\w*?(\d+)',
        # '預存抵繳':r'預存抵繳\s*[\u4e00-\u9fff]?\w*?(\d+)',
        # '預繳金額':r'預繳[金全]額\s*[\u4e00-\u9fff]?\w*?(\d+)',
        # '預繳行動支付':r'預繳行動支付\s*[\u4e00-\u9fff]?\w*?(\d+)',
        # '預繳現金':r'預繳現[金全]\s*[\u4e00-\u9fff]?\w*?(\d+)',
        # '預繳醫指付':r'預繳醫指付\s*[\u4e00-\u9fff]?\w*?(\d+)',
        # '已繳金額':r'已繳[金全]額\s*[\u4e00-\u9fff]?\w*?(\d+)',
        # '繳納現金':r'繳納現[金全]\s*[\u4e00-\u9fff]?\w*?(\d+)',
        # '信用卡':r'信用卡\s*[\u4e00-\u9fff]?\w*?(\d+)',
        # '已退金額':r'已退[金全]額\s*[\u4e00-\u9fff]?\w*?(\d+)',
        # '保險金抵繳':r'保險[金全]抵繳\s*[\u4e00-\u9fff]?\w*?(\d+)',
        # '保險金抵扣':r'保險[金全]抵扣\s*[\u4e00-\u9fff]?\w*?(\d+)',
        # '振興券':r'振興券\s*[\u4e00-\u9fff]?\w*?(\d+)',
        '補助金額':r'[^\u4e00-\u9fff]*補助[金全]額\w*\s*(\d+)',
        '優待金額':r'[^\u4e00-\u9fff]*優待[金全]額\w*\s*(\d+)',
    }
    single_normal_room_regex = re.compile(r'[^\u4e00-\u9fff]*單人房(\d+)日(\d+)')
    single_normal_room_match = single_normal_room_regex.search(text)
    print('match:',single_normal_room_match)


    
    for field_name, regex_pattern in field_regex_map.items():
        match = re.search(regex_pattern, text)
        if match is not None:
            field_data['欄位名稱'].append(field_name)
            field_data['ocr辨識結果'].append(match.group(1))
    # prepay_match = re.search(r'暫繳款\s(\d+)', text)
    reduce_match = re.search(r'[^\u4e00-\u9fff]*減免\s*(\d+)', text)
    total_cost2_match =  re.search(r'[^\u4e00-\u9fff]*費用合計?\w*\s*(\d+)', text)
    
    # if prepay_match:
    #     field_data['欄位名稱'].append('暫繳款')
    #     field_data['ocr辨識結果'].append(prepay_match.group(1))
    if reduce_match:
        field_data['欄位名稱'].append('減免')
        field_data['ocr辨識結果'].append(reduce_match.group(1))
    elif total_cost2_match:
        field_data['欄位名稱'].append('總金額')
        field_data['ocr辨識結果'].append(total_cost2_match.group(1))
    return field_data

def during_hos_from_text_NCKU(text,field_data):
    hos_30f_mathch =re.search(r'[^\u4e00-\u9fff]*30日以內[ ]?[\(（0]?急[\)）0]?\s*(\d+)',text)
    hos_31f_mathch =re.search(r'[^\u4e00-\u9fff]*31日以上[ ]?[\(（0]?急[\)）0]?\s*(\d+)',text)
    hos_60f_mathch =re.search(r'[^\u4e00-\u9fff]*31[-]?60[ ]?日[ ]?[\(（0]?急[\)）0]?\s*(\d+)',text)
    hos_30s_mathch =re.search(r'[^\u4e00-\u9fff]*30日以內[ ]?[\(（0]?慢[\)）0]?\s*(\d+)',text)
    hos_31s_mathch =re.search(r'[^\u4e00-\u9fff]*31日以上[ ]?[\(（0]?慢[\)）0]?\s*(\d+)',text)
    hos_90s_mathch =re.search(r'[^\u4e00-\u9fff]*31[-]?90[ ]?日[ ]?[\(（0]?慢[\)）0]?\s*(\d+)',text)
        # '住院部分負擔':  #30日以內(急) #31日以上(急)#31-60日(急) #30日以內(慢)#31日以上(慢) #31-90日(慢)
    field_data['欄位名稱'].append('住院部份負擔')
    if hos_30f_mathch:
        field_data['ocr辨識結果'].append(hos_30f_mathch.group(1))
    elif hos_31f_mathch:
        field_data['ocr辨識結果'].append(hos_31f_mathch.group(1))
    elif hos_60f_mathch:
        field_data['ocr辨識結果'].append(hos_60f_mathch.group(1))
    elif hos_30s_mathch:
        field_data['ocr辨識結果'].append(hos_30s_mathch.group(1))
    elif hos_31s_mathch:
        field_data['ocr辨識結果'].append(hos_31s_mathch.group(1))
    elif hos_90s_mathch:
        field_data['ocr辨識結果'].append(hos_90s_mathch.group(1))
    else: 
        field_data['ocr辨識結果'].append('0')
    return field_data

def depaerment_from_text_NCKU(text,field_data):
    dept_match= re.search(r'[科]?[ ]?別\s*([^科 ]+科)',text)
    depart_match=re.search(r'[科]?[ ]?別\s*([^系 ]+系)',text)
    department_match=re.search(r'[科]?[ ]?別\s*([^部 ]+部)',text)  #= r'科別(\S+)部'
    # dept_c_pattern = re.compile(r'\S+科')
    
    dept_c_match = re.search(re.compile(r'\S+科'),text)
    dept_b_match = re.search(re.compile(r'\S+系'),text)
    dept_a_match = re.search(re.compile(r'\S+部'),text)
    
    field_data['欄位名稱'].append('就診科別')
    if department_match:
        field_data['ocr辨識結果'].append(department_match.group(1))
    elif depart_match:
        field_data['ocr辨識結果'].append(depart_match.group(1))
    elif dept_match:
        field_data['ocr辨識結果'].append(dept_match.group(1))
    elif dept_c_match:
        field_data['ocr辨識結果'].append(dept_c_match.group(0))
    elif dept_b_match:
        field_data['ocr辨識結果'].append(dept_b_match.group(0))
    elif dept_a_match:
        field_data['ocr辨識結果'].append(dept_a_match.group(0))
    else:
        field_data['ocr辨識結果'].append('0')
    
    return field_data
    

def date_info_from_text_NCKU(text,field_data):
    date_range_match = re.search(r'(\d{4}\d{2}\d{2})[至]?(\d{4}\d{2}\d{2})', text)
    date_matches = re.findall(r'(20\d{2}\d{2}\d{2})',text)
 
    if date_range_match:
        date_obj1, date_obj2=0, 0
        try:
            date_obj1 = datetime.strptime(date_range_match.group(1), "%Y%m%d")
            formatted_date1 = date_obj1.strftime("%Y/%m/%d")
            date_obj2 = datetime.strptime(date_range_match.group(2), "%Y%m%d")
            formatted_date2 = date_obj2.strftime("%Y/%m/%d")
        except ValueError:
            pass
        
        if date_obj1!=0:
            field_data['欄位名稱'].append('住院起日')
            field_data['ocr辨識結果'].append(formatted_date1)
        else:
            field_data['欄位名稱'].append('住院起日')
            field_data['ocr辨識結果'].append(date_range_match.group(1))
        
        if date_obj2!=0:
            field_data['欄位名稱'].append('住院迄日')
            field_data['ocr辨識結果'].append(formatted_date2)
        else:
            field_data['欄位名稱'].append('住院迄日')
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
        
        if date_obj1!=0:
            field_data['欄位名稱'].append('住院起日')
            field_data['ocr辨識結果'].append(formatted_date1)
        else:
            field_data['欄位名稱'].append('住院起日')
            field_data['ocr辨識結果'].append(date_matches[0])        
        if date_obj2!=0:
            field_data['欄位名稱'].append('住院迄日')
            field_data['ocr辨識結果'].append(formatted_date2)
        else:
            field_data['欄位名稱'].append('住院迄日')
            field_data['ocr辨識結果'].append(date_matches[1])
    return field_data
