#!/usr/bin/env python3
"""
COBECO — Gerador de seed a partir do pré-seed (CSV único).

Lê backend/scripts/pre_seed.csv e gera backend/seed_from_csv.sql
com:
  - limpeza idempotente (DELETE por ordem de FK)
  - AUTO_INCREMENT resetado
  - inserção de categorias, fornecedores, fornecedores_categorias,
    produtos e fornecedores_produtos
  - equalização: fornecedores_produtos só é inserido quando
    atende_categoria = S (nem todo produto em todo fornecedor)
  - flag de estoque: fornecedores_produtos.ativo = (disponivel == 'S');
    estoque = 0 quando indisponível

Uso:
  cd backend
  python scripts/gerar_seed_csv.py [--csv scripts/pre_seed.csv] [--out seed_from_csv.sql]
"""

import argparse
import csv
from pathlib import Path

# Ordem canônica das categorias (ids fixos, igual ao seed original)
CATEGORIAS_ORDEM = [
    ("Mercado", "Supermercados, mercearias e atacados"),
    ("Vestuário", "Roupas, calçados e acessórios"),
    ("Automotivos", "Peças, acessórios e serviços automotivos"),
    ("Informática", "Computadores, periféricos e eletrônicos"),
    ("Decoração", "Itens de decoração e artigos para casa"),
    ("Móveis", "Móveis residenciais e corporativos"),
    ("Materiais de Construção e Ferragens", "Materiais de construção, ferramentas e ferragens"),
    ("Ferramentas", "Ferramentas manuais, elétricas e de medição"),
    ("Livros", "Livros, revistas e publicações"),
    ("Jardinagem", "Plantas, ferramentas e artigos de jardim"),
    ("Eletrodomésticos", "Eletrodomésticos de linha branca e marrom"),
]


def sql_str(v: str) -> str:
    return "'" + str(v).replace("'", "''") + "'"


def gerar(csv_path: Path, out_path: Path) -> None:
    linhas = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        for row in leitor:
            linhas.append(row)

    # Agregados distintos
    categorias: dict[str, str] = {}  # nome -> descricao (categoria_macro)
    fornecedores: dict[int, dict] = {}  # id -> dados
    produtos: dict[int, dict] = {}  # id -> dados
    fp_linhas: list[dict] = []  # fornecedores_produtos (apenas atende_categoria=S)
    fc_linhas: set[tuple[int, int]] = set()  # (fornecedor_id, categoria_id)

    cat_nome_para_id: dict[str, int] = {}
    for idx, (nome, desc) in enumerate(CATEGORIAS_ORDEM, start=1):
        cat_nome_para_id[nome] = idx

    for row in linhas:
        pid = int(row["produto_id"])
        fname = row["categoria"].strip()
        fdesc = row["categoria_macro"].strip()
        categorias[fname] = fdesc

        fid = int(row["fornecedor_id"])
        if fid not in fornecedores:
            fornecedores[fid] = {
                "nome": row["fornecedor_nome"].strip(),
                "cnpj": row["fornecedor_cnpj"].strip(),
                "ativo": row["fornecedor_ativo"].strip().upper() == "S",
            }

        if pid not in produtos:
            produtos[pid] = {
                "nome": row["produto_nome"].strip(),
                "marca": row["marca"].strip(),
                "categoria": row["categoria"].strip(),
                "unidade": row["unidade"].strip(),
                "ativo": row["ativo_produto"].strip().upper() == "S",
            }

        # Equalização: só relaciona fornecedor->produto quando atende a categoria
        if row["atende_categoria"].strip().upper() == "S":
            fp_linhas.append({
                "fornecedor_id": fid,
                "produto_id": pid,
                "preco": float(row["preco"]),
                "estoque": int(row["estoque"]),
                "ativo": row["disponivel"].strip().upper() == "S",
            })
            # fornecedor atende a categoria do produto
            cid = cat_nome_para_id[produtos[pid]["categoria"]]
            fc_linhas.add((fid, cid))

    # Mapeia categoria -> id fixo
    cat_id_por_nome = {}
    for idx, (nome, _desc) in enumerate(CATEGORIAS_ORDEM, start=1):
        cat_id_por_nome[nome] = idx

    partes: list[str] = []
    partes.append("-- COBECO — Seed gerado a partir do pré-seed (scripts/pre_seed.csv)")
    partes.append("-- Equalização: fornecedores_produtos apenas quando atende_categoria = S")
    partes.append("-- Flag de estoque: ativo = disponível; estoque = 0 quando indisponível")
    partes.append("")
    partes.append("SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;")
    partes.append("SET FOREIGN_KEY_CHECKS = 0;")
    partes.append("")
    partes.append("-- Limpeza idempotente dos dados")
    partes.append("DELETE FROM `sessoes`;")
    partes.append("DELETE FROM `fornecedores_produtos`;")
    partes.append("DELETE FROM `fornecedores_categorias`;")
    partes.append("DELETE FROM `itens_lista`;")
    partes.append("DELETE FROM `listas`;")
    partes.append("DELETE FROM `usuarios`;")
    partes.append("DELETE FROM `produtos`;")
    partes.append("DELETE FROM `fornecedores`;")
    partes.append("DELETE FROM `categorias`;")
    partes.append("")
    partes.append("ALTER TABLE `sessoes` AUTO_INCREMENT = 1;")
    partes.append("ALTER TABLE `usuarios` AUTO_INCREMENT = 1;")
    partes.append("ALTER TABLE `listas` AUTO_INCREMENT = 1;")
    partes.append("ALTER TABLE `itens_lista` AUTO_INCREMENT = 1;")
    partes.append("ALTER TABLE `categorias` AUTO_INCREMENT = 1;")
    partes.append("ALTER TABLE `fornecedores` AUTO_INCREMENT = 1;")
    partes.append("ALTER TABLE `produtos` AUTO_INCREMENT = 1;")
    partes.append("")

    # Categorias (ordem fixa)
    partes.append("-- Categorias")
    valores = []
    for idx, (nome, desc) in enumerate(CATEGORIAS_ORDEM, start=1):
        valores.append(f"  ({idx}, {sql_str(nome)}, {sql_str(desc)})")
    partes.append("INSERT INTO `categorias` (`id`, `nome`, `descricao`) VALUES")
    partes.append(",\n".join(valores) + ";")
    partes.append("")

    # Fornecedores
    partes.append("-- Fornecedores")
    valores = []
    for fid in sorted(fornecedores):
        d = fornecedores[fid]
        ativo = "TRUE" if d["ativo"] else "FALSE"
        valores.append(f"  ({fid}, {sql_str(d['nome'])}, {sql_str(d['cnpj'])}, {ativo})")
    partes.append("INSERT INTO `fornecedores` (`id`, `nome`, `cnpj`, `ativo`) VALUES")
    partes.append(",\n".join(valores) + ";")
    partes.append("")

    # Fornecedores x Categorias (derivado da equalização)
    partes.append("-- Fornecedores por categoria (N:N, da equalização do CSV)")
    valores = []
    for fid, cid in sorted(fc_linhas):
        valores.append(f"  ({fid}, {cid})")
    if valores:
        partes.append("INSERT INTO `fornecedores_categorias` (`fornecedor_id`, `categoria_id`) VALUES")
        partes.append(",\n".join(valores) + ";")
    else:
        partes.append("-- sem relações")
    partes.append("")

    # Produtos (com categoria_id)
    partes.append("-- Produtos (categoria_id atribuído conforme pré-seed)")
    valores = []
    for pid in sorted(produtos):
        d = produtos[pid]
        cid = cat_id_por_nome[d["categoria"]]
        ativo = "TRUE" if d["ativo"] else "FALSE"
        valores.append(
            f"  ({pid}, {sql_str(d['nome'])}, {sql_str(d['unidade'])}, {ativo}, {cid})"
        )
    partes.append("INSERT INTO `produtos` (`id`, `nome`, `unidade`, `ativo`, `categoria_id`) VALUES")
    partes.append(",\n".join(valores) + ";")
    partes.append("")

    # Fornecedores x Produtos (preços e estoque)
    partes.append("-- Preços e estoque (equalizados por categoria; flag disponível/indisponível)")
    valores = []
    for fp in fp_linhas:
        ativo = "TRUE" if fp["ativo"] else "FALSE"
        valores.append(
            f"  ({fp['fornecedor_id']}, {fp['produto_id']}, {fp['preco']:.2f}, {fp['estoque']}, {ativo})"
        )
    partes.append("INSERT INTO `fornecedores_produtos` (`fornecedor_id`, `produto_id`, `preco`, `estoque`, `ativo`) VALUES")
    partes.append(",\n".join(valores) + ";")
    partes.append("")

    partes.append("SET FOREIGN_KEY_CHECKS = 1;")
    partes.append("")
    partes.append("-- Verificação do volume persistido")
    partes.append("SELECT 'categorias' AS tabela, COUNT(*) AS quantidade FROM `categorias`")
    partes.append("UNION ALL SELECT 'fornecedores', COUNT(*) FROM `fornecedores`")
    partes.append("UNION ALL SELECT 'produtos', COUNT(*) FROM `produtos` WHERE `ativo` = TRUE")
    partes.append("UNION ALL SELECT 'precos', COUNT(*) FROM `fornecedores_produtos` WHERE `ativo` = TRUE")
    partes.append("UNION ALL SELECT 'relacoes', COUNT(*) FROM `fornecedores_categorias`;")
    partes.append("")

    sql = "\n".join(partes)
    out_path.write_text(sql, encoding="utf-8")
    print(f"Gerado: {out_path}")
    print(f"  categorias: {len(CATEGORIAS_ORDEM)}")
    print(f"  fornecedores: {len(fornecedores)}")
    print(f"  produtos: {len(produtos)}")
    print(f"  fornecedores_categorias: {len(fc_linhas)}")
    print(f"  fornecedores_produtos: {len(fp_linhas)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera seed SQL a partir do pré-seed CSV")
    parser.add_argument("--csv", type=Path, default=Path(__file__).parent / "pre_seed.csv")
    parser.add_argument("--out", type=Path, default=Path(__file__).parent.parent / "seed_from_csv.sql")
    args = parser.parse_args()
    gerar(args.csv, args.out)


if __name__ == "__main__":
    main()