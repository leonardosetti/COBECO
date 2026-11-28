"""Seed de dados realistas e massivos para COBECO MVP v3.2.

Gera produtos, fornecedores, preços e estoque refletindo o contexto
de supermercados, lojas de departamento, hardware, livros, pet, etc.

Perfis:
  - realistico: ~25 fornecedores, 5 segmentos, produtos com marcas reais
    e quantificacoes (g, ml, kg, L, un, m).
  - expandido: ~100 fornecedores, 10 segmentos, volume para testes de carga.

Fonte: dados simulados inspirados em catalogo real de varejo.
Nao e scraping real — e sintetico para fins academicos (LGPD).
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from typing import Final, Literal

_UNIT_PATTERN: Final = re.compile(r"^(un|kg|L|m|g|ml)$")
_CENT: Final = Decimal("0.01")

Profile = Literal["realistico", "expandido"]

_EXPECTED_COUNTS: Final[dict[Profile, dict[str, int]]] = {
    "realistico": {
        "categorias": 25,
        "fornecedores": 25,
        "produtos": 106,
        "precos": 299,
        "relacoes": 101,
    },
    "expandido": {
        "categorias": 50,
        "fornecedores": 100,
        "produtos": 681,
        "precos": 3276,
        "relacoes": 330,
    },
}


@dataclass(frozen=True)
class Category:
    id: int
    name: str
    segment: str
    description: str


@dataclass(frozen=True)
class Supplier:
    id: int
    name: str
    cnpj: str
    categories: tuple[int, ...]
    segment: str


@dataclass(frozen=True)
class Product:
    id: int
    category_id: int
    name: str
    marca: str | None
    unit: str
    price: Decimal


@dataclass(frozen=True)
class Offer:
    supplier_id: int
    product_id: int
    price: Decimal
    stock: int


@dataclass(frozen=True)
class SeedDataset:
    profile: Profile
    categories: tuple[Category, ...]
    suppliers: tuple[Supplier, ...]
    products: tuple[Product, ...]
    offers: tuple[Offer, ...]
    supplier_categories: tuple[tuple[int, int], ...]

    @property
    def counts(self) -> dict[str, int]:
        return {
            "categorias": len(self.categories),
            "fornecedores": len(self.suppliers),
            "produtos": len(self.products),
            "precos": len(self.offers),
            "relacoes": len(self.supplier_categories),
        }


def normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFC", value)
    cleaned = "".join(
        " " if character.isspace() else character
        for character in normalized
        if character.isspace() or not unicodedata.category(character).startswith("C")
    )
    return re.compile(r"\s+").sub(" ", cleaned).strip()


def _money(value: Decimal) -> Decimal:
    return value.quantize(_CENT, rounding=ROUND_HALF_UP)


# ============================================================
# CATEGORIAS REAIS POR SEGMENTO (25 no perfil realistico)
# ============================================================
_REALISTICO_CATEGORIES: Final[tuple[tuple[int, str, str, str], ...]] = (
    # Supermercado / Alimentação
    (1,  "Mercearia",     "Supermercado", "Arroz, feijao, acucar, oleo, massa"),
    (2,  "Bebidas",       "Supermercado", "Refrigerantes, sucos, cerveja, agua"),
    (3,  "Limpeza",       "Supermercado", "Detergente, sabão, desinfetante"),
    (4,  "Higiene",       "Supermercado", "Sabonete, shampoo, papel higiênico"),
    (5,  "Padaria",       "Supermercado", "Paes, bolos, biscoitos"),
    (6,  "Frios e Laticínios", "Supermercado", "Queijos, presuntos, iogurtes"),
    (7,  "Açougue",       "Supermercado", "Carnes bovinas, suínas, aves"),
    (8,  "Hortifruti",    "Supermercado", "Frutas, legumes, verduras"),
    # Lojas de Departamento / Eletro
    (9,  "Eletrônicos",   "Departamento", "Celulares, tablets, acessorios"),
    (10, "Informática",   "Departamento", "Notebooks, periféricos, impressoras"),
    (11, "Eletrodomésticos","Departamento", "Geladeiras, fogões, maquinas de lavar"),
    (12, "Móveis",        "Departamento", "Sofas, camas, mesas, cadeiras"),
    (13, "Livros",        "Departamento", "Livros tecnicos, literatura, didaticos"),
    (14, "Papelaria",     "Departamento", "Cadernos, canetas, materiais escritorio"),
    # Hardware / Construção
    (15, "Ferramentas",   "Hardware", "Furadeiras, serrotes, chaves de fenda"),
    (16, "Materiais Construção", "Hardware", "Cimento, areia, tijolo, tinta"),
    (17, "Jardinagem",    "Hardware", "Vasos, adubos, ferramentas de jardim"),
    (18, "Iluminação",    "Hardware", "Lampadas, lustres, refletores"),
    # Pet
    (19, "Pet Alimentos", "Pet", "Racao para caes e gatos"),
    (20, "Pet Acessorios","Pet", "Coleiras, brinquedos, camas"),
    # Automotivo
    (21, "Peças Automotivas", "Automotivo", "Filtros, oleo, velas, pastilhas"),
    (22, "Pneus e Rodas", "Automotivo", "Pneus, rodas, calibragem"),
    # Moda
    (23, "Vestuário Masculino", "Moda", "Camisas, calças, bermudas"),
    (24, "Vestuário Feminino", "Moda", "Blusas, vestidos, saias"),
    (25, "Calçados",      "Moda", "Tenis, sapatos, sandalias"),
)

# CNPJs fictícios válidos (raiz + dígitos verificadores)
_REALISTICO_SUPPLIERS: Final[tuple[tuple[int, str, str, tuple[int, ...], str], ...]] = (
    # Supermercados (BigSellers)
    (1,  "Carrefour",              "99000111",  (1,2,3,4,5,6,7,8),   "Supermercado"),
    (2,  "Extra",                  "00111222",  (1,2,3,4,5,6,7,8),   "Supermercado"),
    (3,  "Pão de Açúcar",          "66777888",  (1,2,3,4,5,6,7,8),   "Supermercado"),
    (4,  "Walmart Brasil",         "11222333",  (1,2,3,4,5,6,7,8),   "Supermercado"),
    (5,  "Mercearia do Tio Zé",    "22333444",  (1,2,3,4,5),         "Supermercado"),
    # Lojas de Departamento (BigSellers)
    (6,  "Casas Bahia",            "33444555",  (9,10,11,12,13,14),  "Departamento"),
    (7,  "Ponto Frio",             "44555666",  (9,10,11,12,13,14),  "Departamento"),
    (8,  "Magazine Luiza",         "55666777",  (9,10,11,12,13,14),  "Departamento"),
    (9,  "Americanas",             "77666555",  (9,10,11,12,13,14),  "Departamento"),
    (10, "Livraria Saraiva",       "77888999",  (13,14),             "Departamento"),
    (11, "Livraria Cultura",       "88999000",  (13,14),             "Departamento"),
    # Hardware / Construção (MidSellers)
    (12, "Leroy Merlin",           "99000112",  (15,16,17,18),       "Hardware"),
    (13, "Telha Norte",            "11222334",  (15,16,17,18),       "Hardware"),
    (14, "Casa & Construção",      "22333445",  (15,16,17),          "Hardware"),
    # Pet (MidSellers)
    (15, "Cobasi",                 "33444556",  (19,20),             "Pet"),
    (16, "Petz",                   "44555667",  (19,20),             "Pet"),
    # Automotivo (MidSellers)
    (17, "AutoPeças São Paulo",    "55666778",  (21,22),             "Automotivo"),
    (18, "Pneus & Cia",            "66777889",  (22,),               "Automotivo"),
    # Moda (MidSellers)
    (19, "C&A",                    "77888990",  (23,24,25),          "Moda"),
    (20, "Renner",                 "88999001",  (23,24,25),          "Moda"),
    (21, "Riachuelo",              "99000113",  (23,24,25),          "Moda"),
    # Decoração / Casa (MidSellers)
    (22, "Tok&Stok",               "11222335",  (12,14,18),          "Departamento"),
    (23, "Etna",                   "22333446",  (12,14),             "Departamento"),
    (24, "Mobly",                  "33444557",  (12,14),             "Departamento"),
    (25, "Decathlon",              "44555668",  (24,25),             "Moda"),  # esporte/moda
)

# Produtos reais por categoria com marcas e quantificacoes
# Formato: (categoria_id, [(nome, marca, unidade, preco_base), ...])
_REALISTICO_PRODUCTS: Final[tuple[tuple[int, tuple[tuple[str, str, str, float], ...]], ...]] = (
    # 1 Mercearia
    (1, (
        ("Arroz Tipo 1 5kg", "Tio João", "kg", 4.99),
        ("Feijão Preto 1kg", "Camil", "kg", 7.49),
        ("Açúcar Refinado União 1kg", "União", "kg", 3.99),
        ("Açúcar Refinado Caravelas 5kg", "Caravelas", "kg", 18.90),
        ("Óleo de Soja Liza 900ml", "Liza", "ml", 6.99),
        ("Café Torrado Pilão 500g", "Pilão", "g", 12.90),
        ("Sal Refinado 1kg", "Tempero", "kg", 2.49),
        ("Macarrão Espaguete 500g", "Massako", "g", 3.49),
        ("Farinha de Trigo 1kg", "Dona Benta", "kg", 4.99),
        ("Molho de Tomate Pomodoro 500g", "Pomodoro", "g", 4.49),
    )),
    # 2 Bebidas
    (2, (
        ("Coca-Cola 2L", "Coca-Cola", "L", 7.99),
        ("Guaraná Antarctica 2L", "Guaraná", "L", 6.99),
        ("Água Mineral 500ml", "Crystal", "ml", 1.99),
        ("Cerveja Skol 350ml", "Skol", "ml", 3.49),
        ("Suco de Laranja 1L", "Del Valle", "L", 5.99),
        ("Vinho Tinto 750ml", "Miolo", "ml", 24.90),
    )),
    # 3 Limpeza
    (3, (
        ("Detergente Ypê 500ml", "Ypê", "ml", 2.99),
        ("Sabão em Pó OMO 1kg", "OMO", "kg", 16.90),
        ("Desinfetante Veja 1L", "Veja", "L", 8.90),
        ("Esponja de Aço Bombril", "Bombril", "un", 3.99),
        ("Amaciante Comfort 2L", "Comfort", "L", 12.90),
    )),
    # 4 Higiene
    (4, (
        ("Sabonete Dove 90g", "Dove", "g", 3.99),
        ("Shampoo Seda 350ml", "Seda", "ml", 9.90),
        ("Papel Higiênico Neve 4 rolos", "Neve", "un", 6.99),
        ("Escova de Dentes Colgate", "Colgate", "un", 7.90),
        ("Desodorante Rexona 50ml", "Rexona", "ml", 11.90),
    )),
    # 5 Padaria
    (5, (
        ("Pão Francês 50g", "Padaria", "g", 0.69),
        ("Biscoito Recheado 150g", "Bauducco", "g", 4.49),
        ("Bolo de Fuba 500g", "Casa", "g", 9.90),
        ("Bolacha Maria 200g", "Rivolli", "g", 3.99),
    )),
    # 6 Frios e Laticínios
    (6, (
        ("Queijo Minas 200g", "Itambé", "g", 7.99),
        ("Presunto 200g", "Sadia", "g", 8.99),
        ("Iogurte Natural 170g", "Itambé", "g", 2.99),
        ("Leite Integral 1L", "Parmalat", "L", 4.99),
    )),
    # 7 Açougue
    (7, (
        ("Carne Moída 500g", "Friboi", "g", 14.90),
        ("Frango Inteiro 1kg", "Seara", "kg", 12.90),
        ("Linguiça Toscana 500g", "Perdigão", "g", 11.90),
        ("Picanha 1kg", "Friboi", "kg", 59.90),
    )),
    # 8 Hortifruti
    (8, (
        ("Maçã 1kg", "Fuji", "kg", 6.99),
        ("Banana Prata 1kg", "Nanica", "kg", 4.99),
        ("Batata 1kg", "Agria", "kg", 3.49),
        ("Cebola 1kg", "Roxa", "kg", 3.99),
    )),
    # 9 Eletrônicos
    (9, (
        ("Smartphone Samsung Galaxy", "Samsung", "un", 1899.00),
        ("Fone Bluetooth Xiaomi", "Xiaomi", "un", 149.00),
        ("Capa para Celular", "Generico", "un", 29.90),
        ("Carregador Turbo 25W", "Samsung", "un", 89.00),
    )),
    # 10 Informática
    (10, (
        ("Notebook Dell Inspiron i5", "Dell", "un", 3499.00),
        ("Mouse Óptico Logitech", "Logitech", "un", 79.00),
        ("Teclado Mecânico Redragon", "Redragon", "un", 199.00),
        ("HD Externo 1TB", "Seagate", "un", 349.00),
    )),
    # 11 Eletrodomésticos
    (11, (
        ("Geladeira Frost Free 340L", "Brastemp", "un", 2899.00),
        ("Micro-ondas 30L", "Electrolux", "un", 549.00),
        ("Liquidificador Arno", "Arno", "un", 129.00),
        ("Ventilador de Mesa", "Britânia", "un", 149.00),
    )),
    # 12 Móveis
    (12, (
        ("Sofá 3 Lugares", "Tok&Stok", "un", 1899.00),
        ("Cama de Casal", "Madesa", "un", 899.00),
        ("Mesa de Jantar 4 lugares", "Tok&Stok", "un", 799.00),
        ("Cadeira de Escritório", "Etna", "un", 349.00),
    )),
    # 13 Livros
    (13, (
        ("Livro Técnico Python", "Casa do Código", "un", 79.90),
        ("Livro de Ficção", "Companhia", "un", 44.90),
        ("Livro Didático", "Saraiva", "un", 89.00),
        ("Revista de Tecnologia", "Exame", "un", 19.90),
    )),
    # 14 Papelaria
    (14, (
        ("Caderno 10 matérias", "Tilibra", "un", 24.90),
        ("Caneta Esferográfica BIC", "BIC", "un", 1.99),
        ("Papel A4 500 folhas", "HP", "un", 24.90),
        ("Grampo", "Generico", "un", 5.90),
    )),
    # 15 Ferramentas
    (15, (
        ("Furadeira 650W", "Bosch", "un", 249.00),
        ("Chave de Fenda Philips", "Stanley", "un", 14.90),
        ("Alicate Universal", "Tramontina", "un", 39.90),
        ("Trena 5m", "Stanley", "un", 29.90),
    )),
    # 16 Materiais Construção
    (16, (
        ("Cimento 50kg", "Votoran", "kg", 24.90),
        ("Tinta Branca 3,6L", "Suvinil", "L", 89.90),
        ("Tijolo 6 furos", "Local", "un", 1.49),
        ("Tubo PVC 2m", "Tigre", "m", 45.90),
    )),
    # 17 Jardinagem
    (17, (
        ("Vaso Plástico Cinza 50cm", "Generico", "un", 19.90),
        ("Adubo Orgânico 2kg", "Cymbrium", "kg", 24.90),
        ("Sementes de Hortelã", "Generico", "g", 8.90),
        ("Tesoura de Poda", "Tramontina", "un", 59.90),
    )),
    # 18 Iluminação
    (18, (
        ("Lâmpada LED Ericsson 50W", "Ericsson", "un", 24.90),
        ("Lustre de Sala", "Generico", "un", 149.00),
        ("Refletor LED 100W", "Generico", "un", 89.00),
        ("Abajur de Quarto", "Generico", "un", 79.00),
    )),
    # 19 Pet Alimentos
    (19, (
        ("Ração para Cães 15kg", "Pedigree", "kg", 89.90),
        ("Ração para Gatos 7,5kg", "Whiskas", "kg", 74.90),
        ("Petisco para Cães", "Premier", "un", 12.90),
        ("Areia Sanitária 5kg", "Clean", "kg", 34.90),
    )),
    # 20 Pet Acessórios
    (20, (
        ("Coleira para Cães", "Generico", "un", 24.90),
        ("Brinquedo Mordedor", "Generico", "un", 19.90),
        ("Cama para Cães", "Generico", "un", 89.00),
        ("Guia Retrátil", "Generico", "un", 34.90),
    )),
    # 21 Peças Automotivas
    (21, (
        ("Filtro de Óleo", "Mann", "un", 24.90),
        ("Óleo Motor 5W30 1L", "Mobil", "L", 44.90),
        ("Vela de Ignição", "NGK", "un", 19.90),
        ("Pastilha de Freio", "Bosch", "un", 89.00),
    )),
    # 22 Pneus e Rodas
    (22, (
        ("Pneu 185/60R15", "Pirelli", "un", 349.00),
        ("Roda de Liga 15\"", "Generico", "un", 499.00),
        ("Calibragem", "Servico", "un", 10.00),
    )),
    # 23 Vestuário Masculino
    (23, (
        ("Camisa Algodão M", "Renner", "un", 79.90),
        ("Calça Jeans 42", "Levi's", "un", 199.00),
        ("Bermuda Sarja M", "C&A", "un", 69.90),
    )),
    # 24 Vestuário Feminino
    (24, (
        ("Blusa de Algodão P", "Renner", "un", 69.90),
        ("Vestido Floral M", "C&A", "un", 119.00),
        ("Saia Jeans M", "Riachuelo", "un", 89.90),
    )),
    # 25 Calçados
    (25, (
        ("Tênis Esportivo 41", "Nike", "un", 299.00),
        ("Sapato Social 40", "Couro", "un", 199.00),
        ("Sandália Feminina", "Beira Rio", "un", 79.90),
    )),
)

# Marcas por categoria para produtos gerados dinamicamente (expandido)
_CATEGORY_BRANDS: Final[dict[int, tuple[str, ...]]] = {
    1: ("Tio João", "Camil", "União", "Caravelas", "Liza", "Massako", "Dona Benta", "Pomodoro"),
    2: ("Coca-Cola", "Guaraná", "Crystal", "Skol", "Del Valle", "Miolo"),
    3: ("Ypê", "OMO", "Veja", "Bombril", "Comfort"),
    4: ("Dove", "Seda", "Neve", "Colgate", "Rexona"),
    5: ("Bauducco", "Rivolli", "Casa", "Padaria"),
    6: ("Itambé", "Sadia", "Parmalat", "Friboi"),
    7: ("Friboi", "Seara", "Perdigão"),
    8: ("Fuji", "Nanica", "Agria", "Roxa"),
    9: ("Samsung", "Xiaomi", "Generico"),
    10: ("Dell", "Logitech", "Redragon", "Seagate"),
    11: ("Brastemp", "Electrolux", "Arno", "Britânia"),
    12: ("Tok&Stok", "Madesa", "Etna"),
    13: ("Casa do Código", "Companhia", "Saraiva", "Exame"),
    14: ("Tilibra", "BIC", "HP", "Generico"),
    15: ("Bosch", "Stanley", "Tramontina"),
    16: ("Votoran", "Suvinil", "Tigre", "Local"),
    17: ("Cymbrium", "Generico", "Tramontina"),
    18: ("Ericsson", "Generico"),
    19: ("Pedigree", "Whiskas", "Premier", "Clean"),
    20: ("Generico",),
    21: ("Mann", "Mobil", "NGK", "Bosch"),
    22: ("Pirelli", "Generico", "Servico"),
    23: ("Renner", "Levi's", "C&A"),
    24: ("Renner", "C&A", "Riachuelo"),
    25: ("Nike", "Couro", "Beira Rio"),
}

# Nomes de produtos genéricos por categoria para expansão (variantes)
_CATEGORY_PRODUCT_NAMES: Final[dict[int, tuple[str, ...]]] = {
    1: ("Arroz", "Feijão", "Açúcar", "Óleo", "Café", "Sal", "Macarrão", "Farinha", "Molho", "Grão de Bico"),
    2: ("Refrigerante", "Água", "Cerveja", "Suco", "Vinho", "Energético", "Chá", "Cerveja Artesanal"),
    3: ("Detergente", "Sabão", "Desinfetante", "Esponja", "Amaciante", "Limpador", "Alvejante", "Saponáceo"),
    4: ("Sabonete", "Shampoo", "Papel Higiênico", "Escova", "Desodorante", "Creme Dental", "Absorvente", "Condicionador"),
    5: ("Pão", "Biscoito", "Bolo", "Bolacha", "Torrada", "Rosca", "Pão de Queijo", "Croissant"),
    6: ("Queijo", "Presunto", "Iogurte", "Leite", "Manteiga", "Requeijão", "Ricota", "Margarina"),
    7: ("Carne Moída", "Frango", "Linguiça", "Picanha", "Costela", "Filé", "Alcatra", "Contra-filé"),
    8: ("Maçã", "Banana", "Batata", "Cebola", "Laranja", "Tomate", "Alface", "Cenoura"),
    9: ("Smartphone", "Fone", "Capa", "Carregador", "Power Bank", "Cabo USB", "Fone Ouvido", "Smartwatch"),
    10: ("Notebook", "Mouse", "Teclado", "HD", "Memória RAM", "Placa de Vídeo", "Monitor", "Impressora"),
    11: ("Geladeira", "Micro-ondas", "Liquidificador", "Ventilador", "Fogão", "Lava-louças", "Aspirador", "Batedeira"),
    12: ("Sofá", "Cama", "Mesa", "Cadeira", "Guarda-roupa", "Estante", "Rack", "Poltrona"),
    13: ("Livro Técnico", "Livro Ficção", "Livro Didático", "Revista", "Dicionário", "Quadrinho", "Biografia", "Poesia"),
    14: ("Caderno", "Caneta", "Papel A4", "Grampo", "Lápis", "Borracha", "Estojo", "Pasta"),
    15: ("Furadeira", "Chave de Fenda", "Alicate", "Trena", "Martelo", "Serrote", "Lixa", "Conjunto de Chaves"),
    16: ("Cimento", "Tinta", "Tijolo", "Tubo PVC", "Areia", "Brita", "Tubo de Cobre", "Válvula"),
    17: ("Vaso", "Adubo", "Semente", "Tesoura", "Regador", "Pá", "Luvas", "Adubo Líquido"),
    18: ("Lâmpada", "Lustre", "Refletor", "Abajur", "Fita LED", "Spots", "Luminária", "Interruptor"),
    19: ("Ração Cão", "Ração Gato", "Petisco", "Areia", "Comedouro", "Bebedouro", "Cama Pet", "Casinha"),
    20: ("Coleira", "Brinquedo", "Cama", "Guia", "Escova", "Shampoo Pet", "Roupinha", "Casinha"),
    21: ("Filtro Óleo", "Óleo Motor", "Vela", "Pastilha", "Correia", "Bateria", "Bujão", "Lâmpada Farol"),
    22: ("Pneu", "Roda", "Calibragem", "Balanceamento", "Câmara", "Válvula", "Capa de Roda", "Aro"),
    23: ("Camisa", "Calça", "Bermuda", "Camiseta", "Blusão", "Jaqueta", "Cinto", "Meia"),
    24: ("Blusa", "Vestido", "Saia", "Shorts", "Camiseta", "Regata", "Calça Legging", "Jaqueta"),
    25: ("Tênis", "Sapato", "Sandália", "Bota", "Chinelo", "Sapatênis", "Mocassim", "Scarpin"),
}

# Expandido: mais fornecedores por segmento
_EXPANDIDO_EXTRA_SUPPLIERS: Final[tuple[tuple[str, str, tuple[int, ...], str], ...]] = (
    ("Assaí",   "66777890", (1,2,3,4,5,6,7,8), "Supermercado"),
    ("Dia",     "77888991", (1,2,3,4,5),         "Supermercado"),
    ("Savegnago","88999002", (1,2,3,4,5),        "Supermercado"),
    ("Pão Rural","99000114", (1,2,3,4,5,6),      "Supermercado"),
    # Departamento adicionais
    ("Kabum",   "11222336", (9,10),              "Departamento"),
    ("Terabyte","22333447", (9,10),              "Departamento"),
    ("Submarino","33444558", (9,10,13,14),       "Departamento"),
    ("Shoptime","44555669", (9,10,11,12),        "Departamento"),
    ("Lojas Americanas Fisicas","55666780",(9,10,12),"Departamento"),
    # Hardware adicionais
    ("Casa do Construtor","66777891",(15,16,17),"Hardware"),
    ("Construfacil","77888992",(15,16,17),"Hardware"),
    ("Lojas Pomar","88999003",(15,16,17),"Hardware"),
    ("C&C","99000115",(15,16,17),"Hardware"),
    # Pet adicionais
    ("Pet Love","11222337",(19,20),"Pet"),
    ("Cobasi Express","22333448",(19,20),"Pet"),
    # Automotivo adicionais
    ("Nakata","33444559",(21,22),"Automotivo"),
    ("Bosch Car Service","44555670",(21,22),"Automotivo"),
    # Moda adicionais
    ("C&A Outlet","55666781",(23,24,25),"Moda"),
    ("Renner Loja","66777892",(23,24,25),"Moda"),
    ("Riachuelo Loja","77888993",(23,24,25),"Moda"),
    ("Marisa","88999004",(23,24,25),"Moda"),
    ("C&A Centro","99000116",(23,24,25),"Moda"),
    # Esportes
    ("Centauro","11222338",(24,25),"Moda"),
    ("Netshoes","22333449",(24,25),"Moda"),
    ("Tennis World","33444560",(24,25),"Moda"),
    ("Decathlon Store","44555671",(24,25),"Moda"),
)


# ============================================================
# CNPJ utilities (duplicado para manter este arquivo standalone)
# ============================================================
_CNPJ_PATTERN: Final = re.compile(r"^\d{2}\.\d{3}\.\d{3}/0001-\d{2}$")
_CNPJ_MODULUS: Final = 11
_CNPJ_ZERO_THRESHOLD: Final = 2


def _cnpj_check_digits(base: str) -> str:
    first_weights = (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 11, 2)
    second_weights = (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
    first_sum = sum(int(d) * w for d, w in zip(base, first_weights, strict=True))
    first_check = 0 if first_sum % _CNPJ_MODULUS < _CNPJ_ZERO_THRESHOLD else _CNPJ_MODULUS - first_sum % _CNPJ_MODULUS
    with_first = f"{base}{first_check}"
    second_sum = sum(int(d) * w for d, w in zip(with_first, second_weights, strict=True))
    second_check = 0 if second_sum % _CNPJ_MODULUS < _CNPJ_ZERO_THRESHOLD else _CNPJ_MODULUS - second_sum % _CNPJ_MODULUS
    return f"{first_check}{second_check}"


def make_cnpj(base: str) -> str:
    if not re.fullmatch(r"\d{8}", base):
        raise ValueError("a raiz do CNPJ deve conter exatamente 8 dígitos")
    digits = f"{base}0001"
    cd = _cnpj_check_digits(digits)
    return f"{base[:2]}.{base[2:5]}.{base[5:8]}/0001-{cd}"


def is_valid_cnpj(value: str) -> bool:
    if not _CNPJ_PATTERN.fullmatch(value):
        return False
    digits = value.replace(".", "").replace("/", "").replace("-", "")
    if digits == digits[0] * 14:
        return False
    return digits[-2:] == _cnpj_check_digits(digits[:12])


# ============================================================
# Unit inference
# ============================================================
def _infer_unit(name: str) -> str:
    n = name.casefold()
    if re.search(r"\d+\s*kg\b", n): return "kg"
    if re.search(r"\d+\s*g\b", n): return "g"
    if re.search(r"\d+\s*ml\b", n): return "ml"
    if re.search(r"\d+\s*l\b", n): return "L"
    if re.search(r"\d+(?:[,.]\d+)?\s*(?:cm|m)\b", n): return "m"
    return "un"


# ============================================================
# Price base per category
# ============================================================
_CATEGORY_BASE_PRICES: Final[dict[int, Decimal]] = {
    1: Decimal("12.90"),   # Mercearia
    2: Decimal("6.99"),    # Bebidas
    3: Decimal("4.99"),    # Limpeza
    4: Decimal("8.90"),    # Higiene
    5: Decimal("4.99"),    # Padaria
    6: Decimal("7.99"),    # Frios
    7: Decimal("14.90"),   # Açougue
    8: Decimal("5.99"),    # Hortifruti
    9: Decimal("899.00"),  # Eletrônicos
    10: Decimal("1299.00"),# Informática
    11: Decimal("899.00"), # Eletrodomésticos
    12: Decimal("799.00"), # Móveis
    13: Decimal("59.90"),  # Livros
    14: Decimal("19.90"),  # Papelaria
    15: Decimal("89.90"),  # Ferramentas
    16: Decimal("24.90"),  # Materiais Construção
    17: Decimal("24.90"),  # Jardinagem
    18: Decimal("49.90"),  # Iluminação
    19: Decimal("69.90"),  # Pet Alimentos
    20: Decimal("34.90"),  # Pet Acessórios
    21: Decimal("44.90"),  # Peças Automotivas
    22: Decimal("349.00"), # Pneus
    23: Decimal("89.90"),  # Vestuário Masc
    24: Decimal("89.90"),  # Vestuário Fem
    25: Decimal("149.00"), # Calçados
    # Categorias expandidas (26-50)
    26: Decimal("29.90"), 27: Decimal("39.90"), 28: Decimal("59.90"), 29: Decimal("79.90"), 30: Decimal("99.90"),
    31: Decimal("24.90"), 32: Decimal("34.90"), 33: Decimal("44.90"), 34: Decimal("54.90"), 35: Decimal("64.90"),
    36: Decimal("74.90"), 37: Decimal("84.90"), 38: Decimal("94.90"), 39: Decimal("104.90"), 40: Decimal("114.90"),
    41: Decimal("124.90"), 42: Decimal("134.90"), 43: Decimal("144.90"), 44: Decimal("154.90"), 45: Decimal("164.90"),
    46: Decimal("174.90"), 47: Decimal("184.90"), 48: Decimal("194.90"), 49: Decimal("204.90"), 50: Decimal("214.90"),
}


def _base_price(category_id: int, product_index: int) -> Decimal:
    base = _CATEGORY_BASE_PRICES[category_id]
    increment = Decimal(product_index * 5 + (product_index % 3) * 2)
    return _money(base + increment)


# ============================================================
# Supplier factor (price variation by supplier)
# ============================================================
def _supplier_factor(supplier_id: int) -> Decimal:
    """Fator de preço por fornecedor para gerar variação realista."""
    return Decimal("0.90") + Decimal(((supplier_id * 7) % 21)) / Decimal("100")


# ============================================================
# Build realistico
# ============================================================
def _build_realistico() -> SeedDataset:
    categories = tuple(
        Category(id=cid, name=normalize_text(nome), segment=seg, description=normalize_text(desc))
        for cid, nome, seg, desc in _REALISTICO_CATEGORIES
    )

    suppliers = tuple(
        Supplier(
            id=sid,
            name=normalize_text(nome),
            cnpj=make_cnpj(cnpj),
            categories=tuple(sorted(cats)),
            segment=seg,
        )
        for sid, nome, cnpj, cats, seg in _REALISTICO_SUPPLIERS
    )

    products: list[Product] = []
    product_id = 1
    for category_id, items in _REALISTICO_PRODUCTS:
        brands = _CATEGORY_BRANDS.get(category_id, ("Generico",))
        for idx, (nome, marca, unit, price) in enumerate(items):
            products.append(
                Product(
                    id=product_id,
                    category_id=category_id,
                    name=normalize_text(nome),
                    marca=normalize_text(marca),
                    unit=unit,
                    price=_money(Decimal(str(price))),
                )
            )
            product_id += 1

    # Ofertas: cada fornecedor oferece um subconjunto de produtos de suas categorias
    suppliers_by_category: dict[int, tuple[int, ...]] = {
        cid: tuple(s.id for s in suppliers if cid in s.categories)
        for cid in range(1, len(categories) + 1)
    }
    all_supplier_ids = tuple(s.id for s in suppliers)
    offers: list[Offer] = []
    for product in products:
        eligible = suppliers_by_category.get(product.category_id, ())
        # Cada produto é oferecido por 2-4 fornecedores da mesma categoria
        n_offers = min(len(eligible), 3 if len(eligible) >= 3 else len(eligible))
        selected = list(eligible[:n_offers])
        for sid in selected:
            fator = _supplier_factor(sid)
            preco = _money(product.price * fator)
            estoque = (sid * 31 + product.id * 17) % 1000 + 10
            offers.append(Offer(supplier_id=sid, product_id=product.id, price=preco, stock=estoque))

    supplier_categories = tuple(
        sorted((s.id, cid) for s in suppliers for cid in s.categories)
    )
    return SeedDataset(
        profile="realistico",
        categories=categories,
        suppliers=suppliers,
        products=tuple(products),
        offers=tuple(offers),
        supplier_categories=supplier_categories,
    )


# ============================================================
# Build expandido
# ============================================================
def _build_expandido() -> SeedDataset:
    # Categorias: as 25 reais + 25 geradas
    extra_categories = tuple(
        Category(
            id=cid,
            name=normalize_text(f"Categoria Extra {cid}"),
            segment="Extra",
            description="Categoria gerada para testes de carga",
        )
        for cid in range(26, 51)
    )
    categories = tuple(
        Category(id=cid, name=normalize_text(nome), segment=seg, description=normalize_text(desc))
        for cid, nome, seg, desc in _REALISTICO_CATEGORIES
    ) + extra_categories

    # Fornecedores: os 25 reais + extras
    suppliers: list[Supplier] = []
    for sid, nome, cnpj, cats, seg in _REALISTICO_SUPPLIERS:
        suppliers.append(
            Supplier(id=sid, name=normalize_text(nome), cnpj=make_cnpj(cnpj),
                     categories=tuple(sorted(cats)), segment=seg)
        )
    sid = 26
    for nome, cnpj, cats, seg in _EXPANDIDO_EXTRA_SUPPLIERS:
        suppliers.append(
            Supplier(id=sid, name=normalize_text(nome), cnpj=make_cnpj(cnpj),
                     categories=tuple(sorted(cats)), segment=seg)
        )
        sid += 1
    # Mais fornecedores genéricos para chegar a 100
    for i in range(sid, 101):
        suppliers.append(
            Supplier(id=i, name=normalize_text(f"Fornecedor Genérico {i}"),
                     cnpj=make_cnpj(f"{10000000 + i:08d}"),
                     categories=(1, 2, 3), segment="Extra")
        )

    products: list[Product] = []
    product_id = 1
    for category in categories:
        brands = _CATEGORY_BRANDS.get(category.id, ("Generico",))
        names = _CATEGORY_PRODUCT_NAMES.get(category.id, ("Produto",))
        for idx, base_name in enumerate(names):
            for variant_idx, variant in enumerate(("Original", "Premium", "Eco")):
                if product_id > 5000:
                    break
                brands_cycle = brands[(product_id - 1) % len(brands)]
                products.append(
                    Product(
                        id=product_id,
                        category_id=category.id,
                        name=normalize_text(f"{category.name} - {base_name} - {variant}"),
                        marca=normalize_text(brands_cycle),
                        unit=_infer_unit(base_name),
                        price=_base_price(category.id, idx),
                    )
                )
                product_id += 1
            if product_id > 5000:
                break
        if product_id > 5000:
            break

    suppliers_by_category: dict[int, tuple[int, ...]] = {
        cid: tuple(s.id for s in suppliers if cid in s.categories)
        for cid in range(1, len(categories) + 1)
    }
    all_supplier_ids = tuple(s.id for s in suppliers)
    offers: list[Offer] = []
    for product in products:
        eligible = suppliers_by_category.get(product.category_id, ())
        n_offers = min(len(eligible), 6 if len(eligible) >= 6 else max(len(eligible), 1))
        selected = list(eligible[:n_offers])
        for sid in selected:
            fator = _supplier_factor(sid)
            preco = _money(product.price * fator)
            estoque = (sid * 31 + product.id * 17) % 1000 + 10
            offers.append(Offer(supplier_id=sid, product_id=product.id, price=preco, stock=estoque))

    supplier_categories = tuple(
        sorted((s.id, cid) for s in suppliers for cid in s.categories)
    )
    return SeedDataset(
        profile="expandido",
        categories=categories,
        suppliers=tuple(suppliers),
        products=tuple(products),
        offers=tuple(offers),
        supplier_categories=supplier_categories,
    )


# ============================================================
# Validation
# ============================================================
def validate_dataset(dataset: SeedDataset) -> None:
    if dataset.counts != _EXPECTED_COUNTS[dataset.profile]:
        raise ValueError(
            f"contagens inválidas para {dataset.profile}: {dataset.counts}; "
            f"esperado {_EXPECTED_COUNTS[dataset.profile]}"
        )
    category_ids = {c.id for c in dataset.categories}
    supplier_ids = {s.id for s in dataset.suppliers}
    product_ids = {p.id for p in dataset.products}
    if len(category_ids) != len(dataset.categories):
        raise ValueError("IDs de categoria duplicados")
    if len(supplier_ids) != len(dataset.suppliers):
        raise ValueError("IDs de fornecedor duplicados")
    if len(product_ids) != len(dataset.products):
        raise ValueError("IDs de produto duplicados")
    cat_names = [c.name.casefold() for c in dataset.categories]
    sup_names = [s.name.casefold() for s in dataset.suppliers]
    prod_names = [p.name.casefold() for p in dataset.products]
    if len(cat_names) != len(set(cat_names)):
        raise ValueError("nomes de categoria duplicados")
    if len(sup_names) != len(set(sup_names)):
        raise ValueError("nomes de fornecedor duplicados")
    if len(prod_names) != len(set(prod_names)):
        raise ValueError("nomes de produto duplicados")
    if len({s.cnpj for s in dataset.suppliers}) != len(dataset.suppliers):
        raise ValueError("CNPJs duplicados")
    if not all(is_valid_cnpj(s.cnpj) for s in dataset.suppliers):
        raise ValueError("CNPJ inválido")
    for product in dataset.products:
        if product.category_id not in category_ids:
            raise ValueError(f"produto {product.id} referencia categoria inexistente")
        if not _UNIT_PATTERN.fullmatch(product.unit):
            raise ValueError(f"unidade inválida no produto {product.id}: {product.unit}")
        if product.price < 0 or product.price.as_tuple().exponent != -2:
            raise ValueError(f"preço inválido no produto {product.id}: {product.price}")
    relation_keys = set()
    for sid, cid in dataset.supplier_categories:
        if sid not in supplier_ids or cid not in category_ids:
            raise ValueError(f"relação inválida: {sid}, {cid}")
        key = (sid, cid)
        if key in relation_keys:
            raise ValueError(f"relação duplicada: {key}")
        relation_keys.add(key)
    offer_keys = set()
    for offer in dataset.offers:
        if offer.supplier_id not in supplier_ids or offer.product_id not in product_ids:
            raise ValueError(f"oferta inválida: {offer}")
        key = (offer.supplier_id, offer.product_id)
        if key in offer_keys:
            raise ValueError(f"oferta duplicada: {key}")
        offer_keys.add(key)
        if offer.price < 0 or offer.price.as_tuple().exponent != -2:
            raise ValueError(f"preço inválido na oferta {key}: {offer.price}")
        if not 0 <= offer.stock <= 9999:
            raise ValueError(f"estoque inválido na oferta {key}: {offer.stock}")


# ============================================================
# Public builder
# ============================================================
def build_dataset(profile: Profile) -> SeedDataset:
    if profile == "realistico":
        dataset = _build_realistico()
    elif profile == "expandido":
        dataset = _build_expandido()
    else:
        raise ValueError(f"perfil inválido: {profile}")
    validate_dataset(dataset)
    return dataset

