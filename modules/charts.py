"""
Gráficos e painéis do Plotly.
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def pizza_categorias(df: pd.DataFrame):
    if df.empty:
        return go.Figure()
        
    df_count = df['categoria'].value_counts().reset_index()
    df_count.columns = ['Categoria', 'Contagem']
    
    fig = px.pie(
        df_count, 
        values='Contagem', 
        names='Categoria', 
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FAFAFA', family="Inter, sans-serif"),
        margin=dict(t=20, b=20, l=20, r=20),
        showlegend=False,
        dragmode=False
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def barra_skus_por_faixa(df_total: pd.DataFrame):
    if df_total.empty:
        return go.Figure()
        
    faixas_count = {'FX 1-2': 0, 'FX 3': 0, 'FX 4': 0, 'FX 5': 0}
    
    for faixas_list in df_total['faixas']:
        for f in faixas_list:
            if '1' in f or '2' in f: faixas_count['FX 1-2'] += 1
            elif '3' in f: faixas_count['FX 3'] += 1
            elif '4' in f: faixas_count['FX 4'] += 1
            elif '5' in f: faixas_count['FX 5'] += 1
            
    df_plot = pd.DataFrame(list(faixas_count.items()), columns=['Faixa', 'SKUs'])
    
    color_map = {
        'FX 1-2': '#3A86FF',
        'FX 3': '#8338EC',
        'FX 4': '#FB5607',
        'FX 5': '#06D6A0'
    }
    
    fig = px.bar(
        df_plot, 
        x='Faixa', 
        y='SKUs', 
        color='Faixa',
        color_discrete_map=color_map,
        text_auto=True
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FAFAFA', family="Inter, sans-serif"),
        margin=dict(t=20, b=20, l=20, r=20),
        showlegend=False,
        xaxis_title=None,
        yaxis_title=None,
        dragmode=False
    )
    return fig

def barra_criticos_por_categoria(df: pd.DataFrame):
    if df.empty:
        return go.Figure()
        
    df_agg = df.groupby('categoria').agg(
        Total=('sku', 'count'),
        Criticos=('is_critical', 'sum')
    ).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_agg['categoria'],
        y=df_agg['Total'],
        name='Total',
        marker_color='#555555'
    ))
    
    fig.add_trace(go.Bar(
        x=df_agg['categoria'],
        y=df_agg['Criticos'],
        name='Críticos',
        marker_color='#E3001B'
    ))
    
    fig.update_layout(
        barmode='group',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FAFAFA', family="Inter, sans-serif"),
        margin=dict(t=20, b=20, l=20, r=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        dragmode=False
    )
    return fig
