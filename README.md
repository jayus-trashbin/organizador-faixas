# Colgate Foco Dashboard

O Colgate Foco é um dashboard desenvolvido primariamente para equipes de campo e backoffice gerenciarem e analisarem as variações dinâmicas das planilhas de foco e vizinhança da Colgate-Palmolive (FX 1-2, FX 3, FX 4 e FX 5).

## Ambiente B2B & UI/UX Mestre
A interface é baseada nas métricas mais recentes de Web Guidelines e Usabilidade de Operação Rápida. O sistema emprega hierarquias limpas com Von Restorff effect no apontamento de Skus críticos para diminuir o tempo de decisão do vendedor em Mobile ou Desktop.

## Executando Localmente

Para iniciar a base de serviço e carregar o painel, acione o Streamlit:
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Como Sincronizar Novos Dados (Acada 3 Meses)
A persistência de memória do software é autônoma:
1. Abra o serviço web do dashboard e navegue na aba "Gerenciamento".
2. Pegue todos os PDFs corporativos (como "ITENS FOCO H&S.pdf", "VIZINHANÇA FX5.pdf") juntos, e arraste-os para o Upload.
3. Clique em **Sincronizar**. O motor de *Ingestão Semântica* vai procurar a assinatura estrutural da tabela e devorá-las inteiras. Se houver algum erro de impressora na página da Colgate, a UI informará você de imediato ao invés de explodir.
4. **Resiliência de Favoritos**: Pode atualizar sem medo. SKUs que você favoritou no ciclo anterior serão preservados e reacoplados à nova base contanto que não tenham sido deslistados das novas faixas.

## Deploy para Produção Corporativa
Como o sistema salva os "favoritos" em disco (`data/favoritos.json`) e lê a tabela mestre de um `data/base_consolidada.parquet`, se for subir na nuvem, você deve ter mapeamento de volume persistente para a pasta `/data`.
*   Para subidas efêmeras gratuitas (ex: Render/Streamlit Cloud), todo "reboot" virtual da máquina fará com que essa pasta suma, caso você não forneça um volume acoplado.
*   **Solução Rápida Recomendada**: Usar um host local/interno (Intranet).
