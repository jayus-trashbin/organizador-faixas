"""
Módulo de Processamento e Regras de Negócio do Colgate Foco.
"""
import pandas as pd
import re
import os
from datetime import datetime
import shutil

def detect_pack_type(descricao: str) -> str | None:
    if not isinstance(descricao, str):
        return None
        
    descricao = descricao.upper()
    patterns = [r'L\d+P\d+', r'\d+UN', r'\d+PACK', r'\d+PK']
    words = ['DUO', 'TRIO', 'PACK']
    
    for pat in patterns:
        match = re.search(pat, descricao)
        if match:
            return match.group()
            
    for word in words:
        if f" {word} " in f" {descricao} ":
            return word
            
    return None

def consolidate(df_raw: pd.DataFrame) -> pd.DataFrame:
    if df_raw.empty:
        return pd.DataFrame()
        
    df_raw = df_raw.copy()
    df_raw['sku'] = df_raw['sku'].astype(str).str.strip()
    
    agg_funcs = {
        'ean': 'first',
        'descricao': 'first',
        'categoria': 'first',
        'faixa_origem': lambda x: sorted(list(set(x)))
    }
    
    for col in df_raw.columns:
        if col not in ['sku', 'ean', 'descricao', 'categoria', 'faixa_origem']:
            agg_funcs[col] = 'first'
            
    df_cons = df_raw.groupby('sku').agg(agg_funcs).reset_index()
    df_cons = df_cons.rename(columns={'faixa_origem': 'faixas'})
    
    df_cons['num_faixas'] = df_cons['faixas'].apply(len)
    total_faixas = df_raw['faixa_origem'].nunique()
    df_cons['is_critical'] = df_cons['num_faixas'] == total_faixas
    
    df_cons['is_pack'] = df_cons['descricao'].apply(lambda d: detect_pack_type(d) is not None)
    df_cons['favorito'] = False
    
    df_cons = df_cons.sort_values(['categoria', 'descricao'])
    
    return df_cons

def apply_filters(df: pd.DataFrame, faixas_sel: list, categorias_sel: list, busca: str, only_favs: bool, only_critical: bool) -> pd.DataFrame:
    if df.empty:
        return df
        
    filtered = df.copy()
    
    if faixas_sel:
        filtered = filtered[filtered['faixas'].apply(lambda x: any(f in x for f in faixas_sel))]
        
    if categorias_sel and "Todas" not in categorias_sel:
        filtered = filtered[filtered['categoria'].isin(categorias_sel)]
        
    if busca:
        busca = str(busca).lower()
        search_mask = (
            filtered['sku'].astype(str).str.lower().str.contains(busca) |
            filtered['ean'].astype(str).str.lower().str.contains(busca) |
            filtered['descricao'].astype(str).str.lower().str.contains(busca) |
            filtered['categoria'].astype(str).str.lower().str.contains(busca)
        )
        filtered = filtered[search_mask]
        
    if only_favs:
        filtered = filtered[filtered['favorito'] == True]
        
    if only_critical:
        filtered = filtered[filtered['is_critical'] == True]
        
    filtered = filtered.sort_values(by=['favorito', 'categoria', 'descricao'], ascending=[False, True, True])
    
    return filtered

def compare_faixas(df: pd.DataFrame, faixa_a: str, faixa_b: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if df.empty:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
        
    df_a = df[df['faixas'].apply(lambda faixas: faixa_a in faixas)]
    df_b = df[df['faixas'].apply(lambda faixas: faixa_b in faixas)]
    
    skus_a = set(df_a['sku'])
    skus_b = set(df_b['sku'])
    
    apenas_a_skus = skus_a - skus_b
    apenas_b_skus = skus_b - skus_a
    ambos_skus = skus_a.intersection(skus_b)
    
    apenas_a = df[df['sku'].isin(apenas_a_skus)]
    apenas_b = df[df['sku'].isin(apenas_b_skus)]
    ambos = df[df['sku'].isin(ambos_skus)]
    
    return apenas_a, apenas_b, ambos

def save_parquet(df: pd.DataFrame, path="data/base_consolidada.parquet"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.replace(".parquet", f"_backup_{timestamp}.parquet")
        shutil.copy2(path, backup_path)
        
    df.to_parquet(path, index=False)

def load_parquet(path="data/base_consolidada.parquet") -> pd.DataFrame | None:
    if os.path.exists(path):
        return pd.read_parquet(path)
    return None

import json

def save_favoritos(favoritos_set: set, path="data/favoritos.json"):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(list(favoritos_set), f)
    except Exception as e:
        print(f"Erro ao salvar favoritos: {e}")

def load_favoritos(path="data/favoritos.json") -> set:
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return set(data)
        except:
            pass
    return set()
