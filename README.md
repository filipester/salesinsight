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

**Descartar registros inválidos em vez de tentar corrigi-los.** Na limpeza
(`limpar_dados`), datas que não convertem e valores ausentes em quantidade ou
preço unitário fazem o registro ser removido, não corrigido. Nesse escopo do
projeto não se usa nenhuma técnica de imputação de valores ausentes (isso só
entra em módulos futuros), então inventar uma data ou um preço para preencher
o buraco introduziria um dado falso nas métricas agregadas mais à frente.
Remover a linha inteira é a opção mais simples e mais honesta com o que
realmente se sabe sobre aquela venda.

**Calcular o trimestre com uma cadeia se/senão explícita.** A coluna
`trimestre` é obtida com `if mes <= 3 / elif mes <= 6 / elif mes <= 9 / else`,
em vez de uma fórmula matemática mais direta. A ideia é deixar a lógica
condicional visível no código, já que demonstrar o uso de `if/elif/else` é um
dos pontos avaliados do projeto.

**Usar `defaultdict` para acumular as métricas.** Em `calcular_metricas`, cada
agrupamento (por mês, produto, categoria e região) soma valores num
`defaultdict`. Isso evita ter que checar se a chave já existe antes de somar
nela, o que deixaria o código repetitivo nos quatro agrupamentos.

**Só arredondar valores que são `float` ao exibir no console.** A função
`imprime_metrica` verifica o tipo de cada valor com `isinstance(valor, float)`
antes de aplicar `round(valor, 2)`. Os blocos de métricas misturam texto
(nome de produto, categoria, região) com números, e arredondar um texto
quebraria o programa, então o arredondamento só se aplica onde faz sentido.

**Não gerar o dataset de novo se ele já existir.** O `main()` só chama
`gerar_dataset_vendas()` quando `vendas.csv` ainda não existe
(`if not os.path.exists(...)`). Como a geração usa uma seed fixa, rodar de
novo sem essa checagem recriaria sempre o mesmo arquivo à toa, e sobrescreveria
qualquer ajuste manual feito no CSV entre uma execução e outra.

**O que entra em `estatisticas_gerais.json`.** O enunciado pede a exportação
de estatísticas gerais em JSON, mas não define quais. Escolhi calcular o
total de vendas, a receita total, a receita média por venda e a quantidade de
vendas individuais com receita acima dessa média — essa última é justamente
uma das perguntas do desafio que nenhum outro requisito cobria.

## Ferramentas utilizadas

- Python 3.10+
- Google Colab / VS Code
- Bibliotecas da biblioteca padrão do Python: `csv`, `json`, `re`, `datetime`, `os`, `random`
- GitHub para versionamento

## Vídeo de demonstração

[inserir o link do Google Drive ou do YouTube aqui]
