import re
import pandas as pd
def transfer_date(input_date_str):
    year = int(input_date_str[:3]) + 1911 
    month = int(input_date_str[4:6])
    day = int(input_date_str[7:9])
    output_date_str = "{:04d}/{:02d}/{:02d}".format(year, month, day)
    return output_date_str
def extract_info_from_CMH(text,field_data):
    # Define regular expressions to extract the data
    field_regex_map = {
        # '事故者姓名': r'姓名([^ ]+)',
        '社保身份': r'就[醫醬酉]?身份([^ ]+)',
        '就診科別': r'[科]?別[:：]?\s*([^ ]+)',
        '住院門診預收':r'住院門診預收\s*[\u4e00-\u9fff]?\w*?(\d+)',
        '預存抵繳':r'預存抵繳\s*[\u4e00-\u9fff]?\w*?(\d+)',
        '預繳金額':r'預繳[金全]額\s*[\u4e00-\u9fff]?\w*?(\d+)',
        '預繳行動支付':r'預繳行動支付\s*[\u4e00-\u9fff]?\w*?(\d+)',
        '預繳現金':r'預繳現[金全]\s*[\u4e00-\u9fff]?\w*?(\d+)',
        '預繳醫指付':r'預繳醫指付\s*[\u4e00-\u9fff]?\w*?(\d+)',
        '已繳金額':r'已繳[金全]額\s*[\u4e00-\u9fff]?\w*?(\d+)',
        '繳納現金':r'繳納現[金全]\s*[\u4e00-\u9fff]?\w*?(\d+)',
        '信用卡':r'信用卡\s*[\u4e00-\u9fff]?\w*?(\d+)',
        '已退金額':r'已退[金全]額\s*[\u4e00-\u9fff]?\w*?(\d+)',
        '保險金抵繳':r'保險[金全]抵繳\s*[\u4e00-\u9fff]?\w*?(\d+)',
        '保險金抵扣':r'保險[金全]抵扣\s*[\u4e00-\u9fff]?\w*?(\d+)',
        '振興券':r'振興券\s*[\u4e00-\u9fff]?\w*?(\d+)',
        '補助金額':r'補助[金全]額\s*[\u4e00-\u9fff]?\w*?(\d+)',
        '優待金額':r'優待[金全]額\s*[\u4e00-\u9fff]?\w*?(\d+)',
        
        #'就醫日期': r'就醫日期(\d{3}/\d{2}/\d{2})\(\d\)',
    }
    for field_name, regex_pattern in field_regex_map.items():
        match = re.search(regex_pattern, text)
        if match is not None:
            field_data['欄位名稱'].append(field_name)
            field_data['ocr辨識結果'].append(match.group(1))
    date_range_pattern = r'[住]?院期間[:：、‧]?\s*(\d{3}/\d{2}/\d{2})[~-]?(\d{3}/\d{2}/\d{2})'
    date_range_match = re.search(date_range_pattern, text)
    
    medical_data_range_pattern =r'就醫日期\s*(\d{3}/\d{2}/\d{2})'
    medical_date_range_match = re.search(medical_data_range_pattern, text)
    date_matches = re.findall(r'(20\d{2}/\d{2}/\d{2})',text)
    #amount_match = re.search(r'NT\$(\d+)',text)
    amount_match = re.search(r'應繳\w*\s*(\d+)',text)
    amount_match2 = re.search(r'[總聰急]額\w*\s*(\d+)',text)
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
        date_start=transfer_date(date_range_match.group(1))
        #field_data['ocr辨識結果'].append(date_range_match.group(1))
        field_data['ocr辨識結果'].append(date_start)
        field_data['欄位名稱'].append('住院迄日')
        date_end=transfer_date(date_range_match.group(2))
        field_data['ocr辨識結果'].append(date_end)
    elif date_matches and len(date_matches)>=2:
        field_data['欄位名稱'].append('住院起日')
        date_start=transfer_date(date_matches[0])
        field_data['ocr辨識結果'].append(date_start)
        field_data['欄位名稱'].append('住院迄日')
        date_end=transfer_date(date_matches[1])
        field_data['ocr辨識結果'].append(date_end)
    if medical_date_range_match:
        field_data['欄位名稱'].append('住院起日')
        medical_date_start = transfer_date(medical_date_range_match.group(1))
        field_data['ocr辨識結果'].append(medical_date_start)
    
        
    
    return field_data
            
def extract_column_from_CMH(text):

    field_data = {'欄位名稱':[],'ocr辨識結果':[]}
    field_regex_map = {
        # '事故者姓名': r'[姓 ]?名([^ ]+)',
        # '病歷號': r'病[ ]?歷[ ]?號([^ ]+)',
        '藥費': r'[^\u4e00-\u9fff][藥樂]費 (\d+)',
        '治療處置費': r'[^\u4e00-\u9fff]治療處置費\w*\s*(\d+)',
        '手術費': r'[^\u4e00-\u9fff]手術費\w*\s*(\d+)',
        '材料費': r'[^\u4e00-\u9fff]材料費\w*\s*(\d+)',
        '放射線診療費': r'[^\u4e00-\u9fff]放射線診療費\w*\s*(\d+)',
        '麻醉技術費': r'[^\u4e00-\u9fff]麻醉技術費\w*\s*(\d+)',
        '檢查檢驗費': r'[^\u4e00-\u9fff]檢查檢驗費\w*\s*(\d+)',
        '證明書費': r'[^\u4e00-\u9fff][証證]明書費\w*\s*(\d+)',
        '放射/化學/其他治療費': r'[^\u4e00-\u9fff]放射[/7]?化學[/7]?其他治療\w*\s*(\d+)',
        '血液費': r'[^\u4e00-\u9fff]血液費\w*\s*(\d+)',
        '病房費': r'[^\u4e00-\u9fff]病房費\w*\s*(\d+)',
        'ICU病房費': r'[^\u4e00-\u9fff]ICU病\w*\s*(\d+)',
        '診察費': r'[^\u4e00-\u9fff]診察\w*\s*(\d+)',
        '護理費': r'[^\u4e00-\u9fff]護理\w*\s*(\d+)',
        '管灌膳食費': r'[^\u4e00-\u9fff]管灌膳\w*\s*(\d+)',
        '護理費': r'[^\u4e00-\u9fff]護理\w*\s*(\d+)',
        '藥事服務費': r'[^\u4e00-\u9fff]藥事服\w*\s*(\d+)',
        '牙科治療處置費': r'[^\u4e00-\u9fff]牙科治療\w*\s*(\d+)',        
        '藥費部份負擔': r'[^\u4e00-\u9fff]藥費部份\w*\s*(\d+)',
        '治療處置費部份負擔': r'[^\u4e00-\u9fff]治療處置[費負]?部\w*\s*(\d+)',
        '手術費部份負擔': r'[^\u4e00-\u9fff]手術費部\w*\s*(\d+)',
        '材料費部份負擔': r'[^\u4e00-\u9fff]材料費部份\w*\s*(\d+)',
        '放射線診療費部份負': r'[^\u4e00-\u9fff]放射線診療費部\w*\s*(\d+)',
        '麻醉技術費部份負擔': r'[^\u4e00-\u9fff]麻醉技術費部\w*\s*(\d+)',
        '檢查檢驗費部份負擔': r'[^\u4e00-\u9fff]檢查檢驗費部\w*\s*(\d+)',
        '證明書費部份負擔': r'[^\u4e00-\u9fff]証明書費部\w*\s*(\d+)',
        '放射/化學/其他治療費部份負擔': r'[^\u4e00-\u9fff]放射/化學/其他治療費部\w*\s*(\d+)',
        '血液費部份負擔': r'[^\u4e00-\u9fff]血液費部\w*\s*(\d+)',
        '病房費部份負擔': r'[^\u4e00-\u9fff]病房費部\w*\s*(\d+)',
        'ICU病房費部份負擔': r'[^\u4e00-\u9fff]ICU病房費部\w*\s*(\d+)',
        '診察費部份負擔': r'[^\u4e00-\u9fff]診察費部份\w*\s*(\d+)',
        '護理費部份負擔': r'[^\u4e00-\u9fff]護理費部份\w*\s*(\d+)',
        '管灌膳食費部份負擔': r'[^\u4e00-\u9fff]管灌膳食費部\w*\s*(\d+)',
        '護理費部份負擔': r'[^\u4e00-\u9fff]護理費部\w*\s*(\d+)',
        '藥事服務費部份負擔': r'[^\u4e00-\u9fff]藥事服務費部\w*\s*(\d+)',
        '牙科治療處置費部份負擔': r'[^\u4e00-\u9fff]牙科治療處置費部\w*\s*(\d+)',
         #new add 
        '注射技術費': r'[^\u4e00-\u9fff]注射技\w*\s*(\d+)',
        '特殊材料費': r'[^\u4e00-\u9fff]特[殊珠]材料\w*\s*(\d+)',
        '麻醉費': r'[^\u4e00-\u9fff]麻醉\w*\s*(\d+)',
        '檢查費': r'[^\u4e00-\u9fff]檢查\w*\s*(\d+)',
        '診斷書費': r'[^\u4e00-\u9fff]診斷書\w*\s*(\d+)',
        '掛號費': r'[^\u4e00-\u9fff]掛號\w*\s*(\d+)',
        '治療性營養品': r'[^\u4e00-\u9fff]治療性營養\w*\s*(\d+)',
        '血液血漿費': r'[^\u4e00-\u9fff][血無]液血漿費\w*\s*(\d+)',
        '復健治療費': r'[^\u4e00-\u9fff]復健治\w*\s*(\d+)',
        '基本部分負擔': r'[^\u4e00-\u9fff]基本部分\w*\s*(\d+)',
        '藥費部分負擔': r'[^\u4e00-\u9fff]藥費部分\w*\s*(\d+)',
        '療程部分負擔': r'[^\u4e00-\u9fff]療程部分\w*\s*(\d+)',
        '基本部分負擔(代收)': r'[^\u4e00-\u9fff]基本部分負擔(代收)\w*\s*(\d+)',
        '診斷書證明費': r'[^\u4e00-\u9fff]診斷書證明費\w*\s*(\d+)',
        '病歷複製本費': r'[^\u4e00-\u9fff]病[歷壓]?複製本費\w*\s*(\d+)',
        '其他': r'[^\u4e00-\u9fff][其共][他化]\w*\s*(\d+)',
        '病程照護費': r'[^\u4e00-\u9fff]病程照護費\w*\s*(\d+)',
        '血液透析費': r'[^\u4e00-\u9fff]血液透析費\w*\s*(\d+)',
        '部分負擔明細(01~30天)': r'[^\u4e00-\u9fff]01~?30\s?天\s*(\d+)\b',
        '部分負擔明細(31~60天)': r'[^\u4e00-\u9fff]31~?60\s?天\s*(\d+)\b',
        '部分負擔明細(61天以上)': r'[^\u4e00-\u9fff]61天以上\s*(\d+)\b',
        

    }
    single_normal_room_regex = re.compile(r'[*林]{0,2}單人房計(\d+)日 (\d+)')
    single_normal_room_match = single_normal_room_regex.search(text)
    
    normal_room_regex = re.compile(r'[*林]{0,2}雙人房計(\d+)日 (\d+)')
    normal_room_match = normal_room_regex.search(text)
    premium_room_regex = re.compile(r'[*林]{0,2}頂級房計(\d+)日 (\d+)')
    premium_room_match = premium_room_regex.search(text)
    meal_cost_regex = re.compile(r'伙食費共計(\d+)日 (\d+)')
    meal_cost_match = meal_cost_regex.search(text)
    
    if single_normal_room_match is not None:
        days = single_normal_room_match.group(1)
        cost = single_normal_room_match.group(2)
        field_data['欄位名稱'].append(f'單人房計{days}日')
        field_data['ocr辨識結果'].append(cost)
    
    if normal_room_match is not None:
        days = normal_room_match.group(1)
        cost = normal_room_match.group(2)
        field_data['欄位名稱'].append(f'雙人房計{days}日')
        field_data['ocr辨識結果'].append(cost)
    if meal_cost_match is not None:
        days = meal_cost_match.group(1)
        cost = meal_cost_match.group(2)
        field_data['欄位名稱'].append(f'伙食費共計{days}日')
        field_data['ocr辨識結果'].append(cost)
    if premium_room_match is not None:
        days = premium_room_match.group(1)
        cost = premium_room_match.group(2)
        field_data['欄位名稱'].append(f'頂級房計{days}日')
        field_data['ocr辨識結果'].append(cost)

    for field_name, regex_pattern in field_regex_map.items():
        match = re.search(regex_pattern, text)
        if match is not None:
            field_data['欄位名稱'].append(field_name)
            field_data['ocr辨識結果'].append(match.group(1))
            
    new_df = pd.DataFrame(field_data)
    return new_df
    