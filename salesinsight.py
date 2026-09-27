from collections import defaultdict
import csv
import random
import re
from datetime import datetime, timedelta

def gerar_dataset_vendas(caminho_csv="vendas.csv", n_registros=200, seed=42):
    """Gera um dataset sintetico de vendas com dados sujos e grava em CSV."""
    random.seed(seed)
    produtos = ["Notebook", "Smartphone", "Tablet", "Monitor",
                "Teclado", "Mouse", "Headset"]
    categorias = {"Notebook": "Computadores", "Smartphone": "Celulares",
                  "Tablet": "Celulares", "Monitor": "Computadores",
                  "Teclado": "Perifericos", "Mouse": "Perifericos",
                  "Headset": "Perifericos"}
    precos = {"Notebook": 3500, "Smartphone": 2200, "Tablet": 1800,
              "Monitor": 1200, "Teclado": 250, "Mouse": 120,
              "Headset": 350}
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
    data_inicio = datetime(2025, 1, 1)
    colunas = ["id_venda", "data_venda", "cliente", "produto",
               "categoria", "regiao", "quantidade", "preco_unitario"]

    with open(caminho_csv, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()

        for i in range(n_registros):
            produto = random.choice(produtos)
            categoria = categorias[produto]
            quantidade = random.randint(1, 10)
            preco = round(precos[produto] * random.uniform(0.85, 1.15), 2)
            data = data_inicio + timedelta(days=random.randint(0, 364))
            data_txt = data.strftime("%Y-%m-%d")
            cliente = f"Cliente_{random.randint(1, 50):03d}"

            # --- sujeira proposital para a etapa de limpeza ---
            if random.random() < 0.05:
                quantidade = ""                       # valor ausente
            if random.random() < 0.04:
                preco = ""                            # valor ausente
            if random.random() < 0.06:
                produto = " " + produto + " "         # espacos extras
            if random.random() < 0.03:
                data_txt = "DATA INVALIDA"             # data invalida
            if random.random() < 0.10:
                cliente = random.choice([              # ruido no nome
                    cliente.upper().replace("_", "-"),
                    cliente + "!!",
                    " " + cliente,
                    cliente.replace("Cliente_", "cliente#"),
                ])

            escritor.writerow({
                "id_venda": i + 1,
                "data_venda": data_txt,
                "cliente": cliente,
                "produto": produto,
                "categoria": categoria,
                "regiao": random.choice(regioes),
                "quantidade": quantidade,
                "preco_unitario": preco,
            })

    print(f"Dataset gerado com {n_registros} registros em {caminho_csv}.")


def carregar_dataset(caminho_csv):
    """Le o CSV e retorna uma lista de dicionarios (um por registro)."""
    with open(caminho_csv, "r", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        registros = list(leitor)
    return registros

def inspecionar_dados(registros):
    """Exibe as informacoes estruturais da lista de registros."""
    total = len(registros)
    colunas = list(registros[0].keys()) if registros else []

    nulos = {coluna: 0 for coluna in colunas}
    for linha in registros:
        for coluna in colunas:
            if linha.get(coluna, "").strip() == "":
                nulos[coluna] += 1

    print("\n=== INSPECAO INICIAL DO DATASET ===")
    print(f"Total de registros: {total}")
    print(f"\nColunas: {colunas}")
    print(f"\nValores ausentes por coluna:\n{nulos}")
    print("\nPrimeiros registros:")
    for linha in registros[:5]:
        print(linha)
    return registros

def limpar_dados(registros):
    """
    Limpa e trata a lista de registros de vendas.
    Retorna: (registros_limpos, relatorio), onde relatorio e um dicionario
    com as contagens de registros iniciais, removidos e finais.
    """
    relatorio = {"iniciais": len(registros), "removidos_data": 0,
                 "removidos_nulos": 0, "finais": 0}
    padrao_cliente = re.compile(r"^Cliente_\d{3}$", flags=re.IGNORECASE)
    limpos = []

    for linha in registros:
    # 1. remover espacos extras nas colunas de texto
        for chave in ("cliente", "produto", "categoria", "regiao"):
            linha[chave] = linha[chave].strip()

    # 2. converter data_venda e descartar datas invalidas
        try:
            linha["data_venda"] = datetime.strptime(linha["data_venda"], "%Y-%m-%d")
        except ValueError:
            relatorio["removidos_data"] += 1
            continue

    # 3. descartar nulos em quantidade e preco_unitario
        if linha["quantidade"] == "" or linha["preco_unitario"] == "":
            relatorio["removidos_nulos"] += 1
            continue

    # 4. ajustar os tipos numericos
        linha["quantidade"] = int(float(linha["quantidade"]))
        linha["preco_unitario"] = float(linha["preco_unitario"])

    # 5. padronizar o nome do cliente com re.sub()
        nome_limpo = re.sub(r"[^A-Za-z0-9_]", "", linha["cliente"])
        linha["cliente"] = nome_limpo
        linha["cliente_fora_do_padrao"] = padrao_cliente.match(nome_limpo) is None
        limpos.append(linha)

    # 6. montar e imprimir o relatorio de limpeza
    relatorio["finais"] = len(limpos)
    print("\n=== RELATORIO DE LIMPEZA ===")
    print(relatorio)
    return limpos, relatorio

def criar_colunas_derivadas(registros):
    """
    Cria colunas derivadas a partir do dataset ja limpo: receita_total, mes,
    mes_nome, trimestre, ano e faixa_receita_item.
    Retorna a mesma lista de registros, com os campos novos adicionados.
    """
    nomes_meses = {
        1: "Janeiro", 2: "Fevereiro", 3: "Marco", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro",
    }

    for linha in registros:
        # cada campo derivado e calculado registro por registro
        linha["receita_total"] = linha["quantidade"] * linha["preco_unitario"]

        data_venda = linha["data_venda"]
        linha["mes"] = data_venda.month
        linha["mes_nome"] = nomes_meses[data_venda.month]
        linha["ano"] = data_venda.year

        # trimestre calculado a partir do mes com if/elif/else
        mes = data_venda.month
        if mes <= 3:
            linha["trimestre"] = "Q1"
        elif mes <= 6:
            linha["trimestre"] = "Q2"
        elif mes <= 9:
            linha["trimestre"] = "Q3"
        else:
            linha["trimestre"] = "Q4"

        # classificacao condicional da receita do registro
        receita = linha["receita_total"]
        if receita < 500:
            linha["faixa_receita_item"] = "Baixo Valor"
        elif receita < 5000:
            linha["faixa_receita_item"] = "Medio Valor"
        else:
            linha["faixa_receita_item"] = "Alto Valor"

    return registros

def calcular_metricas(registros):
    """ 
    Calcula as metricas agregadas da lista de registros. 
    Retorna um dicionario no formato {nome_da_metrica: lista_de_linhas}. 
    Chaves minimas: por_mes, top_produtos, por_categoria, por_regiao. 
    """ 
    metricas = {}
    acumulado = defaultdict(lambda: {"receita_total": 0, "quantidade": 0, "n_vendas": 0})
    # use dicionarios (ou defaultdict) para acumular receita_total, 
    # quantidade e numero de vendas por mes, produto, categoria e 
    # regiao; depois converta cada dicionario em uma lista ordenada 
    # de registros (dict.items() + sorted()) 
    for linha in registros:
        mes = linha["mes"]
        acumulado[mes]["receita_total"] += linha["receita_total"]
        acumulado[mes]["quantidade"] += linha["quantidade"]
        acumulado[mes]["n_vendas"] += 1
    
    por_mes = [{"mes": mes, **dados} for mes, dados in sorted(acumulado.items())]

    receita_por_produto = defaultdict(float)
    for linha in registros:
        receita_por_produto[linha["produto"]] += linha["receita_total"]
    top_produtos = [
        {"produto": produto, "receita_total": receita}
        for produto, receita in sorted(
            receita_por_produto.items(), key=lambda item: item[1], reverse=True
        )
    ][:5]

    receita_por_categoria = defaultdict(float)
    for linha in registros:
        receita_por_categoria[linha["categoria"]] += linha["receita_total"]
    por_categoria = [
        {"categoria": categoria, "receita_total": receita}
        for categoria, receita in sorted(
            receita_por_categoria.items(), key=lambda item: item[1], reverse=True
        )
    ]

    acumulado_regiao = defaultdict(lambda: {"receita_total": 0, "n_vendas": 0})
    for linha in registros:
        regiao = linha["regiao"]
        acumulado_regiao[regiao]["receita_total"] += linha["receita_total"]
        acumulado_regiao[regiao]["n_vendas"] += 1
    por_regiao = [
        {
            "regiao": regiao,
            "receita_total": dados["receita_total"],
            "ticket_medio": dados["receita_total"] / dados["n_vendas"],
        }
        for regiao, dados in sorted(acumulado_regiao.items())
    ]

    metricas["por_mes"] = por_mes
    metricas["top_produtos"] = top_produtos
    metricas["por_categoria"] = por_categoria
    metricas["por_regiao"] = por_regiao

    return metricas

def imprime_metrica(metricas):
    """Exibe cada bloco de metricas no console em formato legivel."""
    for metrica, linhas in metricas.items():
        titulo = metrica.upper().replace("_", " ")
        print(f"\n=== {titulo} ===")
        for linha in linhas:
            pares = []
            for chave, valor in linha.items():
                if isinstance(valor, float):
                    valor = round(valor, 2)
                pares.append(f"{chave}: {valor}")
            print(", ".join(pares))

def segmentar_clientes(registros):
    """
    Agrupa por cliente, soma a receita e classifica em
    Bronze / Prata / Ouro usando uma funcao lambda.
    Retorna uma lista de dicionarios: cliente, total_gasto, segmento.
    """
    classificar = lambda total: (
        "Ouro" if total > 15000 else "Prata" if total >= 5000 else "Bronze"
    )

    total_por_cliente = {}
    for linha in registros:
        total_por_cliente[linha["cliente"]] = (
            total_por_cliente.get(linha["cliente"], 0) + linha["receita_total"]
        )

    clientes = [
        {"cliente": nome, "total_gasto": total, "segmento": classificar(total)}
        for nome, total in total_por_cliente.items()
    ]

    top_10 = sorted(clientes, key=lambda c: c["total_gasto"], reverse=True)[:10]
    distribuicao = defaultdict(int)
    for cliente in clientes:
        distribuicao[cliente["segmento"]] += 1

    print("\n=== TOP 10 CLIENTES ===")
    for cliente in top_10:
        print(f"{cliente['cliente']}: R$ {round(cliente['total_gasto'], 2)} ({cliente['segmento']})")

    print("\n=== DISTRIBUICAO POR SEGMENTO ===")
    for segmento, contagem in distribuicao.items():
        print(f"{segmento}: {contagem}")

    return clientes

gerar_dataset_vendas()
dataset = carregar_dataset('vendas.csv')
inspecionar_dados(dataset)

dados_limpo, relatorio_limpeza = limpar_dados(dataset)

dados = criar_colunas_derivadas(dados_limpo)

metricas = calcular_metricas(dados)
imprime_metrica(metricas)

clientes = segmentar_clientes(dados)