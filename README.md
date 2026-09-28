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
|-- planejamento/
|   |-- tarefas-kanban.md          # quadro Kanban com as tarefas do projeto
```

`vendas.csv` e a pasta `outputs/` não são versionados (estão no `.gitignore`):
os dois são recriados a cada execução do script.

## Organização e versionamento

As tarefas foram planejadas num quadro Kanban
([planejamento/tarefas-kanban.md](planejamento/tarefas-kanban.md)), quebradas
pelos requisitos funcionais do enunciado.

O repositório segue um GitFlow simplificado:

- `main` — versão estável, a que é entregue.
- `develop` — integração das funcionalidades antes de irem para a `main`.
- `feat/pipeline-dados` — correções e novas métricas do fluxo de dados.
- `docs/readme` — README, Kanban e documentação.

As mensagens de commit seguem o padrão Conventional Commits (`feat:`, `fix:`,
`refactor:`, `chore:`, `docs:`), e os merges são feitos com `--no-ff` para que o
histórico mostre onde cada branch foi integrada.

## Decisões técnicas

**Descartar registros inválidos em vez de tentar corrigi-los.** Na limpeza
(`limpar_dados`), datas que não convertem e valores ausentes em quantidade ou
preço unitário fazem o registro ser removido, não corrigido. Nesse escopo do
projeto não se usa nenhuma técnica de imputação de valores ausentes (isso só
entra em módulos futuros), então inventar uma data ou um preço para preencher
o buraco introduziria um dado falso nas métricas agregadas mais à frente.
Remover a linha inteira é a opção mais simples e mais honesta com o que
realmente se sabe sobre aquela venda.

**Padronizar o nome do cliente reconstruindo-o, em vez de só apagar símbolos.**
O dataset traz o mesmo cliente escrito de formas diferentes (`CLIENTE-011`,
`cliente#008`, `Cliente_008!!`). Apagar apenas os caracteres especiais ainda
deixava `CLIENTE011` e `cliente008` como clientes distintos: a segmentação
chegava a 58 clientes quando o gerador cria só 50, e o gasto de um mesmo
cliente ficava dividido. Por isso `limpar_dados` separa as duas partes do
nome com `re.sub` — só as letras (`[^A-Za-z]`, depois `.capitalize()`) e só
os dígitos (`\D`) — e remonta no formato `Cliente_NNN`. Com isso a
segmentação passou a contar corretamente os 50 clientes.

**Calcular o trimestre com uma cadeia se/senão explícita.** A coluna
`trimestre` é obtida com `if mes <= 3 / elif mes <= 6 / elif mes <= 9 / else`,
em vez de uma fórmula matemática mais direta. A ideia é deixar a lógica
condicional visível no código, já que demonstrar o uso de `if/elif/else` é um
dos pontos avaliados do projeto.

**Usar `defaultdict` para acumular as métricas.** Em `calcular_metricas`, cada
agrupamento (por mês, produto, categoria e região) soma valores num
`defaultdict`. Isso evita ter que checar se a chave já existe antes de somar
nela, o que deixaria o código repetitivo nos quatro agrupamentos.

**Só arredondar valores que são `float`.** As funções `imprimir_metricas` e
`imprimir_estatisticas`, e a exportação do JSON, verificam o tipo de cada valor
com `isinstance(valor, float)` antes de aplicar `round(valor, 2)`. Os blocos de
métricas misturam texto (nome de produto, categoria, região) com números, e
arredondar um texto quebraria o programa. Já as contagens (total de vendas,
vendas acima da média) são inteiros e continuam inteiros — converter tudo para
`float` faria o JSON mostrar "183.0 vendas".

**Separar cálculo de exibição.** `calcular_estatisticas_gerais` só calcula e
devolve um dicionário; quem imprime é `imprimir_estatisticas`, que recebe esse
dicionário por parâmetro. Assim o cálculo pode ser reaproveitado (por exemplo,
na exportação do JSON) sem gerar saída no console. Algumas funções que vieram
do enunciado, como `segmentar_clientes`, ainda calculam e imprimem ao mesmo
tempo — separar essas também seria uma melhoria futura.

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
- Git e GitHub para versionamento
- Kanban em Markdown (`planejamento/tarefas-kanban.md`) para organizar as tarefas

## Vídeo de demonstração

[inserir o link do Google Drive ou do YouTube aqui]
