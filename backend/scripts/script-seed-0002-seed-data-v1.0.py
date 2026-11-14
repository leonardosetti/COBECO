"""Fonte canônica e determinística dos dados mockados do COBECO.

O módulo não depende do backend e pode ser usado pelo gerador SQL e pelos testes.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from typing import Final, Literal

# ruff: noqa: TRY003

Profile = Literal["baseline", "expanded"]
_UNIT_PATTERN: Final = re.compile(r"^(un|kg|L|m)$")
_SPACE_PATTERN: Final = re.compile(r"\s+")
_CNPJ_PATTERN: Final = re.compile(r"^\d{2}\.\d{3}\.\d{3}/0001-\d{2}$")
_CENT: Final = Decimal("0.01")
_CNPJ_MODULUS: Final = 11
_CNPJ_ZERO_THRESHOLD: Final = 2
_BASELINE_OFFERS_PER_PRODUCT: Final = 6
_PRICE_EXPONENT: Final = -2
_MAX_STOCK: Final = 9999
_EXPECTED_COUNTS: Final[dict[Profile, dict[str, int]]] = {
    "baseline": {
        "categorias": 11,
        "fornecedores": 10,
        "produtos": 50,
        "precos": 300,
        "relacoes": 25,
    },
    "expanded": {
        "categorias": 26,
        "fornecedores": 60,
        "produtos": 2_600,
        "precos": 31_200,
        "relacoes": 312,
    },
}


@dataclass(frozen=True)
class Segment:
    name: str
    categories: tuple[str, ...]


@dataclass(frozen=True)
class Category:
    id: int
    name: str
    segment: str
    description: str
    proddoc-arch-0006-uc-v1ts: tuple[str, ...]


@dataclass(frozen=True)
class Supplier:
    id: int
    name: str
    cnpj: str
    categories: tuple[int, ...]


@dataclass(frozen=True)
class Proddoc-arch-0006-uc-v1t:
    id: int
    category_id: int
    name: str
    unit: str
    price: Decimal


@dataclass(frozen=True)
class Offer:
    supplier_id: int
    proddoc-arch-0006-uc-v1t_id: int
    price: Decimal
    stock: int


@dataclass(frozen=True)
class SeedDataset:
    profile: Profile
    categories: tuple[Category, ...]
    suppliers: tuple[Supplier, ...]
    proddoc-arch-0006-uc-v1ts: tuple[Proddoc-arch-0006-uc-v1t, ...]
    offers: tuple[Offer, ...]
    supplier_categories: tuple[tuple[int, int], ...]

    @property
    def counts(self) -> dict[str, int]:
        return {
            "categorias": len(self.categories),
            "fornecedores": len(self.suppliers),
            "produtos": len(self.proddoc-arch-0006-uc-v1ts),
            "precos": len(self.offers),
            "relacoes": len(self.supplier_categories),
        }


def normalize_text(value: str) -> str:
    """Normaliza texto para Unicode NFC, sem controles e com espaços canônicos."""
    normalized = unicodedata.normalize("NFC", value)
    cleaned = "".join(
        " " if character.isspace() else character
        for character in normalized
        if character.isspace() or not unicodedata.category(character).startswith("C")
    )
    return _SPACE_PATTERN.sub(" ", cleaned).strip()


def _category(
    category_id: int,
    name: str,
    segment: str,
    description: str,
    proddoc-arch-0006-uc-v1ts: str,
) -> Category:
    return Category(
        id=category_id,
        name=normalize_text(name),
        segment=normalize_text(segment),
        description=normalize_text(description),
        proddoc-arch-0006-uc-v1ts=tuple(normalize_text(item) for item in proddoc-arch-0006-uc-v1ts.split("|")),
    )


CATEGORIES: Final[tuple[Category, ...]] = (
    _category(
        1,
        "Mercado",
        "Alimentação e hogar",
        "Supermercados, mercearias e atacados",
        "Arroz Tipo 1 5kg|Feijão Preto 1kg|Óleo de Soja 900ml|Açúcar Cristal 1kg|Sal Refinado 1kg|"
        "Macarrão Espaguete 500g|Leite Integral 1L|Café Torrado 500g|Pão de Forma 500g|Manteiga 200g",
    ),
    _category(
        2,
        "Vestuário",
        "Moda e acessórios",
        "Roupas, calçados e acessórios",
        "Camiseta Algodão M|Calça Jeans Masculina 42|Vestido Floral M|Tênis Esportivo 41|"
        "Meia Cano Curto|Cinto Couro Sintético|Boné Aba Curva|Luva de Lã|Cachecol Tricô|Jaqueta Jeans G",
    ),
    _category(
        3,
        "Automotivos",
        "Mobilidade",
        "Peças, acessórios e serviços automotivos",
        "Óleo de Motor|Filtro de Óleo|Bateria|Pneu|Freio|Correia|Vela|Graxa|Palha|Farol Automotivo",
    ),
    _category(
        4,
        "Informática",
        "Tecnologia e comunicação",
        "Computadores, periféricos e eletrônicos",
        "Notebook i5 8GB 256GB SSD|Mouse Óptico USB|Teclado Mecânico ABNT2|Monitor 24 Full HD|"
        "HD Externo 1TB USB 3.0|Pen Drive 64GB|Cabo HDMI 2m|Webcam HD 720p|Headset Gamer USB|"
        "Carregador Notebook 65W",
    ),
    _category(
        5,
        "Decoração",
        "Casa e construção",
        "Itens de decoração e artigos para casa",
        "Vaso de Cerâmica 30cm|Quadro Decorativo 40x50|Tapete Sala 2x3m|Cortina Blackout 2,5x3m|"
        "Almofada 45x45cm|Porta-retrato 15x20|Relógio de Parede 30cm|Espelho Redondo 60cm|"
        "Luminária de Mesa|Cesto Organizador 40L",
    ),
    _category(
        6,
        "Móveis",
        "Casa e construção",
        "Móveis residenciais e corporativos",
        "Sofá|Cadeira de Mesa|Mesa de Jantar|Cama de Casal|Armário|Estante|Banco|Puffs|Poltrona|Escrivaninha",
    ),
    _category(
        7,
        "Materiais de Construção e Ferragens",
        "Casa e construção",
        "Materiais de construção, ferramentas e ferragens",
        "Cimento|Areia|Tijolo|Tubo PVC|Fita Isolante|Lâmina de Serra|Parafuso|Prego|Tinta|Reboco",
    ),
    _category(
        8,
        "Ferramentas",
        "Casa e construção",
        "Ferramentas manuais, elétricas e de medição",
        "Martelo de Unha 25mm|Chave de Fenda Philips 2|Alicate Universal 8|Trena 5m|Nível Bolha 40cm|"
        "Parafusadeira Elétrica 12V|Furadeira de Impacto 650W|Serra Circular 7¼|Lixadeira Orbital|"
        "Jogo de Chaves Allen",
    ),
    _category(
        9,
        "Livros",
        "Cultura e entretenimento",
        "Livros, revistas e publicações",
        "Romance|Dicionário|Livro Técnico|História do Brasil|Livro Infantil|Poesia|Biografia|"
        "Ficção Científica|Culinária|Revista",
    ),
    _category(
        10,
        "Jardinagem",
        "Casa e construção",
        "Plantas, ferramentas e artigos de jardim",
        "Regador|Vaso de Plantas|Adubo|Sementes|Pá de Jardim|Tesoura de Poda|Luvas|Mangueira|"
        "Pulverizador|Suporte para Plantas",
    ),
    _category(
        11,
        "Eletrodomésticos",
        "Casa e construção",
        "Eletrodomésticos de linha branca e marrom",
        "Geladeira Frost Free 340L|Fogão 4 Bocas Inox|Micro-ondas 30L|Lava-louças 8 Serviços|"
        "Ar Condicionado 9000 BTU|Lavadora|Secadora|Cozinheira|Forno|Liquidificador",
    ),
    _category(
        12,
        "Bebidas",
        "Alimentação e hogar",
        "Bebidas e drinks",
        "Água Mineral|Sdoc-arch-0006-uc-v1o de Laranja|Cerveja|Vinho Tinto|Refrigerante|Chá|Energético|Café Toddy|"
        "Whisky|Azeite de Oliva",
    ),
    _category(
        13,
        "Limpeza e Higiene",
        "Alimentação e hogar",
        "Produtos de limpeza e higiene",
        "Detergente|Sabão em Pó|Amaciante|Desinfetante|Papel Higiênico|Álcool|Água Sanitária|"
        "Sabão Líquido|Esponja|Saco de Lixo",
    ),
    _category(
        14,
        "Calçados e Bolsas",
        "Moda e acessórios",
        "Calçados, bolsas e acessórios de uso diário",
        "Tênis Esportivo|Sapatilha|Sapato Social|Sandália|Bota|Chinelo|Coilinha|Mochila|Bolsa de Couro|"
        "Carteira",
    ),
    _category(
        15,
        "Óculos e Relógios",
        "Moda e acessórios",
        "Óculos, relógios e acessórios",
        "Óculos de Sol|Óculos de Grau|Relógio Digital|Relógio Analógico|Pulseira de Couro|Brinco|"
        "Corrente de Prata|Estojo|Porta-Óculos|Chaveiro",
    ),
    _category(
        16,
        "Celulares e Telecomunicações",
        "Tecnologia e comunicação",
        "Celulares, tablets e acessórios de telecomunicações",
        "Smartphone|Smartwatch|Tablet|Chip SIM|Cabo de Dados|Carregador Turbo|Fone Bluetooth|"
        "Case para Celular|Power Bank|Carregador Veicular",
    ),
    _category(
        17,
        "Games e Acessórios",
        "Tecnologia e comunicação",
        "Consoles, jogos e acessórios",
        "Controle de Videogame|Jogo Digital|Headset Gamer|Controle Sem Fio|Base para Controle|"
        "Cadeira Gamer|Volante|Minijogo|Caixa de Armazenamento|Adaptador",
    ),
    _category(
        18,
        "Bicicletas e Mobilidade",
        "Mobilidade",
        "Bicicletas, acessórios e equipamentos de mobilidade",
        "Bicicleta Urbana|Bicicleta de Montanha|Bicicleta Dobrável|Capacete|Ciclomputer|Farol de Bicicleta|"
        "Pneu de Bicicleta|Pedal|Corrente|Bomba de Ar",
    ),
    _category(
        19,
        "Farmácia e Saúde",
        "Saúde e bem-estar",
        "Medicamentos, equipamentos e cuidados com a saúde",
        "Analgésico|Antisséptico|Bandagem|Termômetro|Complexo Vitamínico|Anti-histamínico|"
        "Solução Fisiológica|Caneta|Medidor de Glicose|Máscara Descartável",
    ),
    _category(
        20,
        "Beleza e Cuidados Pessoais",
        "Saúde e bem-estar",
        "Cosméticos, higiene e cuidados pessoais",
        "Shampoo|Condicionador|Sabonete Facial|Creme Hidratante|Protetor Solar|Perfume|Batom|Esmalte|"
        "Secador de Cabelo|Máquina de Cortar",
    ),
    _category(
        21,
        "Papelaria e Escritório",
        "Escritório e estudo",
        "Papelaria, organização e produtos de escritório",
        "Caneta Esferográfica|Caderno|Pasta Suspensa|Papel A4|Calculadora|Estojo|Borracha|Marcador|"
        "Envelope|Agenda",
    ),
    _category(
        22,
        "Esportes e Lazer",
        "Esporte e lazer",
        "Equipamentos esportivos e academia",
        "Bola de Futebol|Tênis de Corrida|Camiseta Esportiva|Halter|Tapete de Yoga|Garrafa Térmica|"
        "Luvas de Treino|Peso de Treino|Kettlebell|Corda de Pular",
    ),
    _category(
        23,
        "Camping e Outdoor",
        "Esporte e lazer",
        "Equipamentos de camping e atividades ao ar livre",
        "Tenda|Saco de Dormir|Lanterna|Fogão de Camping|Mochila de Montanha|Rede de Descanso|Hamaca|"
        "Reservatório de Água|Capa de Chuva|Isca Térmica",
    ),
    _category(
        24,
        "Brinquedos e Infantil",
        "Infância, pet e consumo operacional",
        "Brinquedos e produtos infantis",
        "Carrinho|Boneca|Blocos de Montar|Quebra-cabeça|Taco de Bebê|Pelúcia|Jogo de Tabuleiro|"
        "Pipa|Patinete|Livro Colorido",
    ),
    _category(
        25,
        "Pet",
        "Infância, pet e consumo operacional",
        "Alimentos e acessórios para animais de estimação",
        "Ração para Cães|Ração para Gatos|Petisco|Areia Sanitária|Brinquedo Mordedor|Coleira|"
        "Guia Retrátil|Tapete Higiênico|Shampoo para Pet|Comedouro",
    ),
    _category(
        26,
        "Embalagens e Descartáveis",
        "Infância, pet e consumo operacional",
        "Embalagens, descartáveis e materiais de proteção",
        "Caixa de Papelão|Envelope de Expedição|Fita Adesiva|Filme Plástico|Sacola Plástica|"
        "Papel Manteiga|Isopor|Fita Kraft|Etiqueta Adesiva|Sacola Kraft",
    ),
)


SEGMENTS: Final[tuple[Segment, ...]] = (
    Segment("Alimentação e hogar", ("Mercado", "Bebidas", "Limpeza e Higiene")),
    Segment("Moda e acessórios", ("Vestuário", "Calçados e Bolsas", "Óculos e Relógios")),
    Segment(
        "Casa e construção",
        (
            "Decoração",
            "Móveis",
            "Eletrodomésticos",
            "Materiais de Construção e Ferragens",
            "Ferramentas",
            "Jardinagem",
        ),
    ),
    Segment(
        "Tecnologia e comunicação",
        ("Informática", "Celulares e Telecomunicações", "Games e Acessórios"),
    ),
    Segment("Mobilidade", ("Automotivos", "Bicicletas e Mobilidade")),
    Segment("Saúde e bem-estar", ("Farmácia e Saúde", "Beleza e Cuidados Pessoais")),
    Segment("Cultura e entretenimento", ("Livros",)),
    Segment("Esporte e lazer", ("Esportes e Lazer", "Camping e Outdoor")),
    Segment("Escritório e estudo", ("Papelaria e Escritório",)),
    Segment(
        "Infância, pet e consumo operacional",
        ("Brinquedos e Infantil", "Pet", "Embalagens e Descartáveis"),
    ),
)


_BASELINE_SUPPLIERS: Final[tuple[tuple[str, str, tuple[int, ...]], ...]] = (
    ("Leroy Merlin", "11222333", (5, 7, 8, 10)),
    ("Etna", "22333444", (5, 6)),
    ("C&A", "33444555", (2,)),
    ("Renner", "44455666", (2,)),
    ("Hering", "55666777", (2,)),
    ("Pão de Açúcar", "66777888", (1,)),
    ("Magazine Luiza", "77888999", (4, 6, 11)),
    ("Casas Bahia", "88999000", (4, 6, 11)),
    ("Carrefour", "99000111", (1, 2, 3, 4, 5, 11)),
    ("Extra", "00111222", (1, 2, 11)),
)
_BASELINE_PRODUCT_GROUPS: Final[tuple[tuple[int, int], ...]] = (
    (1, 10),
    (8, 10),
    (4, 10),
    (2, 10),
    (5, 5),
    (11, 5),
)
_VARIANTS: Final[tuple[str, ...]] = (
    "Original",
    "Premium",
    "Essencial",
    "Pro",
    "Plus",
    "Compacto",
    "Família",
    "Profissional",
    "Eco",
    "Kit",
)
_VARIANT_FACTORS: Final[tuple[Decimal, ...]] = (
    Decimal("0.85"),
    Decimal("0.90"),
    Decimal("0.95"),
    Decimal("1.00"),
    Decimal("1.05"),
    Decimal("1.10"),
    Decimal("1.15"),
    Decimal("1.20"),
    Decimal("1.25"),
    Decimal("1.30"),
)
_CATEGORY_BASE_PRICES: Final[dict[int, Decimal]] = {
    1: Decimal("12.90"),
    2: Decimal("39.90"),
    3: Decimal("59.90"),
    4: Decimal("129.90"),
    5: Decimal("69.90"),
    6: Decimal("299.90"),
    7: Decimal("19.90"),
    8: Decimal("39.90"),
    9: Decimal("39.90"),
    10: Decimal("24.90"),
    11: Decimal("799.90"),
    12: Decimal("9.90"),
    13: Decimal("14.90"),
    14: Decimal("119.90"),
    15: Decimal("149.90"),
    16: Decimal("599.90"),
    17: Decimal("249.90"),
    18: Decimal("899.90"),
    19: Decimal("24.90"),
    20: Decimal("39.90"),
    21: Decimal("19.90"),
    22: Decimal("79.90"),
    23: Decimal("149.90"),
    24: Decimal("49.90"),
    25: Decimal("39.90"),
    26: Decimal("29.90"),
}


def _money(value: Decimal) -> Decimal:
    return value.quantize(_CENT, rounding=ROUND_HALF_UP)


def _cnpj_check_digits(base: str) -> str:
    first_weights = (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 11, 2)
    second_weights = (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
    first_sum = sum(int(digit) * weight for digit, weight in zip(base, first_weights, strict=True))
    first_check = (
        0
        if first_sum % _CNPJ_MODULUS < _CNPJ_ZERO_THRESHOLD
        else _CNPJ_MODULUS - first_sum % _CNPJ_MODULUS
    )
    with_first = f"{base}{first_check}"
    second_sum = sum(
        int(digit) * weight for digit, weight in zip(with_first, second_weights, strict=True)
    )
    second_check = (
        0
        if second_sum % _CNPJ_MODULUS < _CNPJ_ZERO_THRESHOLD
        else _CNPJ_MODULUS - second_sum % _CNPJ_MODULUS
    )
    return f"{first_check}{second_check}"


def make_cnpj(base: str) -> str:
    """Gera um CNPJ fictício válido com filial 0001 a partir de uma raiz de 8 dígitos."""
    if not re.fullmatch(r"\d{8}", base):
        raise ValueError("a raiz do CNPJ deve conter exatamente 8 dígitos")
    digits = f"{base}0001"
    check_digits = _cnpj_check_digits(digits)
    return f"{base[:2]}.{base[2:5]}.{base[5:8]}/0001-{check_digits}"


def is_valid_cnpj(value: str) -> bool:
    """Informa se o CNPJ tem formato, dígitos verificadores e filial 0001 válidos."""
    if not _CNPJ_PATTERN.fullmatch(value):
        return False
    digits = value.replace(".", "").replace("/", "").replace("-", "")
    if digits == digits[0] * 14:
        return False
    return digits[-2:] == _cnpj_check_digits(digits[:12])


def _infer_unit(name: str) -> str:
    normalized = name.casefold()
    if re.search(r"\d+\s*kg\b", normalized):
        return "kg"
    if re.search(r"\d+\s*g\b", normalized):
        return "kg"
    if re.search(r"\d+\s*ml\b", normalized):
        return "L"
    if re.search(r"\d+\s*l\b", normalized):
        return "L"
    if re.search(r"\d+(?:[,.]\d+)?\s*(?:cm|m)\b", normalized):
        return "m"
    return "un"


def _base_price(category_id: int, proddoc-arch-0006-uc-v1t_index: int) -> Decimal:
    base = _CATEGORY_BASE_PRICES[category_id]
    increment = Decimal(proddoc-arch-0006-uc-v1t_index * 5 + (proddoc-arch-0006-uc-v1t_index % 3) * 2)
    return _money(base + increment)


def _expanded_supplier_names() -> tuple[str, ...]:
    prefixes = (
        "Aurora",
        "Horizonte",
        "Prisma",
        "Boreal",
        "Atlas",
        "Vertex",
        "Lumen",
        "Norte",
        "Serra",
        "Solar",
    )
    suffixes = ("Distribuidora", "Comercial", "Suprimentos", "Atacado", "Loja", "Casa")
    return tuple(
        f"{prefixes[index % len(prefixes)]} {suffixes[index % len(suffixes)]} {index + 11}"
        for index in range(50)
    )


def _expanded_supplier_categories() -> tuple[tuple[int, ...], ...]:
    """Distribui 12 fornecedores por categoria, mantendo 312 relações únicas."""
    category_sets: list[set[int]] = [set() for _ in range(61)]
    supplier_degrees = [0] * 61
    for supplier_id, (_, _, categories) in enumerate(_BASELINE_SUPPLIERS, start=1):
        for category_id in categories:
            category_sets[supplier_id].add(category_id)
            supplier_degrees[supplier_id] += 1

    for category_id in range(1, 27):
        current_count = sum(
            category_id in category_sets[supplier_id] for supplier_id in range(1, 61)
        )
        candidates = sorted(
            (
                supplier_id
                for supplier_id in range(1, 61)
                if category_id not in category_sets[supplier_id]
            ),
            key=lambda supplier_id: (
                supplier_degrees[supplier_id],
                (supplier_id * 17 + category_id * 13) % 61,
                supplier_id,
            ),
        )
        for supplier_id in candidates[: 12 - current_count]:
            category_sets[supplier_id].add(category_id)
            supplier_degrees[supplier_id] += 1

    return tuple(tuple(sorted(category_sets[supplier_id])) for supplier_id in range(1, 61))


def _supplier(
    supplier_id: int,
    name: str,
    base_cnpj: str,
    categories: tuple[int, ...],
) -> Supplier:
    return Supplier(
        id=supplier_id,
        name=normalize_text(name),
        cnpj=make_cnpj(base_cnpj),
        categories=tuple(sorted(categories)),
    )


def _offer_price(proddoc-arch-0006-uc-v1t_price: Decimal, supplier_id: int, proddoc-arch-0006-uc-v1t_id: int) -> Decimal:
    adjustment = Decimal(90 + ((supplier_id * 7 + proddoc-arch-0006-uc-v1t_id * 3) % 21))
    return _money(proddoc-arch-0006-uc-v1t_price * adjustment / Decimal("100"))


def _stock(supplier_id: int, proddoc-arch-0006-uc-v1t_id: int) -> int:
    return (supplier_id * 31 + proddoc-arch-0006-uc-v1t_id * 17) % 1000


def _build_baseline() -> SeedDataset:
    categories = CATEGORIES[:11]
    suppliers = tuple(
        _supplier(supplier_id, name, base_cnpj, categories)
        for supplier_id, (name, base_cnpj, categories) in enumerate(_BASELINE_SUPPLIERS, start=1)
    )

    proddoc-arch-0006-uc-v1ts: list[Proddoc-arch-0006-uc-v1t] = []
    proddoc-arch-0006-uc-v1t_id = 1
    for category_id, quantity in _BASELINE_PRODUCT_GROUPS:
        category = categories[category_id - 1]
        for proddoc-arch-0006-uc-v1t_index in range(quantity):
            name = category.proddoc-arch-0006-uc-v1ts[proddoc-arch-0006-uc-v1t_index]
            proddoc-arch-0006-uc-v1ts.append(
                Proddoc-arch-0006-uc-v1t(
                    id=proddoc-arch-0006-uc-v1t_id,
                    category_id=category_id,
                    name=name,
                    unit=_infer_unit(name),
                    price=_base_price(category_id, proddoc-arch-0006-uc-v1t_index),
                )
            )
            proddoc-arch-0006-uc-v1t_id += 1

    suppliers_by_category = {
        category_id: tuple(
            supplier.id for supplier in suppliers if category_id in supplier.categories
        )
        for category_id in range(1, 12)
    }
    all_supplier_ids = tuple(supplier.id for supplier in suppliers)
    offers: list[Offer] = []
    for proddoc-arch-0006-uc-v1t in proddoc-arch-0006-uc-v1ts:
        selected = list(suppliers_by_category[proddoc-arch-0006-uc-v1t.category_id][:_BASELINE_OFFERS_PER_PRODUCT])
        selected.extend(
            supplier_id
            for supplier_id in all_supplier_ids
            if supplier_id not in selected and len(selected) < _BASELINE_OFFERS_PER_PRODUCT
        )
        for supplier_id in selected:
            offers.append(
                Offer(
                    supplier_id=supplier_id,
                    proddoc-arch-0006-uc-v1t_id=proddoc-arch-0006-uc-v1t.id,
                    price=_offer_price(proddoc-arch-0006-uc-v1t.price, supplier_id, proddoc-arch-0006-uc-v1t.id),
                    stock=_stock(supplier_id, proddoc-arch-0006-uc-v1t.id),
                )
            )

    supplier_categories = tuple(
        sorted(
            (supplier.id, category_id)
            for supplier in suppliers
            for category_id in supplier.categories
        )
    )
    return SeedDataset(
        profile="baseline",
        categories=categories,
        suppliers=suppliers,
        proddoc-arch-0006-uc-v1ts=tuple(proddoc-arch-0006-uc-v1ts),
        offers=tuple(offers),
        supplier_categories=supplier_categories,
    )


def _build_expanded() -> SeedDataset:
    categories = CATEGORIES
    expanded_categories = _expanded_supplier_categories()
    suppliers: list[Supplier] = []
    for supplier_id in range(1, 61):
        if supplier_id <= len(_BASELINE_SUPPLIERS):
            name, base_cnpj, _ = _BASELINE_SUPPLIERS[supplier_id - 1]
        else:
            name = _expanded_supplier_names()[supplier_id - len(_BASELINE_SUPPLIERS) - 1]
            base_cnpj = f"{20_000_000 + (supplier_id - 10) * 1_000:08d}"
        suppliers.append(
            _supplier(
                supplier_id,
                name,
                base_cnpj,
                expanded_categories[supplier_id - 1],
            )
        )

    proddoc-arch-0006-uc-v1ts: list[Proddoc-arch-0006-uc-v1t] = []
    proddoc-arch-0006-uc-v1t_id = 1
    for category in categories:
        for proddoc-arch-0006-uc-v1t_index, base_name in enumerate(category.proddoc-arch-0006-uc-v1ts):
            for variant_index, variant in enumerate(_VARIANTS):
                price = _money(
                    _base_price(category.id, proddoc-arch-0006-uc-v1t_index) * _VARIANT_FACTORS[variant_index]
                )
                proddoc-arch-0006-uc-v1ts.append(
                    Proddoc-arch-0006-uc-v1t(
                        id=proddoc-arch-0006-uc-v1t_id,
                        category_id=category.id,
                        name=f"{category.name} - {base_name} - {variant}",
                        unit=_infer_unit(base_name),
                        price=price,
                    )
                )
                proddoc-arch-0006-uc-v1t_id += 1

    suppliers_by_category = {
        category_id: tuple(
            supplier.id for supplier in suppliers if category_id in supplier.categories
        )
        for category_id in range(1, 27)
    }
    offers: list[Offer] = []
    for proddoc-arch-0006-uc-v1t in proddoc-arch-0006-uc-v1ts:
        for supplier_id in suppliers_by_category[proddoc-arch-0006-uc-v1t.category_id]:
            offers.append(
                Offer(
                    supplier_id=supplier_id,
                    proddoc-arch-0006-uc-v1t_id=proddoc-arch-0006-uc-v1t.id,
                    price=_offer_price(proddoc-arch-0006-uc-v1t.price, supplier_id, proddoc-arch-0006-uc-v1t.id),
                    stock=_stock(supplier_id, proddoc-arch-0006-uc-v1t.id),
                )
            )

    supplier_categories = tuple(
        sorted(
            (supplier.id, category_id)
            for supplier in suppliers
            for category_id in supplier.categories
        )
    )
    return SeedDataset(
        profile="expanded",
        categories=categories,
        suppliers=tuple(suppliers),
        proddoc-arch-0006-uc-v1ts=tuple(proddoc-arch-0006-uc-v1ts),
        offers=tuple(offers),
        supplier_categories=supplier_categories,
    )


def validate_dataset(dataset: SeedDataset) -> None:  # noqa: PLR0912
    """Valida contagens, referências e unicidade do dataset gerado."""
    if dataset.counts != _EXPECTED_COUNTS[dataset.profile]:
        raise ValueError(
            f"contagens inválidas para {dataset.profile}: {dataset.counts}; "
            f"esperado {_EXPECTED_COUNTS[dataset.profile]}"
        )

    category_ids = {category.id for category in dataset.categories}
    supplier_ids = {supplier.id for supplier in dataset.suppliers}
    proddoc-arch-0006-uc-v1t_ids = {proddoc-arch-0006-uc-v1t.id for proddoc-arch-0006-uc-v1t in dataset.proddoc-arch-0006-uc-v1ts}
    if len(category_ids) != len(dataset.categories):
        raise ValueError("IDs de categoria duplicados")
    if len(supplier_ids) != len(dataset.suppliers):
        raise ValueError("IDs de fornecedor duplicados")
    if len(proddoc-arch-0006-uc-v1t_ids) != len(dataset.proddoc-arch-0006-uc-v1ts):
        raise ValueError("IDs de produto duplicados")

    category_names = [category.name.casefold() for category in dataset.categories]
    supplier_names = [supplier.name.casefold() for supplier in dataset.suppliers]
    proddoc-arch-0006-uc-v1t_names = [proddoc-arch-0006-uc-v1t.name.casefold() for proddoc-arch-0006-uc-v1t in dataset.proddoc-arch-0006-uc-v1ts]
    if len(category_names) != len(set(category_names)):
        raise ValueError("nomes de categoria duplicados")
    if len(supplier_names) != len(set(supplier_names)):
        raise ValueError("nomes de fornecedor duplicados")
    if len(proddoc-arch-0006-uc-v1t_names) != len(set(proddoc-arch-0006-uc-v1t_names)):
        raise ValueError("nomes de produto duplicados")

    if len({supplier.cnpj for supplier in dataset.suppliers}) != len(dataset.suppliers):
        raise ValueError("CNPJs duplicados")
    if not all(is_valid_cnpj(supplier.cnpj) for supplier in dataset.suppliers):
        raise ValueError("CNPJ inválido")

    for proddoc-arch-0006-uc-v1t in dataset.proddoc-arch-0006-uc-v1ts:
        if proddoc-arch-0006-uc-v1t.category_id not in category_ids:
            raise ValueError(f"produto {proddoc-arch-0006-uc-v1t.id} referencia categoria inexistente")
        if not _UNIT_PATTERN.fullmatch(proddoc-arch-0006-uc-v1t.unit):
            raise ValueError(f"unidade inválida no produto {proddoc-arch-0006-uc-v1t.id}: {proddoc-arch-0006-uc-v1t.unit}")
        if proddoc-arch-0006-uc-v1t.price < 0 or proddoc-arch-0006-uc-v1t.price.as_tuple().exponent != _PRICE_EXPONENT:
            raise ValueError(f"preço inválido no produto {proddoc-arch-0006-uc-v1t.id}: {proddoc-arch-0006-uc-v1t.price}")

    relation_keys = set()
    for supplier_id, category_id in dataset.supplier_categories:
        if supplier_id not in supplier_ids or category_id not in category_ids:
            raise ValueError(f"relação inválida: {supplier_id}, {category_id}")
        key = (supplier_id, category_id)
        if key in relation_keys:
            raise ValueError(f"relação duplicada: {key}")
        relation_keys.add(key)

    offer_keys = set()
    for offer in dataset.offers:
        if offer.supplier_id not in supplier_ids or offer.proddoc-arch-0006-uc-v1t_id not in proddoc-arch-0006-uc-v1t_ids:
            raise ValueError(f"oferta inválida: {offer}")
        key = (offer.supplier_id, offer.proddoc-arch-0006-uc-v1t_id)
        if key in offer_keys:
            raise ValueError(f"oferta duplicada: {key}")
        offer_keys.add(key)
        if offer.price < 0 or offer.price.as_tuple().exponent != _PRICE_EXPONENT:
            raise ValueError(f"preço inválido na oferta {key}: {offer.price}")
        if not 0 <= offer.stock <= _MAX_STOCK:
            raise ValueError(f"estoque inválido na oferta {key}: {offer.stock}")


def build_dataset(profile: Profile) -> SeedDataset:
    """Constrói e valida o dataset determinístico do perfil solicitado."""
    if profile == "baseline":
        dataset = _build_baseline()
    elif profile == "expanded":
        dataset = _build_expanded()
    else:
        raise ValueError(f"perfil inválido: {profile}")
    validate_dataset(dataset)
    return dataset
