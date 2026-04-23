import pandas as pd
import numpy as np

def get_mock_dataframe() -> pd.DataFrame:
    """
    Retorna o dataframe MOCK consolidado baseado nos prints originais do projeto.
    Possui sobreposições reais, flags is_critical, is_pack e categorias.
    """
    data = [
        # AJAX
        {"sku": "17192", "ean": "7891024120804", "descricao": "17192 - LIMP AJAX PESADA FRESH LIMAO 500ML", "categoria": "AJAX", "faixas": ["FX1-2", "FX3", "FX4", "FX5"], "is_pack": False},
        {"sku": "17199", "ean": "7891024120705", "descricao": "17199 - LIMP AJAX PESADA FRESH 500ML", "categoria": "AJAX", "faixas": ["FX1-2", "FX4", "FX5"], "is_pack": False},
        {"sku": "121563", "ean": "7891024120712", "descricao": "121563 - LIMP AJAX PESADA FRESH 1L", "categoria": "AJAX", "faixas": ["FX1-2", "FX3", "FX4"], "is_pack": False},
        {"sku": "17194", "ean": "7891024120903", "descricao": "17194 - LIMP AJAX PESADA FRESH BLUE 500ML", "categoria": "AJAX", "faixas": ["FX1-2", "FX4"], "is_pack": False},
        {"sku": "152410", "ean": "7891024120767", "descricao": "152410 - LIMP AJAX PESADA FRESH LIMAO 1L", "categoria": "AJAX", "faixas": ["FX1-2", "FX3", "FX4"], "is_pack": False},
        {"sku": "27336", "ean": "7891024127605", "descricao": "27336 - LIMP AJAX PERF FES FLOR BOUQUET 500ML", "categoria": "AJAX", "faixas": ["FX1-2", "FX4", "FX5"], "is_pack": False},
        {"sku": "311102", "ean": "7891024128312", "descricao": "311102 - LIMP AJAX PERF FEST FLOR LAVANDA 1LT", "categoria": "AJAX", "faixas": ["FX1-2", "FX3", "FX4"], "is_pack": False},
        {"sku": "534346", "ean": "7509546691251", "descricao": "534346 - LIMP AJAX PERF FESTA DAS FLORES 500ML", "categoria": "AJAX", "faixas": ["FX4", "FX5"], "is_pack": False},
        {"sku": "25544", "ean": "7891024128305", "descricao": "25544 - LIMP AJAX PERF FES FLOR LAVANDA 500ML", "categoria": "AJAX", "faixas": ["FX1-2", "FX4", "FX5"], "is_pack": False},

        # BS NATURALS
        {"sku": "240492", "ean": "7891024027523", "descricao": "240492 - SAB PALM SUAVE GELEIA REAL 150G", "categoria": "BS NATURALS", "faixas": ["FX4", "FX5"], "is_pack": False},
        {"sku": "202132", "ean": "7891024026458", "descricao": "202132 - SAB PALM SUAVE TQ RADIANTE TURMALIN 150G", "categoria": "BS NATURALS", "faixas": ["FX4", "FX5"], "is_pack": False},
        {"sku": "265543", "ean": "7891024029824", "descricao": "265543 - SAB PALM SUAVE OLEO NUTRITIVO 150G", "categoria": "BS NATURALS", "faixas": ["FX4", "FX5"], "is_pack": False},
        {"sku": "301308", "ean": "7891024035580", "descricao": "301308 - SAB PALM SUAVE ESFOL DELICADA 150G", "categoria": "BS NATURALS", "faixas": ["FX4", "FX5"], "is_pack": False},
        {"sku": "9906", "ean": "7891024110201", "descricao": "9906 - SAB PALM SUAVE OLEO OLIVA 150G", "categoria": "BS NATURALS", "faixas": ["FX4", "FX5"], "is_pack": False},
        {"sku": "13146", "ean": "7891024110300", "descricao": "13146 - SAB PALM SUAVE HIDRAT INT KARITE 150G", "categoria": "BS NATURALS", "faixas": ["FX4", "FX5"], "is_pack": False},
        {"sku": "183477", "ean": "7891024110355", "descricao": "183477 - SAB PALM SUAVE OLEO ARGAN 150G", "categoria": "BS NATURALS", "faixas": ["FX4", "FX5"], "is_pack": False},
        {"sku": "13467", "ean": "7891024110508", "descricao": "13467 - SAB PALM SUAVE LEITE PET ROSA 150G", "categoria": "BS NATURALS", "faixas": ["FX4", "FX5"], "is_pack": False},
        {"sku": "519781", "ean": "7509546669687", "descricao": "519781 - SAB PALM SUAVE MELANCIA E LICHIA 150G", "categoria": "BS NATURALS", "faixas": ["FX4", "FX5"], "is_pack": False},
        
        # BS PROTEX
        {"sku": "325106", "ean": "7891024034910", "descricao": "325106 - SAB PROTEX ANT AVEIA 85G", "categoria": "BS PROTEX", "faixas": ["FX3", "FX4", "FX5"], "is_pack": False},
        {"sku": "325105", "ean": "7891024034996", "descricao": "325105 - SAB PROTEX ANT BALANCE 85G", "categoria": "BS PROTEX", "faixas": ["FX3", "FX4", "FX5"], "is_pack": False},
        {"sku": "325104", "ean": "7891024035047", "descricao": "325104 - SAB PROTEX ANT LIMP PROF 85G", "categoria": "BS PROTEX", "faixas": ["FX3", "FX4", "FX5"], "is_pack": False},
        {"sku": "475469", "ean": "7509546678832", "descricao": "475469 - SAB PROTEX CARVAO DETOX 85G", "categoria": "BS PROTEX", "faixas": ["FX4", "FX5"], "is_pack": False},
        {"sku": "325101", "ean": "7891024035078", "descricao": "325101 - SAB PROTEX ANT CREAM 85G", "categoria": "BS PROTEX", "faixas": ["FX4", "FX5"], "is_pack": False},
        {"sku": "325094", "ean": "7891024035139", "descricao": "325094 - SAB PROTEX ANT VITAMINA E 85G", "categoria": "BS PROTEX", "faixas": ["FX4", "FX5"], "is_pack": False},
        {"sku": "325108", "ean": "7891024035191", "descricao": "325108 - SAB PROTEX ANT COMPLETE 12 85G", "categoria": "BS PROTEX", "faixas": ["FX4", "FX5"], "is_pack": False},
        {"sku": "325099", "ean": "7891024035207", "descricao": "325099 - SAB PROTEX ANT OMEGA 3 85G", "categoria": "BS PROTEX", "faixas": ["FX4", "FX5"], "is_pack": False},
        
        # CREMES DENTAIS
        {"sku": "503947", "ean": "7509546687926", "descricao": "503947 - CR D COLGATE ANTICARIE 120G", "categoria": "CD COLGATE MPA 120G", "faixas": ["FX1-2", "FX3"], "is_pack": False},
        {"sku": "416087", "ean": "7509546657738", "descricao": "416087 - CR D COLGATE TOTAL 12 ANTITARTARO 180G", "categoria": "CD COLGATE TOTAL 180G", "faixas": ["FX1-2"], "is_pack": False},
        {"sku": "322933", "ean": "7891024037973", "descricao": "322933 - CR D COLGATE TR A ORIG PRECO ESP 180G", "categoria": "CD COLGATE TRIPLA AÇÃO 180G", "faixas": ["FX1-2", "FX3"], "is_pack": False},
        {"sku": "496744", "ean": "7509546665306", "descricao": "496744 - CR D COLGATE LUMINOUS WHI CARV 140G", "categoria": "CD LUMINOUS 140G", "faixas": ["FX1-2"], "is_pack": False},
        {"sku": "433627", "ean": "7509546667638", "descricao": "433627 - CR D SORRISO TR LIMP COMP PCO ESP 120G", "categoria": "CD SORRISO TRIPLA LIMP COMPLETA 120G", "faixas": ["FX1-2", "FX3"], "is_pack": False},
        {"sku": "459875", "ean": "7509546675121", "descricao": "459875 - CR D SORRISO CARVAO ATIVADO 60G", "categoria": "CD CARVÃO", "faixas": ["FX4", "FX5"], "is_pack": False},
        
        # ESCOVAS E PACKS
        {"sku": "201469", "ean": "7891024026434", "descricao": "201469 - ESC DENTAL COLG CLASS CLEAN L3P2", "categoria": "ED COLGATE CLASSIC 3 PACK", "faixas": ["FX1-2", "FX3"], "is_pack": True},
        {"sku": "222249", "ean": "7509546061689", "descricao": "222249 - ESC DENTAL COLG SLIM SOFT BLAC L2P1", "categoria": "ED COLGATE SLIM SOFT BLACK 2 PACK", "faixas": ["FX1-2", "FX3"], "is_pack": True},
        {"sku": "503950", "ean": "7509546673042", "descricao": "503950 - ESC DENTAL COLGATE ZIG ZAG CHARCOAL 2UN", "categoria": "ED COLGATE ZIG ZAG 2PK", "faixas": ["FX3"], "is_pack": True},

        # OUTROS
        {"sku": "269587", "ean": "7891024027622", "descricao": "269587 - ENXAG BUCAL COLG ICE INF L500P350ML", "categoria": "ENXAGUANTE 500ML", "faixas": ["FX3"], "is_pack": True},
        {"sku": "152390", "ean": "7891024128596", "descricao": "152390 - LAVA ROU OLA BEBE 1L", "categoria": "OLA", "faixas": ["FX3"], "is_pack": False},
        {"sku": "1054", "ean": "7891024194102", "descricao": "1054 - DESINF PINHO SOL ORIG 500ML", "categoria": "PINHO SOL", "faixas": ["FX3"], "is_pack": False},
        {"sku": "92562", "ean": "7891024194607", "descricao": "92562 - DESINF PINHO SOL ORIG 1L", "categoria": "PINHO SOL", "faixas": ["FX3"], "is_pack": False},
        {"sku": "13014", "ean": "7891024193006", "descricao": "13014 - DESINF PINHO SOL LAVANDA 500ML", "categoria": "PINHO SOL", "faixas": ["FX3"], "is_pack": False},
    ]
    
    df = pd.DataFrame(data)
    df['num_faixas'] = df['faixas'].apply(len)
    total_faixas = 4 # FX1-2, FX3, FX4, FX5
    df['is_critical'] = df['num_faixas'] == total_faixas
    df['favorito'] = False
    
    return df
