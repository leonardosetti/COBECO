# COBECO Backend — Catálogo Router (FastAPI)
# Endpoints: Categorias, Fornecedores, Produtos (Autocomplete)


from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.adapters.db.database import get_db
from src.adapters.db.models import (
    CategoriaModel,
    FornecedorCategoriaModel,
    FornecedorModel,
    FornecedorProdutoModel,
    ProdutoModel,
)
from src.domain.repositories import (
    CategoriaRepository,
    FornecedorRepository,
    ProdutoRepository,
)

router = APIRouter(tags=["Catálogo"])


# ============================================================
# Schemas
# ============================================================
class CategoriaResponse(BaseModel):
    id: int
    nome: str
    descricao: str | None = None

    class Config:
        from_attributes = True


class FornecedorResponse(BaseModel):
    id: int
    nome: str
    cnpj: str
    categorias: list[CategoriaResponse] = []

    class Config:
        from_attributes = True


class ProdutoResponse(BaseModel):
    id: int
    nome: str
    marca: str | None = None
    unidade: str

    class Config:
        from_attributes = True


class FornecedorDisponibilidadeResponse(BaseModel):
    fornecedor: FornecedorResponse
    percentual_disponibilidade: float
    itens_disponiveis: int
    itens_totais: int


# Gatilhos de busca semântica para categorias (RF20).
# Mapeia NOME DA CATEGORIA (lowercase) -> lista de termos/sinônimos que disparam essa categoria.
# Baseado nas 25 categorias do seed realístico (banco stage/dev) + chaves genéricas.
CATEGORIA_GATILHOS: dict[str, list[str]] = {
    # ===== SUPERMERCADO (8 categorias) =====
    "mercearia": ["arroz", "feijão", "açúcar", "óleo", "massa", "supermercado", "mercearia", "alimento", "mantimento", "comida", "cereal", "grão", "farinha", "molho", "tempero", "conserva", "enlatado"],
    "bebidas": ["refrigerante", "suco", "cerveja", "água", "bebida", "drink", "líquido", "refri", "isotônico", "energético", "chá", "café", "leite", "iogurte bebível", "vinho", "espumante", "cachaça", "whisky"],
    "limpeza": ["detergente", "sabão", "desinfetante", "limpeza", "lavar", "multiuso", "álcool", "sanitária", "água sanitária", "cloro", "limpa vidros", "lustra móveis", "cera", "removedor", "esponja", "vassoura", "rodo", "balde"],
    "higiene": ["sabonete", "shampoo", "papel higiênico", "higiene", "pessoal", "banho", "creme dental", "escova", "fio dental", "enxaguante", "desodorante", "perfume", "cosmético", "beleza", "condicionador", "absorvente", "fralda", "cotonete"],
    "padaria": ["pão", "biscoito", "bolo", "bolacha", "torrada", "rosca", "pão de queijo", "croissant", "pão francês", "pão de forma", "bisnaguinha", "sonho", "quentão", "broa", "pão doce", "pão integral"],
    "frios e laticínios": ["queijo", "presunto", "iogurte", "leite", "manteiga", "requeijão", "ricota", "margarina", "mortadela", "salame", "peito de peru", "blanquet", "cream cheese", "creme de leite", "leite condensado"],
    "açougue": ["carne", "frango", "linguiça", "picanha", "costela", "filé", "alcatra", "contra-filé", "carne moída", "bife", "bisteca", "bacon", "couve", "miúdo", "fígado", "coração", "moela"],
    "hortifruti": ["maçã", "banana", "batata", "cebola", "laranja", "tomate", "alface", "cenoura", "fruta", "legume", "verdura", "hortifruti", "uva", "manga", "abacaxi", "melancia", "morango", "limão", "alho", "pimentão", "pepino", "abobrinha", "berinjela", "couve-flor", "brócolis", "espinafre", "repolho"],
    
    # ===== INFORMÁTICA E ELETRÔNICOS (4 categorias) =====
    "eletrônicos": ["celular", "tablet", "eletrônico", "smartphone", "fone", "carregador", "gadget", "tech", "dispositivo", "aparelho", "smart", "smartwatch", "fone bluetooth", "caixa de som", "headset", "webcam", "drone", "câmera", "action cam"],
    "informática": ["computador", "notebook", "periférico", "impressora", "processador", "placa de vídeo", "mouse", "teclado", "monitor", "pc", "ti", "tecnologia", "software", "hardware", "rede", "servidor", "hd", "ssd", "memória ram", "placa mãe", "gabinete", "fonte", "cooler", "mousepad", "hub usb", "cabo hdmi", "adaptador"],
    "eletrodomésticos": ["geladeira", "fogão", "máquina de lavar", "micro-ondas", "eletrodoméstico", "lava-louças", "forno", "freezer", "cooktop", "coifa", "purificador", "ar condicionado", "aquecedor", "ventilador", "liquidificador", "batedeira", "processador alimentos", "aspirador", "ferro de passar", "cafeteira", "torneadeira", "panela elétrica", "air fryer"],
    "móveis": ["sofá", "cadeira", "mesa", "armário", "cama", "móvel", "estofado", "mobília", "rack", "guarda-roupa", "colchão", "estante", "escrivaninha", "poltrona", "puff", "banqueta", "cômoda", "cabeceira", "criado-mudo", "buffet", "aparador", "sapateira", "nichos", "prateleira"],
    
    # ===== LIVROS E PAPELARIA (2 categorias) =====
    "livros": ["livro", "revista", "leitura", "didático", "literatura", "romance", "mangá", "hq", "ebook", "autor", "biblioteca", "livraria", "texto", "manual", "guia", "dicionário", "enciclopédia", "infantil", "juvenil", "técnico", "biografia", "autoajuda", "suspense", "fantasia", "ficção", "não-ficção", "clássico", "best-seller", "lançamento"],
    "papelaria": ["caderno", "caneta", "papelaria", "escritório", "papel", "lápis", "material escolar", "escola", "escrita", "desenho", "arte", "artesanal", "borracha", "apontador", "régua", "tesoura", "cola", "fita adesiva", "grampeador", "clips", "pastas", "arquivo", "agenda", "planner", "marcador", "textmarker", "lapiseira", "grafite"],
    
    # ===== CONSTRUÇÃO E FERRAGENS (4 categorias) =====
    "ferramentas": ["martelo", "serrote", "chave de fenda", "alicate", "furadeira", "ferramenta", "chave inglesa", "trena", "nível", "parafusadeira", "chave allen", "torquímetro", "multímetro", "lixadeira", "esmerilhadeira", "serra circular", "plain", "formão", "marreta", "picareta", "enxada", "pá", "pá de obra", "rastelo", "carrinho de mão", "betoneira", "compactador", "gerador", "compressor", "serra tico-tico", "politriz", "pistola de pintura"],
    "materiais construção": ["cimento", "tijolo", "tinta", "cano", "construção", "obra", "material", "reformar", "areia", "brita", "telha", "bloco", "argamassa", "reboco", "ferro", "aço", "vergalhão", "laje", "piso", "azulejo", "porcelanato", "drywall", "gesso", "forro pvc", "manta asfáltica", "impermeabilizante", "selante", "silicone", "massa corrida", "lixa", "pincel", "rolo de pintura", "bandeja"],
    "jardinagem": ["pá", "rastelo", "jardim", "planta", "vaso", "adubo", "jardinagem", "flor", "grama", "semente", "terra", "regador", "podador", "tesoura poda", "mangueira", "aspirador folhas", "cortador grama", "trator", "enxada", "cultivador", "adubo orgânico", "substrato", "argila expandida", "pedra decorativa", "cascata", "fonte", "iluminação jardim", "cerca viva", "treliça"],
    "iluminação": ["lâmpada", "lustre", "refletor", "iluminação", "led", "luminária", "spot", "trilho", "abajur", "pendente", "plafon", "embutir", "externo", "interno", "dimerizável", "rgb", "fita led", "painel led", "lâmpada inteligente", "sensor presença", "fotocélula", "poste", "balizador", "arandela", "projetor", "emergência"],
    
    # ===== PET (2 categorias) =====
    "pet alimentos": ["ração", "cachorro", "gato", "pet", "petisco", "animal", "bicho", "veterinário", "banho", "tosa", "pet shop", "ração premium", "ração natural", "sachê", "lata", "bifinho", "osso", "catnip", "leite pet", "vitamina", "suplemento"],
    "pet acessórios": ["coleira", "guia", "cama", "brinquedo", "comedouro", "bebedouro", "casinha", "roupinha", "tapete higiênico", "areia sanitária", "portão", "grade", "transportadora", "cinto segurança", "identificação", "medalha", "shampoo pet", "condicionador pet", "escova", "corta unha", "tesoura", "toalha", "fraldas pet"],
    
    # ===== AUTOMOTIVO (2 categorias) =====
    "peças automotivas": ["filtro", "óleo", "vela", "pastilha", "automotivo", "carro", "moto", "veículo", "peça", "mecânica", "oficina", "revisão", "troca óleo", "correia", "tensor", "bomba água", "radiador", "alternador", "motor partida", "bateria", "cabo vela", "bobina", "sensor", "atalho", "amortecedor", "mola", "bandeja", "pivô", "terminal", "barra direção", "caixa direção", "bomba direção", "embreagem", "platô", "disco", "rolamento", "retentor", "junta", "vedação", "anilha", "parafuso", "porca", "arruela", "chave roda", "macaco", "triângulo", "coxim", "bucha", "pino", "eixo", "diferencial", "câmbio", "embreagem", "volante motor", "atuador", "cilindro mestre", "cilindro roda", "mangueira freio", "fluido freio", "abs", "sensor abs", "vela ignição", "cabo vela", "bobina ignição", "distribuidor", "rotor", "tampa distribuidor", "platinado", "condensador", "capacitor"],
    "pneus e rodas": ["pneu", "roda", "calibragem", "balanceamento", "alinhamento", "aro", "pneus", "rodas", "borracha", "câmara", "válvula", "rodízio", "pneu radial", "pneu diagonal", "pneu runflat", "pneu verde", "pneu remold", "recapado", "estepe", "triângulo", "chave roda", "macaco", "compressor portátil", "selante", "reparo pneu", "capa roda", "calota", "porca roda", "parafuso roda", "centro roda", "anela", "câmara ar", "válvula pneu", "bico", "tampa válvula", "extensor válvula"],
    
    # ===== MODA (3 categorias) =====
    "vestuário masculino": ["camisa", "calça", "bermuda", "camiseta", "blusão", "jaqueta", "cinto", "meia", "cueca", "sungas", "traje", "terno", "gravata", "palito", "colete", "suéter", "cardigan", "moletom", "blusa frio", "jaqueta couro", "casaco", "trench coat", "parka", "puffer", "colete puffer", "camisa polo", "camisa social", "camisa flanela", "camisa jeans", "calça jeans", "calça sarja", "calça social", "calça moletom", "calça tactel", "bermuda jeans", "bermuda sarja", "bermuda tactel", "bermuda moletom", "cueca boxer", "cueca slip", "cueca samba canção", "meia cano alto", "meia cano curto", "meia invisível", "meia esportiva", "meia social"],
    "vestuário feminino": ["blusa", "vestido", "saia", "shorts", "camiseta", "regata", "calça legging", "jaqueta", "cardigan", "kimono", "quemono", "blazer", "trench coat", "casaco", "poncho", "xale", "lenço", "echarpe", "cachecol", "gorro", "luva", "meia calça", "meia 7/8", "meia soquete", "lingerie", "sutiã", "calcinha", "body", "maiô", "biquíni", "saída praia", "vestido longo", "vestido curto", "vestido midi", "saia longa", "saia midi", "saia curta", "shorts jeans", "shorts sarja", "shorts moletom", "calça jeans", "calça leggging", "calça pantalona", "calça jogger", "calça mom", "calça skinny", "calça wide leg", "blusa cropped", "blusa ombro a ombro", "blusa manga longa", "blusa manga curta", "blusa alcinha", "blusa decote v", "blusa decote u", "blusa gola alta", "blusa canoa"],
    "calçados": ["tênis", "sapato", "sandália", "bota", "chinelo", "rasteira", "salto", "coturno", "sneaker", "esporte", "corrida", "caminhada", "futebol", "mocassim", "scarpin", "peep toe", "ankle boot", "over the knee", "bota cano curto", "bota cano longo", "bota cano médio", "bota country", "bota chelsea", "bota tratorada", "tênis running", "tênis training", "tênis lifestyle", "tênis basquete", "tênis skate", "tênis casual", "sapato social", "sapato oxford", "sapato derby", "sapato loafer", "sapato monk strap", "sandália rasteira", "sandália salto", "sandália plataforma", "sandália gladiadora", "sandália papete", "chinelo slide", "chinelo dedo", "chinelo nuvem", "crocs", "birkenstock", "havaianas", "ipanema", "rider"],
    
    # ===== CHAVES GENÉRICAS (busca ampla por prefixo/semelhança) =====
    "construção": ["cimento", "tijolo", "tinta", "cano", "construção", "obra", "material", "reformar", "pedreiro", "mestre de obras", "engenharia", "arquitetura"],
    "jardim": ["pá", "rastelo", "jardim", "planta", "vaso", "adubo", "jardinagem", "flor", "grama", "horta", "paisagismo", "jardineiro"],
    "ferramenta": ["martelo", "serrote", "chave", "alicate", "furadeira", "ferramenta", "reparo", "consertar", "manutenção", "oficina"],
    "informática": ["computador", "notebook", "periférico", "impressora", "processador", "pc", "ti", "tecnologia", "sistema", "programa", "código", "desenvolvedor"],
    "eletrônico": ["celular", "tablet", "eletrônico", "smartphone", "fone", "carregador", "gadget", "tech", "dispositivo", "aparelho", "smart"],
    "eletro": ["geladeira", "fogão", "máquina", "micro-ondas", "eletrodoméstico", "eletro", "doméstico", "cozinha", "lavanderia", "eletroportátil"],
    "móvel": ["sofá", "cadeira", "mesa", "armário", "cama", "móvel", "estofado", "mobília", "decorar", "mobiliário", "decoracao"],
    "livro": ["livro", "revista", "leitura", "didático", "literatura", "romance", "autor", "biblioteca", "escrita", "autor", "publicação"],
    "papelaria": ["caderno", "caneta", "papelaria", "escritório", "papel", "lápis", "material escolar", "escola", "escrita", "desenho", "arte", "artesanal"],
    "pet": ["ração", "cachorro", "gato", "pet", "petisco", "animal", "bicho", "veterinário", "banho", "tosa", "pet shop"],
    "auto": ["filtro", "óleo", "vela", "pastilha", "automotivo", "carro", "moto", "veículo", "peça", "mecânica", "oficina", "revisão", "troca óleo"],
    "pneu": ["pneu", "roda", "calibragem", "balanceamento", "alinhamento", "aro", "pneus", "rodas", "borracha", "câmara", "válvula", "rodízio"],
    "moda": ["camisa", "calça", "vestido", "saia", "blusa", "moda", "roupa", "vestir", "estilo", "tendência", "fashion", "look", "outfit", "vestuário"],
    "calçado": ["tênis", "sapato", "sandália", "calçado", "bota", "chinelo", "rasteira", "salto", "coturno", "sneaker", "esporte", "corrida", "caminhada", "futebol"],
    "higiene": ["sabonete", "shampoo", "papel higiênico", "higiene", "pessoal", "banho", "creme dental", "escova", "fio dental", "enxaguante", "desodorante", "perfume", "cosmético", "beleza"],
    "limpeza": ["detergente", "sabão", "desinfetante", "limpeza", "lavar", "multiuso", "álcool", "sanitária", "água sanitária", "cloro", "limpa vidros", "lustra móveis", "cera", "removedor"],
    "bebida": ["refrigerante", "suco", "cerveja", "água", "bebida", "drink", "líquido", "refri", "isotônico", "energético", "chá", "café", "leite", "iogurte bebível"],
    "iluminação": ["lâmpada", "lustre", "refletor", "iluminação", "led", "luminária", "spot", "trilho", "abajur", "pendente", "plafon", "embutir", "externo", "interno", "dimerizável", "rgb"],
    "supermercado": ["arroz", "feijão", "açúcar", "óleo", "massa", "supermercado", "mercearia", "alimento", "mantimento", "comida", "cereal", "grão"],
    "vestuário": ["roupas", "camiseta", "camisa", "calça", "calçado", "sapato", "moda", "roupa", "vestir", "traje", "blusa", "vestido", "saia", "bermuda", "moletom", "jaqueta", "jeans", "social", "polo"],
    "automotivos": ["carro", "moto", "veículo", "automotivo", "peça", "filtro", "óleo", "vela", "pastilha", "freio", "amortecedor", "bateria", "correia", "pneu", "roda", "calibragem", "balanceamento", "aro"],
    "decoração": ["quadro", "tapete", "vaso", "luminaire", "enfeite", "decoração", "decorar", "adorno", "ornamento", "arte", "espelho", "cortina", "almofada", "vela", "aroma"],
}

# Mapeamento de grandes áreas para categorias macro (RF27/RF28).
# Nomes batem EXATAMENTE com as 25 categorias do seed realístico (banco stage/dev).
# Expandido à medida que o catálogo cresce; migrar para coluna/tabela no DB quando houver >20 áreas.
AREAS_GRANDES: dict[str, list[str]] = {
    "Supermercado": [
        "Mercearia", "Bebidas", "Limpeza", "Higiene",
        "Padaria", "Frios e Laticínios", "Açougue", "Hortifruti"
    ],
    "Informática e Eletrônicos": [
        "Eletrônicos", "Informática", "Eletrodomésticos", "Móveis"
    ],
    "Livros e Papelaria": [
        "Livros", "Papelaria"
    ],
    "Construção e Ferragens": [
        "Ferramentas", "Materiais Construção", "Jardinagem", "Iluminação"
    ],
    "Pet": [
        "Pet Alimentos", "Pet Acessórios"
    ],
    "Automotivo": [
        "Peças Automotivas", "Pneus e Rodas"
    ],
    "Moda": [
        "Vestuário Masculino", "Vestuário Feminino", "Calçados"
    ],
}


class AreaGrandeResponse(BaseModel):
    id: int
    nome: str
    categorias: list[CategoriaResponse] = []

    class Config:
        from_attributes = True


class CategoriaBuscaResponse(BaseModel):
    id: int
    nome: str
    descricao: str | None = None
    match_por: str = "nome"  # "nome" | "sinonimo"

    class Config:
        from_attributes = True


# ============================================================
# Repository Implementations
# ============================================================
class CategoriaRepositoryImpl(CategoriaRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def listar_todas(self):
        result = await self.session.execute(select(CategoriaModel).order_by(CategoriaModel.nome))
        return list(result.scalars().all())

    async def buscar_por_id(self, categoria_id: int):
        result = await self.session.execute(
            select(CategoriaModel).where(CategoriaModel.id == categoria_id)
        )
        return result.scalar_one_or_none()

    async def buscar_por_ids(self, ids: list[int]):
        result = await self.session.execute(
            select(CategoriaModel).where(CategoriaModel.id.in_(ids))
        )
        return list(result.scalars().all())

    async def buscar_por_termo(self, termo: str):
        """Busca semântica de categorias por nome ou sinônimos (RF20).
        
        Match priority:
        1. Nome da categoria contém o termo (ex: "vestuário" em "Vestuário Masculino")
        2. Termo está nos gatilhos da categoria (ex: "roupas" -> "vestuário masculino")
        3. Chave genérica de CATEGORIA_GATILHOS contém o termo (ex: "roupas" -> chave "vestuário")
        """
        from sqlalchemy import select

        t = (termo or "").strip().lower()
        if not t:
            return []

        categorias_por_nome: dict[int, CategoriaModel] = {}
        categorias_por_sinonimo: dict[int, CategoriaModel] = {}

        # 1. Match direto no nome da categoria (substring)
        todas = await self.session.execute(select(CategoriaModel).order_by(CategoriaModel.nome))
        for cat in todas.scalars().all():
            nome = (cat.nome or "").lower()
            if t in nome or nome in t:
                categorias_por_nome[cat.id] = cat
                continue
            
            # 2. Match nos gatilhos específicos da categoria (nome exato da categoria)
            gatilhos = CATEGORIA_GATILHOS.get(nome, [])
            if t in gatilhos or any(g.startswith(t) or t.startswith(g) for g in gatilhos if g):
                categorias_por_sinonimo[cat.id] = cat
                continue
            
            # 3. Match em chaves genéricas de CATEGORIA_GATILHOS (para busca ampla)
            # Ex: buscar "roupas" encontra chave "vestuário" que tem "roupas" nos gatilhos
            for chave, gatilhos_gen in CATEGORIA_GATILHOS.items():
                if chave in nome or nome in chave:  # ex: "vestuário" in "vestuário masculino"
                    if t in gatilhos_gen or any(g.startswith(t) or t.startswith(g) for g in gatilhos_gen if g):
                        categorias_por_sinonimo[cat.id] = cat
                        break

        mescladas = {**categorias_por_sinonimo, **categorias_por_nome}
        return list(mescladas.values())


class FornecedorRepositoryImpl(FornecedorRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def listar_ativos(self):
        result = await self.session.execute(
            select(FornecedorModel).where(FornecedorModel.ativo).order_by(FornecedorModel.nome)
        )
        return list(result.scalars().all())

    async def listar_por_categorias(self, categoria_ids: list[int]):
        # Fornecedores que têm TODAS as categorias selecionadas (interseção)
        # Ou PELO MENOS UMA (união) - conforme RF12/UC03
        # Usando união (pelo menos uma categoria)
        from sqlalchemy import select

        subquery = (
            select(FornecedorCategoriaModel.fornecedor_id)
            .where(FornecedorCategoriaModel.categoria_id.in_(categoria_ids))
            .group_by(FornecedorCategoriaModel.fornecedor_id)
        )

        result = await self.session.execute(
            select(FornecedorModel)
            .where(
                FornecedorModel.id.in_(subquery),
                FornecedorModel.ativo,
            )
            .order_by(FornecedorModel.nome)
        )
        return list(result.scalars().all())

    async def buscar_por_id(self, fornecedor_id: int):
        result = await self.session.execute(
            select(FornecedorModel)
            .options(selectinload(FornecedorModel.categorias))
            .where(FornecedorModel.id == fornecedor_id)
        )
        return result.scalar_one_or_none()

    async def buscar_por_ids(self, ids: list[int]):
        result = await self.session.execute(
            select(FornecedorModel).where(FornecedorModel.id.in_(ids))
        )
        return list(result.scalars().all())

    async def calcular_disponibilidade(
        self,
        fornecedor_id: int,
        produto_ids: list[int],
    ):
        from src.adapters.db.models import FornecedorProdutoModel

        result = await self.session.execute(
            select(FornecedorProdutoModel).where(
                FornecedorProdutoModel.fornecedor_id == fornecedor_id,
                FornecedorProdutoModel.produto_id.in_(produto_ids),
                FornecedorProdutoModel.ativo,
                FornecedorProdutoModel.estoque > 0,
            )
        )
        produtos_encontrados = list(result.scalars().all())

        itens_disponiveis = len(produtos_encontrados)
        itens_ausentes = len(produto_ids) - itens_disponiveis
        preco_total = sum(p.preco * p.estoque for p in produtos_encontrados)

        return itens_disponiveis, itens_ausentes, preco_total


class ProdutoRepositoryImpl(ProdutoRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def buscar_por_id(self, produto_id: int):
        result = await self.session.execute(
            select(ProdutoModel).where(ProdutoModel.id == produto_id, ProdutoModel.ativo)
        )
        return result.scalar_one_or_none()

    async def buscar_por_ids(self, ids: list[int]):
        result = await self.session.execute(
            select(ProdutoModel).where(ProdutoModel.id.in_(ids), ProdutoModel.ativo)
        )
        return list(result.scalars().all())

    async def autocomplete(self, query: str, limit: int = 10, categoria_ids: list[int] | None = None):
        """Busca híbrida Full-Text Search: FULLTEXT (nome) + marca (FULLTEXT) + expansão semântica via produto_classes (FULLTEXT).

        Retorna resultados ordenados por relevância (score do MATCH/AGAINST, BOOLEAN MODE).
        Todas as buscas usam índices FULLTEXT do MySQL — nenhuma busca por LIKE.
        Se categoria_ids fornecido, filtra produtos apenas dessas categorias.
        """
        from sqlalchemy import text

        q = query.strip()
        if not q:
            return []

        # Sanitiza termo para BOOLEAN MODE (escapa caracteres especiais)
        q_sanitized = "".join(ch for ch in q if ch.isalnum() or ch.isspace()).strip()
        if not q_sanitized:
            return []

        # Cláusula WHERE adicional para filtro de categoria
        cat_where = ""
        cat_params = {}
        if categoria_ids:
            cat_where = " AND categoria_id IN :categoria_ids"
            cat_params = {"categoria_ids": tuple(categoria_ids)}

        # 1. FULLTEXT search no nome (MySQL MATCH AGAINST) — ordenado por relevância
        fulltext_sql = text(f"""
            SELECT id, nome, marca, unidade, ativo, criado_em,
                   MATCH(nome) AGAINST(:query IN BOOLEAN MODE) AS relevancia
            FROM produtos
            WHERE ativo = TRUE
              AND MATCH(nome) AGAINST(:query IN BOOLEAN MODE)
              {cat_where}
            ORDER BY relevancia DESC
            LIMIT :limit
        """)
        params = {"query": f"+{q_sanitized}*", "limit": limit, **cat_params}
        result = await self.session.execute(fulltext_sql, params)
        rows = result.mappings().all()
        produtos = [ProdutoModel(**{k: v for k, v in dict(r).items() if k != "relevancia"}) for r in rows]
        for p, r in zip(produtos, rows):
            p.relevancia = float(r["relevancia"])

        if len(produtos) >= limit:
            return produtos[:limit]

        # 2. FULLTEXT search em marca (MySQL MATCH AGAINST)
        remaining = limit - len(produtos)
        marca_ids = {p.id for p in produtos}
        marca_sql = text(f"""
            SELECT id, nome, marca, unidade, ativo, criado_em,
                   MATCH(marca) AGAINST(:query IN BOOLEAN MODE) AS relevancia
            FROM produtos
            WHERE ativo = TRUE
              AND id NOT IN :excluded_ids
              AND MATCH(marca) AGAINST(:query IN BOOLEAN MODE)
              {cat_where}
            ORDER BY relevancia DESC
            LIMIT :limit
        """)
        excluded = tuple(marca_ids) if marca_ids else (0,)
        params = {"excluded_ids": excluded, "query": f"+{q_sanitized}*", "limit": remaining, **cat_params}
        result = await self.session.execute(marca_sql, params)
        rows = result.mappings().all()
        produtos.extend(ProdutoModel(**{k: v for k, v in dict(r).items() if k != "relevancia"}) for r in rows)
        for p, r in zip(produtos[len(produtos) - len(rows):], rows):
            p.relevancia = float(r["relevancia"])

        if len(produtos) >= limit:
            return produtos[:limit]

        # 3. Expansão semântica via produto_classes (FULLTEXT nas colunas geradas)
        remaining = limit - len(produtos)
        if remaining > 0:
            classe_sql = text("""
                SELECT termos_busca, marcas_referencia
                FROM produto_classes
                WHERE ativo = TRUE
                  AND (
                    MATCH(termos_busca_texto) AGAINST(:query IN BOOLEAN MODE)
                    OR MATCH(marcas_referencia_texto) AGAINST(:query IN BOOLEAN MODE)
                  )
            """)
            result = await self.session.execute(classe_sql, {"query": f"+{q_sanitized}*"})
            classe_rows = result.mappings().all()

            import json

            related_terms = set()
            related_brands = set()
            for row in classe_rows:
                related_terms.update(json.loads(row["termos_busca"]))
                related_brands.update(json.loads(row["marcas_referencia"]))

            if related_brands:
                brand_ids = {p.id for p in produtos}
                brand_placeholders = ", ".join([f":brand{i}" for i in range(len(related_brands))])
                marca_sql = text(f"""
                    SELECT id, nome, marca, unidade, ativo, criado_em
                    FROM produtos
                    WHERE ativo = TRUE
                      AND id NOT IN :excluded_ids
                      AND (marca IN ({brand_placeholders}))
                      {cat_where}
                    LIMIT :limit
                """)
                params = {
                    "excluded_ids": tuple(brand_ids) if brand_ids else (0,),
                    "limit": remaining,
                    **cat_params
                }
                for i, brand in enumerate(related_brands):
                    params[f"brand{i}"] = brand
                result = await self.session.execute(marca_sql, params)
                rows = result.mappings().all()
                produtos.extend(ProdutoModel(**dict(r)) for r in rows)

            if len(produtos) < limit and related_terms:
                remaining = limit - len(produtos)
                term_ids = {p.id for p in produtos}
                simple_terms = [
                    t for t in related_terms if t.replace(" ", "").isalnum() and len(t) >= 2
                ]
                if simple_terms:
                    ft_query = " ".join(f"+{t}*" for t in simple_terms[:5])
                    ft_sql = text(f"""
                        SELECT id, nome, marca, unidade, ativo, criado_em,
                               MATCH(nome) AGAINST(:query IN BOOLEAN MODE) AS relevancia
                        FROM produtos
                        WHERE ativo = TRUE
                          AND id NOT IN :excluded_ids
                          AND MATCH(nome) AGAINST(:query IN BOOLEAN MODE)
                          {cat_where}
                        ORDER BY relevancia DESC
                        LIMIT :limit
                    """)
                    excluded = tuple(term_ids) if term_ids else (0,)
                    result = await self.session.execute(
                        ft_sql, {"excluded_ids": excluded, "query": ft_query, "limit": remaining, **cat_params}
                    )
                    rows = result.mappings().all()
                    novos = [ProdutoModel(**{k: v for k, v in dict(r).items() if k != "relevancia"}) for r in rows]
                    for p, r in zip(novos, rows):
                        p.relevancia = float(r["relevancia"])
                    produtos.extend(novos)

        return produtos[:limit]

    async def listar_ativos(self):
        result = await self.session.execute(
            select(ProdutoModel).where(ProdutoModel.ativo).order_by(ProdutoModel.nome)
        )
        return list(result.scalars().all())

    async def count_ativos(self) -> int:
        from sqlalchemy import func

        result = await self.session.execute(
            select(func.count()).select_from(ProdutoModel).where(ProdutoModel.ativo)
        )
        return int(result.scalar_one())

    async def listar_por_categorias(self, categoria_ids: list[int]):
        """Produtos das categorias selecionadas (RF19).
        
        Filtra produtos pela sua categoria principal (produtos.categoria_id)
        e garante que estejam disponíveis em pelo menos um fornecedor ativo.
        """
        if not categoria_ids:
            return []
        
        # Subquery: fornecedores ativos com estoque > 0
        sub_fornecedores = (
            select(FornecedorProdutoModel.fornecedor_id)
            .distinct()
            .where(
                FornecedorProdutoModel.ativo == True,
                FornecedorProdutoModel.estoque > 0,
            )
        )
        
        result = await self.session.execute(
            select(ProdutoModel)
            .where(
                ProdutoModel.ativo == True,
                ProdutoModel.categoria_id.in_(categoria_ids),
                # Garante que existe pelo menos um fornecedor ativo com estoque
                ProdutoModel.id.in_(
                    select(FornecedorProdutoModel.produto_id)
                    .where(
                        FornecedorProdutoModel.fornecedor_id.in_(sub_fornecedores),
                        FornecedorProdutoModel.ativo == True,
                        FornecedorProdutoModel.estoque > 0,
                    )
                )
            )
            .order_by(ProdutoModel.nome)
        )
        return list(result.scalars().all())


def get_categoria_repo(session: AsyncSession = Depends(get_db)) -> CategoriaRepository:
    return CategoriaRepositoryImpl(session)


def get_fornecedor_repo(
    session: AsyncSession = Depends(get_db),
) -> FornecedorRepository:
    return FornecedorRepositoryImpl(session)


def get_produto_repo(session: AsyncSession = Depends(get_db)) -> ProdutoRepository:
    return ProdutoRepositoryImpl(session)


# ============================================================
# Endpoints
# ============================================================
@router.get(
    "/categorias",
    response_model=list[CategoriaResponse],
    summary="UC03/RF12 - Listar Categorias (Pré-filtro)",
)
async def listar_categorias(
    areas: str | None = Query(
        None, description="IDs de grandes áreas separados por vírgula (filtro multi-seleção, RF27)"
    ),
    repo: CategoriaRepository = Depends(get_categoria_repo),
):
    categorias = await repo.listar_todas()
    if areas:
        try:
            area_ids = [int(a) for a in areas.split(",") if a.strip()]
            nomes_area = list(AREAS_GRANDES.keys())
            nomes_categorias_permitidas: set[str] = set()
            for aid in area_ids:
                if 1 <= aid <= len(nomes_area):
                    nomes_categorias_permitidas.update(AREAS_GRANDES[nomes_area[aid - 1]])
            if nomes_categorias_permitidas:
                categorias = [c for c in categorias if (c.nome or "").strip() in nomes_categorias_permitidas]
            else:
                categorias = []
        except ValueError:
            pass
    return [CategoriaResponse.model_validate(c) for c in categorias]


@router.get(
    "/categorias/busca",
    response_model=list[CategoriaBuscaResponse],
    summary="RF20 - Busca semântica de categorias (nome + sinônimos)",
)
async def buscar_categorias(
    q: str = Query(..., min_length=1, description="Termo de busca semântica (ex.: roupas, pá, rastelo)"),
    repo: CategoriaRepository = Depends(get_categoria_repo),
):
    categorias = await repo.buscar_por_termo(q)
    resultados = []
    t = (q or "").strip().lower()
    for c in categorias:
        nome = (c.nome or "").lower()
        match_por = "nome" if (t in nome or nome in t) else "sinonimo"
        resultados.append(
            CategoriaBuscaResponse(
                id=c.id,
                nome=c.nome,
                descricao=c.descricao,
                match_por=match_por,
            )
        )
    return resultados


@router.get(
    "/areas-grandes",
    response_model=list[AreaGrandeResponse],
    summary="RF28 - Listar grandes áreas com suas categorias macro",
)
async def listar_areas_grandes(
    repo: CategoriaRepository = Depends(get_categoria_repo),
):
    todas = await repo.listar_todas()
    mapa_nome = {(c.nome or "").strip(): c for c in todas}
    resultado = []
    for idx, (nome_area, nomes_cats) in enumerate(AREAS_GRANDES.items(), start=1):
        cats_resp = []
        for nm in nomes_cats:
            c = mapa_nome.get(nm)
            if c:
                cats_resp.append(CategoriaResponse.model_validate(c))
        resultado.append(AreaGrandeResponse(id=idx, nome=nome_area, categorias=cats_resp))
    return resultado


@router.get(
    "/fornecedores",
    response_model=list[FornecedorResponse],
    summary="UC04/RF13 - Listar Fornecedores (filtrado por categorias)",
)
async def listar_fornecedores(
    categorias: str | None = Query(None, description="IDs de categorias separados por vírgula"),
    repo: FornecedorRepositoryImpl = Depends(get_fornecedor_repo),
    categoria_repo: CategoriaRepository = Depends(get_categoria_repo),
):
    if categorias:
        categoria_ids = [int(c) for c in categorias.split(",")]
        fornecedores = await repo.listar_por_categorias(categoria_ids)
    else:
        fornecedores = await repo.listar_ativos()

    response = []
    for fornecedor in fornecedores:
        # Busca categorias do fornecedor
        from sqlalchemy import select

        cat_result = await repo.session.execute(
            select(CategoriaModel)
            .join(FornecedorCategoriaModel)
            .where(FornecedorCategoriaModel.fornecedor_id == fornecedor.id)
        )
        cats = cat_result.scalars().all()
        response.append(
            FornecedorResponse(
                id=fornecedor.id or 0,
                nome=fornecedor.nome,
                cnpj=fornecedor.cnpj,
                categorias=[CategoriaResponse.model_validate(c) for c in cats],
            )
        )
    return response


@router.get(
    "/fornecedores/{fornecedor_id}/disponibilidade",
    response_model=FornecedorDisponibilidadeResponse,
    summary="UC04/UC05 - Calcular Disponibilidade do Fornecedor",
)
async def calcular_disponibilidade_fornecedor(
    fornecedor_id: int,
    produtos: str = Query(..., description="IDs de produtos separados por vírgula"),
    repo: FornecedorRepository = Depends(get_fornecedor_repo),
):
    produto_ids = [int(p) for p in produtos.split(",")]

    itens_disp, itens_aus, preco_total = await repo.calcular_disponibilidade(
        fornecedor_id, produto_ids
    )

    fornecedor = await repo.buscar_por_id(fornecedor_id)
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")

    percentual = (itens_disp / len(produto_ids) * 100) if produto_ids else 0

    return FornecedorDisponibilidadeResponse(
        fornecedor=FornecedorResponse.model_validate(fornecedor),
        percentual_disponibilidade=round(percentual, 1),
        itens_disponiveis=itens_disp,
        itens_totais=len(produto_ids),
    )


class FornecedorDisponibilidadeLoteItem(BaseModel):
    fornecedor_id: int
    percentual_disponibilidade: float
    itens_disponiveis: int
    itens_totais: int


@router.get(
    "/fornecedores/disponibilidade-lote",
    response_model=list[FornecedorDisponibilidadeLoteItem],
    summary="UC04/UC05 - Disponibilidade em lote de fornecedores para uma lista de produtos",
)
async def calcular_disponibilidade_lote(
    produtos: str = Query(..., description="IDs de produtos separados por vírgula"),
    fornecedores: str | None = Query(
        None, description="IDs de fornecedores separados por vírgula (opcional: todos os ativos)"
    ),
    repo: FornecedorRepository = Depends(get_fornecedor_repo),
):
    produto_ids = [int(p) for p in produtos.split(",")]
    if not produto_ids:
        return []

    if fornecedores:
        fornecedor_ids = [int(f) for f in fornecedores.split(",")]
    else:
        todos = await repo.listar_ativos()
        fornecedor_ids = [f.id for f in todos]

    resultado: list[FornecedorDisponibilidadeLoteItem] = []
    for fornecedor_id in fornecedor_ids:
        itens_disp, itens_aus, _preco = await repo.calcular_disponibilidade(
            fornecedor_id, produto_ids
        )
        percentual = (itens_disp / len(produto_ids) * 100) if produto_ids else 0
        resultado.append(
            FornecedorDisponibilidadeLoteItem(
                fornecedor_id=fornecedor_id,
                percentual_disponibilidade=round(percentual, 1),
                itens_disponiveis=itens_disp,
                itens_totais=len(produto_ids),
            )
        )
    return resultado


@router.get(
    "/produtos/autocomplete",
    response_model=list[ProdutoResponse],
    summary="UC02/RF07 - Autocomplete de Produtos (com filtro opcional de categorias)",
)
async def autocomplete_produtos(
    q: str = Query(..., min_length=2, description="Termo de busca"),
    limit: int = Query(10, ge=1, le=50),
    categorias: str | None = Query(None, description="IDs de categorias separados por vírgula (filtro opcional)"),
    repo: ProdutoRepository = Depends(get_produto_repo),
):
    categoria_ids = [int(c) for c in categorias.split(",")] if categorias else None
    produtos = await repo.autocomplete(q, limit, categoria_ids)
    return [ProdutoResponse.model_validate(p) for p in produtos]


@router.get(
    "/produtos",
    response_model=list[ProdutoResponse],
    summary="Listar Produtos Ativos (filtrado por categorias selecionadas, RF19)",
)
async def listar_produtos(
    categorias: str | None = Query(
        None, description="IDs de categorias separados por vírgula (filtra produtos por categoria)"
    ),
    repo: ProdutoRepository = Depends(get_produto_repo),
):
    if categorias:
        categoria_ids = [int(c) for c in categorias.split(",")]
        produtos = await repo.listar_por_categorias(categoria_ids)
    else:
        produtos = await repo.listar_ativos()
    return [ProdutoResponse.model_validate(p) for p in produtos]
