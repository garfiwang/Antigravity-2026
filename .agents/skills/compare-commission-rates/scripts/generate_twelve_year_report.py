import pdfplumber
import os
import re

folder_path = "/Users/garfiwang/Documents/Antigravity-2026/壽險佣金-2026"
files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]

date_pattern = re.compile(r'\d{4}/\d{2}/\d{2}')
age_pattern = re.compile(r'(\d+~\d+|\d+~|~\d+)')
insurance_keywords = ["壽險", "保險", "附約", "年金", "健康", "傷害", "定期", "終身", "防癌", "醫療", "養老"]

def is_float(val):
    try:
        if '.' not in val:
            return False
        float(val)
        return True
    except ValueError:
        return False

def contains_12_year(term_str):
    if term_str == '12':
        return True
    range_match = re.match(r'(\d+)~(\d+)', term_str)
    if range_match:
        start = int(range_match.group(1))
        end = int(range_match.group(2))
        if start <= 12 <= end:
            return True
    return False

def process_rates(rates_list):
    processed = []
    for part in rates_list:
        if part == "-":
            processed.append("-")
        else:
            floats = re.findall(r'\d+\.\d{2}', part)
            if floats:
                processed.extend(floats)
            else:
                processed.append(part)
    return processed

def extract_names_and_data(filepath):
    code_to_name = {}
    data_rows = []
    
    with pdfplumber.open(filepath) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue
            lines = text.split('\n')
            
            standalone_names = []
            data_lines = []
            
            for line_idx, line in enumerate(lines):
                parts = line.split()
                if not parts:
                    continue
                
                has_date = any(date_pattern.match(p) for p in parts)
                has_chinese = any(any('\u4e00' <= char <= '\u9fff' for char in word) for word in parts)
                has_float = any(is_float(p) for p in parts)
                
                if not has_date and not has_float and has_chinese:
                    candidate_name = " ".join(parts).strip()
                    if any(k in candidate_name for k in insurance_keywords):
                        if not any(h in candidate_name for h in ["險種名稱", "製表日期", "初年度", "續年度", "特別報酬率", "業績換算率", "人壽商品"]):
                            standalone_names.append((line_idx, candidate_name))
                
                if has_date:
                    date_idx = -1
                    for idx, part in enumerate(parts):
                        if date_pattern.match(part):
                            date_idx = idx
                            break
                    
                    if date_idx > 0:
                        code = parts[date_idx - 1]
                        name_parts = parts[:date_idx - 1]
                        name = " ".join(name_parts).strip()
                        data_lines.append((line_idx, code, name))
            
            for line_idx, code, name in data_lines:
                if name and any('\u4e00' <= char <= '\u9fff' for char in name) and not any(h in name for h in ["險種名稱", "險種代號"]):
                    code_to_name[code] = name
                else:
                    for s_idx, s_name in standalone_names:
                        if abs(s_idx - line_idx) <= 2:
                            code_to_name[code] = s_name
                            break
                            
    with pdfplumber.open(filepath) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue
            lines = text.split('\n')
            
            for line_idx, line in enumerate(lines):
                parts = line.split()
                if not parts:
                    continue
                
                has_date = any(date_pattern.match(p) for p in parts)
                if not has_date:
                    continue
                
                float_idx = -1
                for idx, part in enumerate(parts):
                    if is_float(part):
                        float_idx = idx
                        break
                
                if float_idx > 0:
                    term = parts[float_idx - 1]
                    rate = parts[float_idx]
                    
                    date_idx = -1
                    for idx, part in enumerate(parts[:float_idx]):
                        if date_pattern.match(part):
                            date_idx = idx
                            break
                    
                    if date_idx > 0:
                        code = parts[date_idx - 1]
                        start_date = parts[date_idx]
                        
                        middle_parts = parts[date_idx + 1: float_idx - 1]
                        
                        end_date = "-"
                        age = "-"
                        other_conditions = "-"
                        
                        for p in middle_parts:
                            if date_pattern.match(p):
                                end_date = p
                            elif age_pattern.match(p):
                                age = p
                            elif p != "-":
                                other_conditions = p
                                
                        name = code_to_name.get(code, "")
                        raw_renewal = parts[float_idx + 1:]
                        renewal_rates = process_rates(raw_renewal)
                        
                        data_rows.append({
                            "name": name,
                            "code": code,
                            "start_date": start_date,
                            "end_date": end_date,
                            "age": age,
                            "other_conditions": other_conditions,
                            "term": term,
                            "rate": rate,
                            "renewal_rates": renewal_rates,
                            "page": i + 1,
                            "line": line_idx + 1
                        })
                        
    return data_rows

# Columns definitions for each insurance company
company_columns = {
    "保誠人壽": {
        "headers": ["險種名稱", "險種代號", "起賣日", "停賣日", "年齡", "其他條件", "繳費年期", "初年度業績換算率", "實際首年佣金率(FYC%)", "續2", "續3", "續4", "續5", "續6", "續7~9", "續10", "續11~20", "續21~滿", "特7", "特8~10", "特11~12", "特13~15", "特16~20", "特期滿"],
        "renewal_cols_count": 15
    },
    "元大人壽": {
        "headers": ["險種名稱", "險種代號", "起賣日", "停賣日", "年齡", "其他條件", "繳費年期", "初年度業績換算率", "實際首年佣金率(FYC%)", "續2", "續3", "續4", "續5", "續6", "續7~25", "續26~滿", "續31~滿", "特7~10", "特11~12", "特13~15", "特16~20", "特21~30"],
        "renewal_cols_count": 13
    },
    "全球人壽": {
        "headers": ["險種名稱", "險種代號", "起賣日", "停賣日", "年齡", "其他條件", "繳費年期", "初年度業績換算率", "實際首年佣金率(FYC%)", "續2", "續3", "續4", "續5", "續6", "續7~30", "續31~滿", "特7~14", "特15~19", "特20~期滿"],
        "renewal_cols_count": 10
    },
    "安達人壽": {
        "headers": ["險種名稱", "險種代號", "起賣日", "停賣日", "年齡", "其他條件", "繳費年期", "初年度業績換算率", "實際首年佣金率(FYC%)", "續2", "續3", "續4", "續5", "續6", "續7~10", "續11~20", "續21~滿", "特7~10", "特11~期滿"],
        "renewal_cols_count": 10
    },
    "遠雄人壽": {
        "headers": ["險種名稱", "險種代號", "起賣日", "停賣日", "年齡", "其他條件", "繳費年期", "初年度業績換算率", "實際首年佣金率(FYC%)", "續2", "續3", "續4", "續5", "續6", "續7~10", "續11~12", "續13~20", "續21~滿", "續31~滿", "特7~10", "特11~14", "特15", "特16~17", "特18~19", "特20", "特21~25", "特26~30", "特期滿"],
        "renewal_cols_count": 19
    }
}

file_to_company = {
    "保誠人壽-20260626.pdf": "保誠人壽",
    "元大人壽-20260626.pdf": "元大人壽",
    "全球人壽-20260626.pdf": "全球人壽",
    "安達人壽 - 202605.pdf": "安達人壽",
    "遠雄人壽-20260626.pdf": "遠雄人壽"
}

if __name__ == "__main__":
    # First, extract and filter all data
    all_filtered_data = {}
    global_max_fyc = 0.0
    global_max_item = None
    company_max_fyc = {}
    
    for filename in sorted(files):
        company_name = file_to_company[filename]
        filepath = os.path.join(folder_path, filename)
        rows = extract_names_and_data(filepath)
        
        # Filter 12-year term
        filtered_rows = [r for r in rows if contains_12_year(r["term"])]
        
        all_filtered_data[company_name] = filtered_rows
        
        # Find max for this company
        local_max = 0.0
        for r in filtered_rows:
            fyc = float(r["rate"]) * 0.4
            if fyc > local_max:
                local_max = fyc
            if fyc > global_max_fyc:
                global_max_fyc = fyc
                global_max_item = {
                    "company": company_name,
                    "name": r["name"],
                    "code": r["code"],
                    "fyc": fyc
                }
        company_max_fyc[company_name] = local_max
    
    print(f"Global max: {global_max_fyc}%")
    if global_max_item:
        print(f"Global max item: {global_max_item}")
    print(f"Company maxes: {company_max_fyc}")
    
    # Generate report content
    markdown_content = []
    markdown_content.append("# 十二年期壽險商品佣金率列表 (已更新商品與高亮)\n")
    markdown_content.append("本列表彙整了資料夾內所有保險公司 PDF 檔案中，繳費年期為 **12年期**（或包含12年的年期範圍，例如 10~15年）的商品。每個公司的表格欄位均與原始檔案完全一致。\n")
    markdown_content.append("> [!IMPORTANT]")
    markdown_content.append("> 1. **各家保險公司自己旗下首年實際佣金率 (FYC%) 最高之項目已使用 <span style='color:red; font-weight:bold;'>紅字粗體</span> 表示。**")
    markdown_content.append("> 2. **初年度服務報酬 (實際首年佣金率 FYC%) = 初年度保費 × 初年度業績換算率 × 40%**\n")
    
    for filename in sorted(files):
        company_name = file_to_company[filename]
        filtered_rows = all_filtered_data[company_name]
        local_max = company_max_fyc.get(company_name, 0.0)
        
        markdown_content.append(f"## {company_name} ({filename})\n")
        
        if not filtered_rows:
            markdown_content.append("無符合條件之十二年期商品。\n")
            continue
            
        config = company_columns[company_name]
        headers = config["headers"]
        renewal_count = config["renewal_cols_count"]
        
        markdown_content.append("| " + " | ".join(headers) + " |")
        markdown_content.append("| " + " | ".join([":---" if i == 0 else ":---:" for i in range(len(headers))]) + " |")
        
        for row in filtered_rows:
            rate_val = float(row["rate"])
            fyc_val = rate_val * 0.4
            
            # Check if this row is the local max for this company
            is_local_max = abs(fyc_val - local_max) < 1e-6 and local_max > 0
            
            if is_local_max:
                fyc_str = f"<span style='color:red; font-weight:bold;'>{fyc_val:.2f}%</span>"
                rate_str = f"<span style='color:red; font-weight:bold;'>{rate_val:.2f}%</span>"
            else:
                fyc_str = f"{fyc_val:.2f}%"
                rate_str = f"{rate_val:.2f}%"
                
            row_renewals = row["renewal_rates"]
            if len(row_renewals) < renewal_count:
                row_renewals = row_renewals + ["-"] * (renewal_count - len(row_renewals))
            elif len(row_renewals) > renewal_count:
                row_renewals = row_renewals[:renewal_count]
                
            formatted_renewals = []
            for val in row_renewals:
                if val != "-" and val != "":
                    try:
                        formatted_renewals.append(f"{float(val):.2f}%")
                    except ValueError:
                        formatted_renewals.append(val)
                else:
                    formatted_renewals.append("-")
                    
            disp_name = f"**{row['name']}**" if row['name'] else "-"
            if is_local_max:
                disp_name = f"<span style='color:red; font-weight:bold;'>{row['name']}</span>"
                
            row_data = [
                disp_name,
                f"`{row['code']}`" if not is_local_max else f"<span style='color:red; font-weight:bold;'>`{row['code']}`</span>",
                row["start_date"],
                row["end_date"],
                row["age"],
                row["other_conditions"],
                row["term"],
                rate_str,
                fyc_str,
            ] + formatted_renewals
            
            markdown_content.append("| " + " | ".join(row_data) + " |")
            
        markdown_content.append("\n")
    
    # Write report to workspace
    output_file = "/Users/garfiwang/Documents/Antigravity-2026/壽險佣金-2026/十二年期商品佣金率列表.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(markdown_content))
    
    print(f"Report successfully written to: {output_file}")
