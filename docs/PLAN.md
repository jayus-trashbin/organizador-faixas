# 🎼 Orchestration Report: Frontend Design & UX Overhaul

## Fase 1: Planejamento Tático (Project Planner Role)

Baseado nos princípios de **UX Psychology** (frontend-design e ui-ux-pro-max), as limitações do _Streamlit_ e o contexto de uma força de vendas B2B (necessidade de decisões viscerais e rápidas sob alta carga cognitiva em campo).

### Princípios Analisados
1. **Fitts' Law** (Área e Acesso): Os filtros na barra lateral exigem cliques em checkboxes muito distantes. Mudar para _Pills/Tags_ clicáveis logo acima da tabela.
2. **Miller's Law / Hick's Law** (Carga Cognitiva): Agrupamento de Analytics no meio da tabela polui a visualização. Transformaremos isso em abas dedicadas (`Tabela` vs `Gráficos`) na primeira guia.
3. **Von Restorff Effect** (Isolamento Visual): O KPI de "Itens Críticos" é a métrica principal da Colgate. Ele será o único cartão de dados invertido (Solid Red Background / White Text), para atrair a atenção do vendedor imediatamente. O Analytics também usará esse destaque.
4. **Regra 60-30-10**: 60% Slate Dark, 30% Slate Grey (Painéis), 10% Red (Métricas primárias e Busca Ativa).

### ⚙️ Implementações Propostas (Fase 2 - Parallel Execution)

#### **[Frontend-Specialist] Modificações na UI/UX**
- [ ] **Data Cards Assimétricos**: Injetar CSS em `theme.py` focando exclusivamente a métrica de "Itens Críticos" com fundo vermelho vibrante e tipografia brilhante, diferenciando-a dos demais KPIs cinzas.
- [ ] **Tabulagem de Contexto**: Dentro de `Painel Geral`, dividir a interface em duas sub-abas puras: `Tabela de SKUs` e `Analytics de Venda`, eliminando a rolagem vertical infinita em mobile.
- [ ] **Filtros por Pills (Streamlit native pils/checkboxes em container)**: Mudar a seleção de Modo e Preferências Rápidas (Apenas Críticos) para mais próximo do campo de Busca ou usando `pills_` segmentados para fluidez tátil em vez de caixas verticais escondidas.

#### **[Performance-Optimizer] Refinamentos Técnicos**
- [ ] Limpeza do estado visual do PDF. Reposicionar o Botão de Download para ficar fisicamente aglutinado ao controlador de Filtros, tornando a "Geração" uma consequência instantânea do funil e não um botão de rodapé.

### Status de Orquestração Limitada
- Como sou a única entidade técnica neste shell, serei o coordenador sequencial, assumindo chapéus de *UI/UX*, *Tester* e *Frontend Engineer* assim que sua aprovação for fornecida.

---

Você concorda com essa arquitetura de Layout orientada ao comportamento do Vendedor B2B? Se sim, avance ou ajuste algo!
