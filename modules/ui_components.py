"""
Componentes da Interface de Usuário (Streamlit)
"""
import pandas as pd
import streamlit as st

def render_header(ultima_atualizacao: str | None):
    st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <h1 style="color: #E3001B; margin-bottom: 0;">Colgate Foco</h1>
            <p style="color: #888; font-size: 1.1em;">Sua lista de itens foco, sempre à mão.</p>
        </div>
    """, unsafe_allow_html=True)
    
    if ultima_atualizacao:
        st.markdown(f"<p style='text-align: center; color: #666; font-size: 0.8em;'>Última atualização: {ultima_atualizacao}</p>", unsafe_allow_html=True)
        
    st.divider()

def render_onboarding():
    """First-run screen shown when no PDF data exists yet."""
    import modules.parser as parser
    import modules.processor as processor
    
    st.markdown("""
        <div style="text-align: center; padding: 40px 20px;">
            <h2 style="color: #CBD5E1;">Bem-vindo ao Colgate Foco!</h2>
            <p style="color: #94A3B8; font-size: 1.1em; max-width: 500px; margin: 0 auto;">
                Para começar, carregue os PDFs dos Itens Foco enviados pela Colgate.
                Isso leva menos de 1 minuto.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("#### Passo 1: Selecione os arquivos PDF")
        uploaded_files = st.file_uploader(
            "Arraste os PDFs da Colgate aqui",
            accept_multiple_files=True,
            type=["pdf"],
            help="Selecione todos os PDFs das faixas de uma só vez (FX 1-2, FX 3, FX 4 e FX 5).",
            key="onboarding_upload"
        )
        
        if uploaded_files:
            nomes = ", ".join([f.name for f in uploaded_files])
            st.caption(f"{len(uploaded_files)} arquivo(s): {nomes}")
            st.markdown("#### Passo 2: Confirme o carregamento")
            
            if st.button("Carregar e iniciar", type="primary", use_container_width=True, icon=":material/rocket_launch:"):
                with st.spinner("Lendo os PDFs... Isso pode levar alguns segundos."):
                    df_novo_bruto, warnings_list = parser.parse_pdfs(uploaded_files, {})
                    
                    for w in warnings_list:
                        st.toast(f"Atenção: {w}", icon="⚠️")
                    
                    if not df_novo_bruto.empty:
                        df_consolidado = processor.consolidate(df_novo_bruto)
                        processor.save_parquet(df_consolidado)
                        st.success(f"Pronto! {len(df_consolidado)} produtos carregados com sucesso.", icon=":material/check_circle:")
                        import time
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Não encontrei nenhum produto nos arquivos. Verifique se os PDFs são os corretos da Colgate.")

def render_sidebar(categorias: list) -> dict:
    st.sidebar.header(":material/tune: Filtros")
    
    st.sidebar.subheader("Faixas de Loja")
    col1, col2 = st.sidebar.columns(2)
    fx1_2 = col1.checkbox("FX 1-2", value=True)
    fx3 = col2.checkbox("FX 3", value=True)
    fx4 = col1.checkbox("FX 4", value=True)
    fx5 = col2.checkbox("FX 5", value=True)
    
    faixas_sel = []
    if fx1_2: faixas_sel.append("FX1-2")
    if fx3: faixas_sel.append("FX3")
    if fx4: faixas_sel.append("FX4")
    if fx5: faixas_sel.append("FX5")

    st.sidebar.divider()
    
    st.sidebar.subheader("Linha de Produto")
    todas_categorias = ["Todas"] + list(categorias)
    categorias_sel = st.sidebar.multiselect("Selecione as linhas", options=todas_categorias, default=["Todas"])
    
    return {
        "faixas": faixas_sel,
        "categorias": categorias_sel,
    }

def render_quick_filters() -> dict:
    st.markdown("<br>", unsafe_allow_html=True)
    c_busca, c_modo, c_fav, c_crit = st.columns([2.5, 1.5, 1.2, 1.2])
    
    with c_busca:
        busca = st.text_input("Busca", "", placeholder="Buscar por produto, código ou linha...", label_visibility="collapsed")
    
    with c_modo:
        modo = st.radio("Visão", ["Venda", "Logística"], horizontal=True, label_visibility="collapsed")
        
    with c_fav:
        only_favs = st.toggle("Meus Favoritos", value=False, help="Mostra só os produtos que você marcou como favorito.")
        
    with c_crit:
        only_critical = st.toggle("Só Críticos", value=False, help="Mostra apenas os itens prioritários que estão em todas as faixas.")
        
    return {
        "busca": busca,
        "modo": "vendas" if "Venda" in modo else "logistica",
        "only_favs": only_favs,
        "only_critical": only_critical
    }

def render_kpi_cards(df_filtered: pd.DataFrame, df_total: pd.DataFrame):
    col1, col2, col3, col4 = st.columns(4)
    
    total_skus = len(df_filtered)
    total_skus_geral = len(df_total)
    
    criticos = df_filtered['is_critical'].sum() if not df_filtered.empty else 0
    criticos_geral = df_total['is_critical'].sum() if not df_total.empty else 0
    
    packs = df_filtered['is_pack'].sum() if not df_filtered.empty else 0
    unitarios = total_skus - packs
    
    cat_ativas = df_filtered['categoria'].nunique() if not df_filtered.empty else 0
    cat_total = df_total['categoria'].nunique() if not df_total.empty else 0
    
    col1.metric(":material/inventory_2: Total de Produtos", total_skus, f"{total_skus - total_skus_geral} filtrado" if total_skus != total_skus_geral else None)
    col2.metric(":material/priority_high: Itens Prioritários", int(criticos), f"{int(criticos - criticos_geral)} filtrado" if criticos != criticos_geral else None)
    col3.metric(":material/view_in_ar: Packs / Unitários", f"{int(packs)} / {int(unitarios)}")
    col4.metric(":material/category: Linhas Ativas", cat_ativas, f"{cat_ativas - cat_total} filtrado" if cat_ativas != cat_total else None)

def render_tabela(df_filtered: pd.DataFrame, modo: str, state_key: str) -> pd.DataFrame:
    if df_filtered.empty:
        st.info("**Nenhum produto encontrado.**\n\nTente ajustar os filtros:\n- Marque mais faixas na barra lateral\n- Limpe o campo de busca\n- Desative os botões 'Só Críticos' ou 'Meus Favoritos'", icon=":material/search_off:")
        return pd.DataFrame()
        
    df_view = df_filtered.copy()
    
    # Enrich Data
    df_view['Prioridade'] = df_view['is_critical'].apply(lambda x: "★ Prioritário" if x else "")
    df_view['Faixas'] = df_view['faixas'].apply(lambda x: " · ".join(x))
    df_view['Cobertura'] = df_view['faixas'].apply(lambda x: len(x))
    df_view['Tipo'] = df_view['is_pack'].apply(lambda x: "Pack" if x else "Unitário")
    
    # Sort logically
    df_view = df_view.sort_values(by=['categoria', 'is_critical', 'Cobertura', 'descricao'], ascending=[True, False, False, True])
    
    # Strip prefix from description
    def clear_desc(row):
        desc = str(row.get('descricao', ''))
        sku_prefix = str(row.get('sku', '')) + ' - '
        if desc.startswith(sku_prefix):
            return desc[len(sku_prefix):]
        return desc
    df_view['descricao'] = df_view.apply(clear_desc, axis=1)
    
    if modo == "vendas":
        cols = ['favorito', 'Prioridade', 'sku', 'categoria', 'descricao', 'Cobertura', 'Faixas']
    else:
        cols = ['favorito', 'Prioridade', 'sku', 'ean', 'categoria', 'Tipo', 'Cobertura', 'Faixas']
        
    df_view = df_view[cols]
    
    st.caption(f"{len(df_view)} produto(s) encontrado(s)")
    
    def highlight_critical(row):
        return ['background-color: rgba(227, 0, 27, 0.08); color: #C00000' if row['Prioridade'] else ''] * len(row)
        
    styled_df = df_view.style.apply(highlight_critical, axis=1)
    
    edited_df = st.data_editor(
        styled_df,
        column_config={
            "favorito": st.column_config.CheckboxColumn("Favorito", help="Marque para salvar nos seus favoritos", default=False),
            "Prioridade": st.column_config.TextColumn("Status", help="Produtos prioritários estão em todas as faixas", width="small"),
            "sku": st.column_config.TextColumn("Código", help="Código do produto", width="small"),
            "categoria": st.column_config.TextColumn("Linha", width="medium"),
            "descricao": st.column_config.TextColumn("Produto", help="Nome do produto", width="large"),
            "Cobertura": st.column_config.ProgressColumn("Cob.", format="%f / 4", min_value=0, max_value=4, help="Número de faixas em que este produto pontua"),
            "Faixas": st.column_config.TextColumn("Faixas", help="Faixas de loja onde este produto é foco", width="medium"),
            "Tipo": st.column_config.TextColumn("Formato", help="Pack (embalagem múltipla) ou unitário"),
            "ean": st.column_config.TextColumn("Cód. de Barras")
        },
        disabled=["Prioridade", "sku", "categoria", "descricao", "Cobertura", "Faixas", "Tipo", "ean"],
        hide_index=True,
        key=state_key,
        width="stretch"
    )
    
    return edited_df
