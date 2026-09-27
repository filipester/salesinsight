# SalesInsight PY

## Sobre o projeto

Análise de dados de vendas desenvolvida em Python puro (biblioteca padrão). O
projeto carrega, limpa, transforma e agrega um dataset de vendas sintético,
gerando métricas por período, produto, categoria e região, além de uma
segmentação simples de clientes por faixa de gasto.

Este é o Mini-Projeto Avaliativo do Módulo 01 (Semana 08) da trilha
Desenvolvedor(a) em IA para Análise Preditiva. A versão vigente do desafio
tem escopo reduzido: não são exigidos Pandas, NumPy, Matplotlib/Seaborn ou
classes, apenas os conceitos trabalhados até a Semana 05.

## O que o projeto analisa

- Receita total e volume de vendas por mês e por trimestre
- Top produtos e categorias por receita
- Desempenho por região
- Segmentação de clientes por nível de gasto (Bronze, Prata, Ouro)
- Vendas com receita por transação acima da média geral
- Exportação de relatórios em CSV e JSON

## Conceitos aplicados (Módulo 01 - Semanas 01 a 05)

- Lógica de programação: variáveis, tipos, operadores, condicionais (if/elif/else), repetição (for/while)
- Estruturas de dados: listas, tuplas, dicionários e estruturas compostas
- Funções: parâmetros, retorno, docstrings, lambda, função de ordem superior
- Leitura e escrita de arquivos CSV e JSON
- Módulo `datetime` e expressões regulares (`re`)
- Git e GitHub: branches, commits e GitFlow simplificado

## Como executar

### Google Colab (recomendado)

1. Faça upload de `salesinsight.py` e de `vendas.csv` para o Colab (ou deixe o
   próprio script gerar o dataset).
2. Execute: `!python salesinsight.py`
3. Ou cole o conteúdo em células de um notebook `.ipynb`.

### Localmente com VS Code

1. Instale o Python 3.10+ e o VS Code.
2. Nenhuma dependência externa é necessária (usa apenas a biblioteca padrão
   do Python: `csv`, `json`, `re`, `datetime`, `os`, `random`).
3. Execute no terminal: `python salesinsight.py`

## Estrutura do projeto

```
salesinsight-py/
|-- salesinsight.py       # fluxo principal (geracao, limpeza, metricas, exportacao)
|-- vendas.csv             # dataset gerado sinteticamente pelo proprio codigo
|-- README.md
|-- outputs/                       # gerado ao executar o fluxo completo
|   |-- metricas_por_mes.csv
|   |-- segmentacao_clientes.csv
|   |-- estatisticas_gerais.json
```

## Decisões técnicas

<!-- Preencher com pelo menos uma decisão relevante, por exemplo: por que
descartar registros invalidos em vez de tentar corrigi-los, ou por que usar
dicionarios para acumular metricas em vez de repetir calculos. -->

## Ferramentas utilizadas

- Python 3.10+
- Google Colab / VS Code
- Bibliotecas da biblioteca padrão do Python: `csv`, `json`, `re`, `datetime`, `os`, `random`
- GitHub para versionamento

## Vídeo de demonstração

[inserir o link do Google Drive ou do YouTube aqui]
