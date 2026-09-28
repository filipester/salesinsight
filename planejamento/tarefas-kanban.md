# Kanban — SalesInsight PY

Quadro de tarefas do mini-projeto, quebrado pelos requisitos funcionais (RF) do
enunciado. Cada cartão indica a branch em que foi desenvolvido.

## A fazer

_Nenhuma tarefa pendente._

## Fazendo

_Nenhuma tarefa em andamento._

## Concluído

### Entrega
- [x] Integrar `docs/readme` → `develop` → `main` — `main`
- [x] Gravar e editar o vídeo de demonstração (até 5 min)
- [x] Publicar o vídeo com acesso por link e colocar o link no README — `main`
- [x] Enviar os links do repositório e do vídeo no AVA

### Estrutura e dados
- [x] Criar repositório público e `.gitignore` — `main`
- [x] RF01 — Gerar o dataset sintético de vendas (`gerar_dataset_vendas`) — `main`
- [x] RF02 — Carregar e inspecionar os dados (`carregar_dataset`, `inspecionar_dados`) — `main`
- [x] RF03 — Limpar os dados: espaços, datas inválidas, nulos e tipos (`limpar_dados`) — `main`
- [x] RF03 — Corrigir a padronização de clientes para `Cliente_NNN` com regex — `feat/pipeline-dados`

### Transformação e análise
- [x] RF04 — Criar colunas derivadas: receita, mês, trimestre, ano, faixa (`criar_colunas_derivadas`) — `main`
- [x] RF05 — Calcular métricas por mês, produto, categoria e região (`calcular_metricas`) — `main`
- [x] RF05 — Adicionar métricas por trimestre — `feat/pipeline-dados`
- [x] RF06 — Segmentar clientes em Bronze/Prata/Ouro com lambda (`segmentar_clientes`) — `main`

### Organização e saída
- [x] RF07 — Organizar em funções e criar função de ordem superior (`processar_coluna`) — `main`
- [x] RF08 — Exportar CSV e JSON e reler o JSON (`exportar_resultados`) — `main`
- [x] RF08 — Manter inteiros como `int` no JSON exportado — `feat/pipeline-dados`
- [x] Calcular estatísticas gerais e vendas acima da média (`calcular_estatisticas_gerais`) — `main`
- [x] Exibir estatísticas gerais no console (`imprimir_estatisticas`) — `feat/pipeline-dados`
- [x] RF09 — Criar `main()` e o bloco `if __name__ == "__main__":` — `main`

### Versionamento e documentação
- [x] Criar branches `develop`, `feat/pipeline-dados` e `docs/readme` — `develop`
- [x] Integrar `feat/pipeline-dados` → `develop` — `develop`
- [x] Escrever o README: objetivo, execução, conceitos e decisões técnicas — `docs/readme`
- [x] Montar este quadro Kanban — `docs/readme`
