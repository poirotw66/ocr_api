import re
from datetime import datetime
from receipt_uni.convert_df_to_api_format import transfer_date
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

def extract_info_from_CG(text, field_data):
#     field_regex_map = {
#         # '事故者姓名': r'[姓 ]?名([^ ]+)',
#         # '病歷號': r'病[ ]?歷[ ]?號([^ ]+)', 
#         '病房費差額（單床）': r'[^\u4e00-\u9fff]*差額[ ]?[\(（c]?[單軍]?床[\)）]?\w*\s*(\d+)',
#         '病房費差額（雙床）':r'[^\u4e00-\u9fff]*差額[ ]?[\(（c]?雙床[\)）]?\w*\s*(\d+)',
#         '醫師診察費': r'[^\u4e00-\u9fff]*[醫]?師診察[費]?\w*\s*(\d+)',
#         '藥品費': r'[^\u4e00-\u9fff]*藥[品晶]\w*\s*(\d+)',
#         '核醫費': r'[^\u4e00-\u9fff]*核[醫醬]\w*\s*(\d+)',
#         'X光費': r'[^\u4e00-\u9fff]*X光\w*\s*(\d+)',
#         '材料費': r'[^\u4e00-\u9fff]*材料\w*\s*(\d+)',
#         '檢驗費': r'[^\u4e00-\u9fff]*檢驗\w*\s*(\d+)',
#         # '病房費': r'[^\u4e00-\u9fff]*病房\w*\s*(\d+)',
#         '護理費': r'[^\u4e00-\u9fff]*護理\w*\s*(\d+)',
#         '處置費': r'[^\u4e00-\u9fff]*處[宜置費腎]\w*[\s\$]*(\d+)',
#         '伙食費': r'[^\u4e00-\u9fff]*[伙休夜]?食\w*\s*(\d+)',
#         '掛號費': r'[^\u4e00-\u9fff]*掛號\w*\s*(\d+)',
#         '手術費': r'[^\u4e00-\u9fff]*手術\w*\s*(\d+)',
#         '麻醉費': r'[^\u4e00-\u9fff]*麻醉\w*\s*(\d+)',
#         '門（急）診費': r'[^\u4e00-\u9fff]*門[\s\w]*[\(（]?急[\) ]?診\w*\s*(\d+)',
#         '其他費': r'[^\u4e00-\u9fff]*[其共]?他\w*\s*(\d+)',
#         '證明書費': r'[^\u4e00-\u9fff]*證[明萌]書\w*\s*(\d+)',
#         '暫繳款':r'[^\u4e00-\u9fff]*暫繳款\w*\s*(\d+)',
#         '補助金額':r'[^\u4e00-\u9fff]*補助[金全]額\w*\s*(\d+)',
#         '優待金額':r'[^\u4e00-\u9fff]*優待[金全]額\w*\s*(\d+)',
#         '基本部份負擔':r'[^\u4e00-\u9fff]*基本部\w*\s*(\d+)',
#         '檢查檢驗部份負擔':r'[^\u4e00-\u9fff]*檢驗部\w*\s*(\d+)',
#         '藥費部份負擔':r'[^\u4e00-\u9fff]*藥費部\w*\s*(\d+)',
#         '復健部份負擔':r'[^\u4e00-\u9fff]*復健部\w*\s*(\d+)'
#     }

#     for field_name, regex_pattern in field_regex_map.items():
#         match = re.search(regex_pattern, text)
#         if match is not None:
#             field_data['欄位名稱'].append(field_name)
#             field_data['ocr辨識結果'].append(match.group(1))
    reduce_match = re.search(r'[^\u4e00-\u9fff]*減免\w*\s*(\d+)', text)
    total_cost_match =  re.search(r'[^\u4e00-\u9fff]*收據金額\s*(\d+)', text)
    total_cost2_match =  re.search(r'[^\u4e00-\u9fff]*金[額]?合計\s*(\d+)', text)
    if reduce_match:
        field_data['欄位名稱'].append('減免')
        field_data['ocr辨識結果'].append(reduce_match.group(1))
    if total_cost2_match and reduce_match:
        charge = int(total_cost2_match.group(1)) - int(reduce_match.group(1))
        field_data['欄位名稱'].append('總金額')
        field_data['ocr辨識結果'].append(str(charge))
    elif total_cost2_match:
        field_data['欄位名稱'].append('總金額')
        field_data['ocr辨識結果'].append(total_cost2_match.group(1))
    return field_data


def during_hos_from_text_CG(text,field_data):
    hos_30f_mathch =re.search(r'[^\u4e00-\u9fff]*30日以內[ ]?[\(（0]?急[\)）0]?\s*(\d+)',text)
    hos_31f_mathch =re.search(r'[^\u4e00-\u9fff]*31日以上[ ]?[\(（0]?急[\)）0]?\s*(\d+)',text)
    hos_60f_mathch =re.search(r'[^\u4e00-\u9fff]*31[-]?60[ ]?日[ ]?[\(（0]?急[\)）0]?\s*(\d+)',text)
    hos_30s_mathch =re.search(r'[^\u4e00-\u9fff]*30日以內[ ]?[\(（0]?慢[\)）0]?\s*(\d+)',text)
    hos_31s_mathch =re.search(r'[^\u4e00-\u9fff]*31日以上[ ]?[\(（0]?慢[\)）0]?\s*(\d+)',text)
    hos_90s_mathch =re.search(r'[^\u4e00-\u9fff]*31[-]?90[ ]?日[ ]?[\(（0]?慢[\)）0]?\s*(\d+)',text)
        # '住院部分負擔':  #30日以內(急) #31日以上(急)#31-60日(急) #30日以內(慢)#31日以上(慢) #31-90日(慢)
    field_data['欄位名稱'].append('住院部份負擔')
    sum =0
    if hos_30f_mathch and hos_31f_mathch and hos_60f_mathch:
        sum += int(hos_30f_mathch.group(1))+int(hos_31f_mathch.group(1))+int(hos_60f_mathch.group(1))
        field_data['ocr辨識結果'].append(str(sum))
    elif hos_30f_mathch and hos_31f_mathch:
        sum += int(hos_30f_mathch.group(1))+int(hos_31f_mathch.group(1))
        field_data['ocr辨識結果'].append(str(sum))    
    elif hos_30f_mathch:
        field_data['ocr辨識結果'].append(hos_30f_mathch.group(1))
    elif hos_31f_mathch:
        field_data['ocr辨識結果'].append(hos_31f_mathch.group(1))
    elif hos_60f_mathch:
        field_data['ocr辨識結果'].append(hos_60f_mathch.group(1))
    elif hos_30s_mathch and hos_31s_mathch and hos_90s_mathch:
        sum += int(hos_30s_mathch.group(1))+int(hos_31s_mathch.group(1))+int(hos_60s_mathch.group(1))
        field_data['ocr辨識結果'].append(str(sum))  
    elif hos_30s_mathch and hos_31s_mathch:
        sum += int(hos_30s_mathch.group(1))+int(hos_31s_mathch.group(1))
        field_data['ocr辨識結果'].append(str(sum))            
    elif hos_30s_mathch:
        field_data['ocr辨識結果'].append(hos_30s_mathch.group(1))
    elif hos_31s_mathch:
        field_data['ocr辨識結果'].append(hos_31s_mathch.group(1))
    elif hos_90s_mathch:
        field_data['ocr辨識結果'].append(hos_90s_mathch.group(1))
    else: 
        field_data['ocr辨識結果'].append('0')
    
    return field_data


def depaerment_from_text_CG(text,field_data):
    dept_all_match= re.search(r'[科]?[ ]?別\s*([^ ]+)',text)
    dept_match= re.search(r'[科]?[ ]?別\s*([^科 ]+科)',text)
    depart_match=re.search(r'[科]?[ ]?別\s*([^系 ]+系)',text)
    department_match=re.search(r'[科]?[ ]?別\s*([^部 ]+部)',text)  #= r'科別(\S+)部'
    # dept_c_pattern = re.compile(r'\S+科')
    
    dept_c_match = re.search(re.compile(r'\S+科'),text)
    dept_b_match = re.search(re.compile(r'\S+系'),text)
    # dept_a_match = re.search(re.compile(r'\S+部'),text)
    
    field_data['欄位名稱'].append('就診科別')
    if department_match:
        field_data['ocr辨識結果'].append(department_match.group(1))
    elif depart_match:
        field_data['ocr辨識結果'].append(depart_match.group(1))
    elif dept_match:
        field_data['ocr辨識結果'].append(dept_match.group(1))
    elif dept_all_match:
        field_data['ocr辨識結果'].append(dept_all_match.group(1))
    elif dept_c_match:
        field_data['ocr辨識結果'].append(dept_c_match.group(0))
    elif dept_b_match:
        field_data['ocr辨識結果'].append(dept_b_match.group(0))
    # elif dept_a_match:
        # field_data['ocr辨識結果'].append(dept_a_match.group(0))
    else:
        field_data['ocr辨識結果'].append('0')
    return field_data
    

    

def date_info_from_text_CG(text,field_data):
    date_range_match = re.search(r'(\d{4}\d{2}\d{2})[至]?(\d{4}\d{2}\d{2})', text)
    date_matches = re.findall(r'(20\d{2}\d{2}\d{2})',text)
    outpatient_date_match = re.search(r'[醫醬馨酉]日\w*\s*(\d{3}\s*/\s*\d{2}\s*/\s*\d{2})',text)
    if outpatient_date_match:
        field_data['欄位名稱'].append('就診日期')
        outpatient_date=transfer_date(outpatient_date_match.group(1))
        field_data['ocr辨識結果'].append(outpatient_date)
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
            date_obj2 = datetime.strptime(date_matches[1], "%Y%m%d")
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
    elif date_matches and len(date_matches)<2:
        try:
            date_obj1 = datetime.strptime(date_matches[0], "%Y%m%d")
            formatted_date1 = date_obj1.strftime("%Y/%m/%d")
            date_obj2 = datetime.strptime(date_matches[0], "%Y%m%d")
            formatted_date2 = date_obj2.strftime("%Y/%m/%d")
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
                field_data['ocr辨識結果'].append(date_matches[0])
        except ValueError:
            pass
    return field_data
        
    
def check_details_CG(rs_ocr):
    search_terms = ["名稱","數量"]
    for term in search_terms:
        index = rs_ocr.find(term)
        if index !=-1:
            return True
    return False

def check_details(rs_ocr):
    search_terms = ["名稱","數量"]
    for term in search_terms:
        index = rs_ocr.find(term)
        if index !=-1:
            return "details"
    return "receipt"