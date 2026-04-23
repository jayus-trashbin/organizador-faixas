"""
Módulo de Parser para PDFs do Colgate Foco.
"""
import pandas as pd
import pdfplumber
import re

def detect_faixa_from_title(pdf_stream) -> str | None:
    try:
        with pdfplumber.open(pdf_stream) as pdf:
            if len(pdf.pages) > 0:
                first_page = pdf.pages[0]
                text = first_page.extract_text()
                if text:
                    # Regex FX 1-2, FX 3, FX4, etc (case insensitive)
                    match = re.search(r'FX\s?(\d(?:[-–]\d)?|\d)', text, re.IGNORECASE)
                    if match:
                        return f"FX{match.group(1).replace(' ', '')}"
    except Exception as e:
        print(f"Erro ao detectar faixa: {e}")
    return None

def clean_string(s):
    if not isinstance(s, str): return ""
    return str(s).strip().upper()

def extract_table_from_pdf(pdf_stream) -> tuple[pd.DataFrame, list[str]]:
    warnings = []
    final_rows = []
    columns_map = None
    
    try:
        with pdfplumber.open(pdf_stream) as pdf:
            for page_num, page in enumerate(pdf.pages):
                table = page.extract_table()
                if not table:
                    continue
                
                start_row_idx = 0
                for r_idx, row in enumerate(table):
                    row_upper = [clean_string(v) for v in row]
                    
                    if "SKU" in row_upper and "EAN" in row_upper:
                        start_row_idx = r_idx + 1
                        
                        if columns_map is None:
                            try:
                                sku_idx = row_upper.index("SKU")
                                ean_idx = row_upper.index("EAN")
                                
                                cat_idx = -1
                                for i, v in enumerate(row_upper):
                                    if "GRUPO" in v or "CATEGORIA" in v:
                                        cat_idx = i
                                        break
                                if cat_idx == -1: cat_idx = 0
                                
                                desc_idx = -1
                                for i, v in enumerate(row_upper):
                                    if "DESCRI" in v:
                                        desc_idx = i
                                        break
                                if desc_idx == -1: desc_idx = 3
                                
                                columns_map = {
                                    'categoria_idx': cat_idx,
                                    'sku_idx': sku_idx,
                                    'ean_idx': ean_idx,
                                    'descricao_idx': desc_idx
                                }
                            except ValueError:
                                warnings.append(f"Página {page_num+1}: Formato da tabela de colunas divergente.")
                        break
                
                if columns_map is None:
                    continue
                
                for row in table[start_row_idx:]:
                    if not row or all(v is None for v in row): continue
                    
                    try:
                        cat_val = row[columns_map['categoria_idx']] if len(row) > columns_map['categoria_idx'] else None
                        sku_val = row[columns_map['sku_idx']] if len(row) > columns_map['sku_idx'] else None
                        ean_val = row[columns_map['ean_idx']] if len(row) > columns_map['ean_idx'] else None
                        desc_val = row[columns_map['descricao_idx']] if len(row) > columns_map['descricao_idx'] else None
                        
                        sku_str = str(sku_val).strip() if sku_val else ""
                        if sku_str.upper() == "SKU" or "SKUS" in sku_str.upper() or not sku_str:
                            continue
                            
                        final_rows.append({
                            'categoria': str(cat_val).replace('\n', ' ').strip() if cat_val else "",
                            'sku': sku_str,
                            'ean': str(ean_val).strip() if ean_val else "",
                            'descricao': str(desc_val).replace('\n', ' ').strip() if desc_val else ""
                        })
                    except Exception:
                        pass
                        
        df = pd.DataFrame(final_rows)
        if df.empty:
            warnings.append("Nenhuma linha útil capturada desta faixa.")
        return df, warnings
    except Exception as e:
        warnings.append(f"PDF corrompido ou protegido: {str(e)}")
        return pd.DataFrame(), warnings

def parse_pdfs(uploaded_files: list, faixa_map: dict) -> tuple[pd.DataFrame, list[str]]:
    all_dfs = []
    super_warnings = []
    
    for file in uploaded_files:
        filename = file.name
        file.seek(0)
        faixa = detect_faixa_from_title(file)
        
        if not faixa:
            faixa = faixa_map.get(filename, "Desconhecida")
            
        file.seek(0)
        df, warnings = extract_table_from_pdf(file)
        
        for w in warnings:
            super_warnings.append(f"[{filename}] {w}")
            
        if not df.empty:
            df['faixa_origem'] = faixa
            all_dfs.append(df)
            
    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True), super_warnings
    
    return pd.DataFrame(), super_warnings
