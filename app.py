import streamlit as st
import pandas as pd
import os
from datetime import datetime

import modules.ui_components as ui
import modules.processor as processor
import modules.parser as parser
from mock.mock_data import get_mock_dataframe
import modules.theme as theme

def init_session_state():
    if 'favoritos' not in st.session_state:
        st.session_state.favoritos = processor.load_favoritos()

def load_data():
    df = processor.load_parquet()
    if df is not None:
        file_stats = os.stat("data/base_consolidada.parquet")
        last_modified = datetime.fromtimestamp(file_stats.st_mtime).strftime("%d/%m/%Y")
        return df, last_modified, False
    else:
        return None, None, True

def main():
    st.set_page_config(
        page_title="Colgate Foco",
        layout="wide"
    )
    theme.inject_custom_css()
    
    init_session_state()
    
    df_base, ultima_atualizacao, precisa_configurar = load_data()
    
    # First-run: guide the rep to upload PDFs
    if precisa_configurar:
        ui.render_header(None)
        ui.render_onboarding()
        return
        
    if df_base is None or df_base.empty:
        st.error("Não foi possível carregar os dados. Reinicie o aplicativo.")
        return
        
    categorias_unicas = sorted(df_base['categoria'].dropna().unique())
    
    filtros = ui.render_sidebar(categorias_unicas)
    
    ui.render_header(ultima_atualizacao)
        
    tab_painel, tab_comparativo, tab_upload = st.tabs([
        ":material/dashboard: Meus Itens Foco",
        ":material/compare_arrows: Evolução de Loja",
        ":material/refresh: Atualizar Lista"
    ])
    
    with tab_painel:
        quick_filtros = ui.render_quick_filters()
        # Merge quick filters preserving sidebar 'faixas' and 'categorias'
        for k, v in quick_filtros.items():
            filtros[k] = v
        
        df_base['favorito'] = df_base['sku'].isin(st.session_state.favoritos)
        
        df_filtered = processor.apply_filters(
            df=df_base,
            faixas_sel=filtros.get('faixas', []),
            categorias_sel=filtros.get('categorias', []),
            busca=filtros.get('busca', ''),
            only_favs=filtros.get('only_favs', False),
            only_critical=filtros.get('only_critical', False)
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        ui.render_kpi_cards(df_filtered, df_base)
        st.markdown("<br>", unsafe_allow_html=True)
        tab_tabela, tab_analytics = st.tabs([":material/table_chart: Lista de Produtos", ":material/monitoring: Resumo Visual"])
        
        with tab_tabela:
            edited_df = ui.render_tabela(df_filtered, filtros['modo'], state_key="tabela_principal")
            
            if edited_df is not None and not edited_df.empty:
                novos_favoritos = edited_df[edited_df['favorito'] == True]['sku'].tolist()
                desmarcados = edited_df[edited_df['favorito'] == False]['sku'].tolist()
                
                mudou = False
                for f in novos_favoritos:
                    if f not in st.session_state.favoritos:
                        st.session_state.favoritos.add(f)
                        mudou = True
                for d in desmarcados:
                    if d in st.session_state.favoritos:
                        st.session_state.favoritos.discard(d)
                        mudou = True
                        
                if mudou:
                    processor.save_favoritos(st.session_state.favoritos)

            if not df_base.empty:
                st.markdown("<br>", unsafe_allow_html=True)
                with st.expander(":material/print: Configurar e Exportar PDF", expanded=False):
                    st.caption("Escolha quais itens entrarão no relatório independentemente da tabela.")
                    
                    c1, c2 = st.columns(2)
                    pdf_faixas_default = [f for f in (filtros.get('faixas') or []) if f in ["FX1-2", "FX3", "FX4", "FX5"]]
                    if not pdf_faixas_default:
                        pdf_faixas_default = ["FX1-2", "FX3", "FX4", "FX5"]
                    pdf_faixas = c1.multiselect("Faixas das Lojas", options=["FX1-2", "FX3", "FX4", "FX5"], default=pdf_faixas_default, key="pdf_fx")
                    
                    cats_disp = sorted(df_base['categoria'].unique().tolist())
                    pdf_cats_default = [c for c in (filtros.get('categorias') or []) if c in cats_disp]
                    if not pdf_cats_default:
                        pdf_cats_default = cats_disp
                    pdf_cats = c2.multiselect("Categorias / Linhas", options=cats_disp, default=pdf_cats_default, key="pdf_cat")
                    
                    c3, c4 = st.columns(2)
                    apenas_criticos = c3.checkbox("Exportar apenas Prioritários", value=filtros.get('only_critical', False), key="pdf_crit")
                    apenas_favs = c4.checkbox("Exportar apenas Favoritos (★)", value=filtros.get('only_favs', False), key="pdf_fav")
                    
                    df_pdf = df_base.copy()
                    df_pdf['favorito'] = df_pdf['sku'].isin(st.session_state.favoritos)
                    
                    df_pdf = processor.apply_filters(
                        df=df_pdf,
                        faixas_sel=pdf_faixas,
                        categorias_sel=pdf_cats,
                        busca='',
                        only_favs=apenas_favs,
                        only_critical=apenas_criticos
                    )
                    
                    if not df_pdf.empty:
                        import modules.exporter as exporter
                        pdf_filtros = {
                            "faixas": pdf_faixas,
                            "only_critical": apenas_criticos,
                            "only_favs": apenas_favs,
                            "modo": filtros.get('modo', 'vendas')
                        }
                        pdf_bytes = exporter.generate_pdf(df_pdf, pdf_filtros, filtros.get('modo', 'vendas'))
                        st.download_button(
                            label=f"Baixar PDF — {len(df_pdf)} produtos",
                            data=pdf_bytes,
                            file_name=f"ColgateFoco_{datetime.now().strftime('%d-%m-%Y')}.pdf",
                            mime="application/pdf",
                            type="primary",
                            icon=":material/download:",
                            use_container_width=True
                        )
                    else:
                        st.info("Nenhum produto encontrado. Altere a seleção acima.")
                        
        with tab_analytics:
            import modules.charts as charts
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("**Mix de Categoria**")
                st.plotly_chart(charts.pizza_categorias(df_filtered), key="chart_categorias")
            with c2:
                st.markdown("**SKUs por Faixa (Total)**")
                st.plotly_chart(charts.barra_skus_por_faixa(df_base), key="chart_faixas")
            with c3:
                st.markdown("**Críticos vs Total**")
                st.plotly_chart(charts.barra_criticos_por_categoria(df_filtered), key="chart_criticos")

    with tab_comparativo:
        st.subheader(":material/balance: Quanto vale evoluir essa loja?")
        st.caption("Selecione a faixa atual do cliente e a faixa alvo para ver exatamente o que ele ainda não compra.")
        col1, col2 = st.columns(2)
        faixa_a = col1.selectbox("Faixa A (Ponto de Partida)", options=["FX1-2", "FX3", "FX4", "FX5"], index=1)
        faixa_b = col2.selectbox("Faixa B (Evolução Alvo)", options=["FX1-2", "FX3", "FX4", "FX5"], index=2)
        
        if faixa_a and faixa_b:
            apenas_a, apenas_b, ambos = processor.compare_faixas(df_base, faixa_a, faixa_b)
            
            n_faltando = len(apenas_b)
            st.info(f"**Para evoluir esse cliente:** Indique {n_faltando} produto{'s' if n_faltando > 1 else ''} que ele ainda não tem na faixa {faixa_b}. Concentre-se nos marcados como Crítico primeiro.", icon=":material/rocket_launch:")
            
            with st.expander(f"Produtos que o cliente de {faixa_a} ainda não tem ({len(apenas_b)} itens)", expanded=True):
                df_show = apenas_b[['sku', 'categoria', 'descricao', 'is_critical']].rename(
                    columns={'sku': 'Código', 'categoria': 'Linha', 'descricao': 'Produto', 'is_critical': 'Crítico'}
                )
                st.dataframe(df_show, hide_index=True, use_container_width=True)
            with st.expander(f"Produtos já comuns entre as duas faixas ({len(ambos)} itens)"):
                df_ambos = ambos[['sku', 'categoria', 'descricao']].rename(
                    columns={'sku': 'Código', 'categoria': 'Linha', 'descricao': 'Produto'}
                )
                st.dataframe(df_ambos, hide_index=True, use_container_width=True)

    with tab_upload:
        st.subheader(":material/refresh: Atualizar a Lista de Produtos")
        st.markdown("Toda vez que a Colgate enviar novos relatórios (a cada trimestre), carregue os arquivos aqui para atualizar os produtos automaticamente.")
        st.caption("Selecione todos os arquivos PDF enviados pela Colgate de uma vez. O sistema processa tudo automaticamente.")
        
        uploaded_files = st.file_uploader(
            "Arquivos PDF da Colgate",
            accept_multiple_files=True,
            type=["pdf"],
            help="Selecione os PDFs das faixas (FX 1-2, FX 3, FX 4, FX 5). Pode selecionar vários ao mesmo tempo."
        )
        
        if uploaded_files:
            nomes = ", ".join([f.name for f in uploaded_files])
            st.caption(f"{len(uploaded_files)} arquivo(s) selecionado(s): {nomes}")
            
            if st.button("Atualizar Lista de Produtos", type="primary", use_container_width=True, icon=":material/sync:"):
                with st.spinner("Lendo os PDFs e atualizando os produtos..."):
                    df_novo_bruto, parser_warnings = parser.parse_pdfs(uploaded_files, {})
                    
                    if parser_warnings:
                        for w in parser_warnings:
                            st.toast(f"Atenção: {w}", icon="⚠️")
                            
                    if not df_novo_bruto.empty:
                        df_novo_consolidado = processor.consolidate(df_novo_bruto)
                        processor.save_parquet(df_novo_consolidado)
                        st.success(f"Lista atualizada com sucesso! {len(df_novo_consolidado)} produtos carregados.", icon=":material/check_circle:")
                        import time
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error("Não encontrei nenhum produto nos arquivos enviados. Verifique se os PDFs são os corretos da Colgate.")
                        
        st.divider()
        st.subheader(":material/delete: Recomeçar do Zero")
        st.markdown("Use esta opção se ocorreram mudanças profundas nas faixas e você precisa apagar a base atual para começar do zero.")
        st.caption("Fique tranquilo: seus produtos Favoritos continuarão com a 'estrelinha' caso enviem PDFs contendo o mesmo código de produto.")
        
        if st.button("Apagar todos os dados atuais", type="secondary", icon=":material/delete_forever:"):
            if os.path.exists("data/base_consolidada.parquet"):
                os.remove("data/base_consolidada.parquet")
            st.success("Dados apagados com sucesso! Levando você de volta ao início...", icon="✅")
            import time
            time.sleep(1.5)
            st.rerun()

if __name__ == "__main__":
    main()
