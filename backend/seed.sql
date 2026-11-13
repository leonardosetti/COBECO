-- COBECO MVP — Seed SQL (MySQL 8 InnoDB)
-- Executado automaticamente na inicialização do container DB
-- Popula: 11 categorias, 10 fornecedores, 50 produtos, ~300 preços
-- Baseado em CAMADADEDADOS.md v3.2

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================================
-- LIMPA DADOS EXISTENTES (idempotente)
-- ============================================================
DELETE FROM `fornecedores_produtos`;
DELETE FROM `fornecedores_categorias`;
DELETE FROM `itens_lista`;
DELETE FROM `listas`;
DELETE FROM `usuarios`;
DELETE FROM `produtos`;
DELETE FROM `fornecedores`;
DELETE FROM `categorias`;

-- Reset auto_increment
ALTER TABLE `categorias` AUTO_INCREMENT = 1;
ALTER TABLE `fornecedores` AUTO_INCREMENT = 1;
ALTER TABLE `produtos` AUTO_INCREMENT = 1;
ALTER TABLE `usuarios` AUTO_INCREMENT = 1;
ALTER TABLE `listas` AUTO_INCREMENT = 1;
ALTER TABLE `itens_lista` AUTO_INCREMENT = 1;

-- ============================================================
-- CATEGORIAS (11 categorias MACRO)
-- ============================================================
INSERT INTO `categorias` (`nome`, `descricao`) VALUES
('Mercado', 'Supermercados, mercearias e atacados'),
('Vestuário', 'Roupas, calçados e acessórios'),
('Automotivos', 'Peças, acessórios e serviços automotivos'),
('Informática', 'Computadores, periféricos e eletrônicos'),
('Decoração', 'Itens de decoração e artigos para casa'),
('Móveis', 'Móveis residenciais e corporativos'),
('Materiais de Construção e Ferragens', 'Materiais de construção, ferramentas e ferragens'),
('Ferramentas', 'Ferramentas manuais, elétricas e de medição'),
('Livros', 'Livros, revistas e publicações'),
('Jardinagem', 'Plantas, ferramentas e artigos de jardim'),
('Eletrodomésticos', 'Eletrodomésticos de linha branca e marrom');

-- ============================================================
-- FORNECEDORES (10 fornecedores)
-- ============================================================
INSERT INTO `fornecedores` (`nome`, `cnpj`, `ativo`) VALUES
('Leroy Merlin', '11.222.333/0001-44', TRUE),
('Etna', '22.333.444/0001-55', TRUE),
('C&A', '33.444.555/0001-66', TRUE),
('Renner', '44.555.666/0001-77', TRUE),
('Hering', '55.666.777/0001-88', TRUE),
('Pão de Açúcar', '66.777.888/0001-99', TRUE),
('Magazine Luiza', '77.888.999/0001-00', TRUE),
('Casas Bahia', '88.999.000/0001-11', TRUE),
('Carrefour', '99.000.111/0001-22', TRUE),
('Extra', '00.111.222/0001-33', TRUE);

-- ============================================================
-- FORNECEDORES_CATEGORIAS (N:N ~25 relações)
-- ============================================================
-- Leroy Merlin (1) -> Materiais de Construção (7), Ferramentas (8), Jardinagem (10), Decoração (5)
INSERT INTO `fornecedores_categorias` (`fornecedor_id`, `categoria_id`) VALUES
(1, 7), (1, 8), (1, 10), (1, 5);

-- Etna (2) -> Decoração (5), Móveis (6)
INSERT INTO `fornecedores_categorias` (`fornecedor_id`, `categoria_id`) VALUES
(2, 5), (2, 6);

-- C&A (3) -> Vestuário (2)
INSERT INTO `fornecedores_categorias` (`fornecedor_id`, `categoria_id`) VALUES
(3, 2);

-- Renner (4) -> Vestuário (2)
INSERT INTO `fornecedores_categorias` (`fornecedor_id`, `categoria_id`) VALUES
(4, 2);

-- Hering (5) -> Vestuário (2)
INSERT INTO `fornecedores_categorias` (`fornecedor_id`, `categoria_id`) VALUES
(5, 2);

-- Pão de Açúcar (6) -> Mercado (1)
INSERT INTO `fornecedores_categorias` (`fornecedor_id`, `categoria_id`) VALUES
(6, 1);

-- Magazine Luiza (7) -> Eletrodomésticos (11), Informática (4), Móveis (6)
INSERT INTO `fornecedores_categorias` (`fornecedor_id`, `categoria_id`) VALUES
(7, 11), (7, 4), (7, 6);

-- Casas Bahia (8) -> Eletrodomésticos (11), Informática (4), Móveis (6)
INSERT INTO `fornecedores_categorias` (`fornecedor_id`, `categoria_id`) VALUES
(8, 11), (8, 4), (8, 6);

-- Carrefour (9) -> Mercado (1), Vestuário (2), Automotivos (3), Decoração (5), Eletrodomésticos (11), Informática (4)
INSERT INTO `fornecedores_categorias` (`fornecedor_id`, `categoria_id`) VALUES
(9, 1), (9, 2), (9, 3), (9, 5), (9, 11), (9, 4);

-- Extra (10) -> Mercado (1), Vestuário (2), Eletrodomésticos (11)
INSERT INTO `fornecedores_categorias` (`fornecedor_id`, `categoria_id`) VALUES
(10, 1), (10, 2), (10, 11);

-- ============================================================
-- PRODUTOS (50 produtos agnósticos à categoria)
-- ============================================================
INSERT INTO `produtos` (`nome`, `unidade`, `ativo`) VALUES
-- Alimentos (Mercado)
('Arroz Tipo 1 5kg', 'un', TRUE),
('Feijão Preto 1kg', 'un', TRUE),
('Óleo de Soja 900ml', 'un', TRUE),
('Açúcar Cristal 1kg', 'un', TRUE),
('Sal Refinado 1kg', 'un', TRUE),
('Macarrão Espaguete 500g', 'un', TRUE),
('Leite Integral 1L', 'un', TRUE),
('Café Torrado 500g', 'un', TRUE),
('Pão de Forma 500g', 'un', TRUE),
('Manteiga 200g', 'un', TRUE),

-- Ferramentas (Ferramentas, Materiais Construção)
('Martelo de Unha 25mm', 'un', TRUE),
('Chave de Fenda Philips #2', 'un', TRUE),
('Alicate Universal 8"', 'un', TRUE),
('Trena 5m', 'un', TRUE),
('Nível Bolha 40cm', 'un', TRUE),
('Parafusadeira Elétrica 12V', 'un', TRUE),
('Furadeira de Impacto 650W', 'un', TRUE),
('Serra Circular 7-1/4"', 'un', TRUE),
('Lixadeira Orbital', 'un', TRUE),
('Jogo de Chaves Allen', 'un', TRUE),

-- Informática
('Notebook i5 8GB 256GB SSD', 'un', TRUE),
('Mouse Óptico USB', 'un', TRUE),
('Teclado Mecânico ABNT2', 'un', TRUE),
('Monitor 24" Full HD', 'un', TRUE),
('HD Externo 1TB USB 3.0', 'un', TRUE),
('Pen Drive 64GB', 'un', TRUE),
('Cabo HDMI 2m', 'un', TRUE),
('Webcam HD 720p', 'un', TRUE),
('Headset Gamer USB', 'un', TRUE),
('Carregador Notebook 65W', 'un', TRUE),

-- Vestuário
('Camiseta Algodão M', 'un', TRUE),
('Calça Jeans Masculina 42', 'un', TRUE),
('Vestido Floral M', 'un', TRUE),
('Tênis Esportivo 41', 'un', TRUE),
('Meia Cano Curto (par)', 'un', TRUE),
('Cinto Couro Sintético', 'un', TRUE),
('Boné Aba Curva', 'un', TRUE),
('Luva de Lã', 'un', TRUE),
('Cachecol Tricô', 'un', TRUE),
('Jaqueta Jeans G', 'un', TRUE),

-- Casa/Decoração
('Vaso Cerâmica 30cm', 'un', TRUE),
('Quadro Decorativo 40x50', 'un', TRUE),
('Tapete Sala 2x3m', 'un', TRUE),
('Cortina Blackout 2,5x3m', 'un', TRUE),
('Almofada 45x45cm', 'un', TRUE),
('Porta-retrato 15x20', 'un', TRUE),
('Relógio Parede 30cm', 'un', TRUE),
('Espelho Redondo 60cm', 'un', TRUE),
('Luminária de Mesa', 'un', TRUE),
('Cesto Organizador 40L', 'un', TRUE),

-- Eletrodomésticos
('Geladeira Frost Free 340L', 'un', TRUE),
('Fogão 4 Bocas Inox', 'un', TRUE),
('Micro-ondas 30L', 'un', TRUE),
('Lava-louças 8 Serviços', 'un', TRUE),
('Ar Condicionado 9000 BTU', 'un', TRUE);

-- ============================================================
-- FORNECEDORES_PRODUTOS (~300 preços com variação ±20%)
-- Preços base com variação aleatória por fornecedor
-- ============================================================

-- Função auxiliar para preço com variação
-- Preço final = base * (0.8 a 1.2) * fator_fornecedor

-- Leroy Merlin (1) - foco: Materiais, Ferramentas, Jardinagem, Decoração
INSERT INTO `fornecedores_produtos` (`fornecedor_id`, `produto_id`, `preco`, `estoque`, `ativo`) VALUES
(1, 11, 45.90, 50, TRUE), (1, 12, 18.50, 100, TRUE), (1, 13, 32.90, 80, TRUE),
(1, 14, 25.90, 60, TRUE), (1, 15, 28.90, 40, TRUE), (1, 16, 189.90, 20, TRUE),
(1, 17, 299.90, 15, TRUE), (1, 18, 349.90, 10, TRUE), (1, 19, 229.90, 12, TRUE),
(1, 20, 89.90, 25, TRUE), (1, 31, 42.90, 30, TRUE), (1, 32, 89.90, 20, TRUE),
(1, 33, 189.90, 15, TRUE), (1, 34, 45.90, 40, TRUE), (1, 35, 12.90, 50, TRUE),
(1, 36, 28.90, 35, TRUE), (1, 37, 35.90, 25, TRUE), (1, 38, 55.90, 20, TRUE),
(1, 39, 42.90, 30, TRUE), (1, 40, 65.90, 15, TRUE);

-- Etna (2) - foco: Decoração, Móveis
INSERT INTO `fornecedores_produtos` (`fornecedor_id`, `produto_id`, `preco`, `estoque`, `ativo`) VALUES
(2, 31, 55.90, 25, TRUE), (2, 32, 129.90, 15, TRUE), (2, 33, 249.90, 10, TRUE),
(2, 34, 65.90, 30, TRUE), (2, 35, 18.90, 40, TRUE), (2, 36, 42.90, 20, TRUE),
(2, 37, 48.90, 15, TRUE), (2, 38, 72.90, 12, TRUE), (2, 39, 58.90, 20, TRUE),
(2, 40, 85.90, 10, TRUE);

-- C&A (3) - foco: Vestuário
INSERT INTO `fornecedores_produtos` (`fornecedor_id`, `produto_id`, `preco`, `estoque`, `ativo`) VALUES
(3, 21, 39.90, 100, TRUE), (3, 22, 89.90, 80, TRUE), (3, 23, 79.90, 60, TRUE),
(3, 24, 129.90, 50, TRUE), (3, 25, 19.90, 200, TRUE), (3, 26, 34.90, 80, TRUE),
(3, 27, 29.90, 120, TRUE), (3, 28, 24.90, 150, TRUE), (3, 29, 32.90, 100, TRUE),
(3, 30, 149.90, 40, TRUE);

-- Renner (4) - foco: Vestuário
INSERT INTO `fornecedores_produtos` (`fornecedor_id`, `produto_id`, `preco`, `estoque`, `ativo`) VALUES
(4, 21, 44.90, 90, TRUE), (4, 22, 99.90, 70, TRUE), (4, 23, 89.90, 55, TRUE),
(4, 24, 149.90, 45, TRUE), (4, 25, 22.90, 180, TRUE), (4, 26, 39.90, 70, TRUE),
(4, 27, 34.90, 110, TRUE), (4, 28, 29.90, 130, TRUE), (4, 29, 37.90, 90, TRUE),
(4, 30, 169.90, 35, TRUE);

-- Hering (5) - foco: Vestuário
INSERT INTO `fornecedores_produtos` (`fornecedor_id`, `produto_id`, `preco`, `estoque`, `ativo`) VALUES
(5, 21, 34.90, 110, TRUE), (5, 22, 79.90, 85, TRUE), (5, 23, 69.90, 65, TRUE),
(5, 24, 119.90, 55, TRUE), (5, 25, 17.90, 220, TRUE), (5, 26, 29.90, 90, TRUE),
(5, 27, 24.90, 130, TRUE), (5, 28, 19.90, 160, TRUE), (5, 29, 27.90, 110, TRUE),
(5, 30, 129.90, 50, TRUE);

-- Pão de Açúcar (6) - foco: Mercado
INSERT INTO `fornecedores_produtos` (`fornecedor_id`, `produto_id`, `preco`, `estoque`, `ativo`) VALUES
(6, 1, 24.90, 200, TRUE), (6, 2, 9.90, 300, TRUE), (6, 3, 8.90, 250, TRUE),
(6, 4, 4.90, 400, TRUE), (6, 5, 3.50, 500, TRUE), (6, 6, 5.90, 350, TRUE),
(6, 7, 6.50, 300, TRUE), (6, 8, 18.90, 200, TRUE), (6, 9, 8.90, 250, TRUE),
(6, 10, 12.90, 180, TRUE);

-- Magazine Luiza (7) - foco: Eletrodomésticos, Informática, Móveis
INSERT INTO `fornecedores_produtos` (`fornecedor_id`, `produto_id`, `preco`, `estoque`, `ativo`) VALUES
(7, 11, 52.90, 40, TRUE), (7, 12, 22.90, 90, TRUE), (7, 13, 38.90, 70, TRUE),
(7, 14, 29.90, 55, TRUE), (7, 15, 33.90, 35, TRUE), (7, 16, 219.90, 18, TRUE),
(7, 17, 329.90, 12, TRUE), (7, 18, 389.90, 8, TRUE), (7, 19, 259.90, 10, TRUE),
(7, 20, 99.90, 22, TRUE), (7, 41, 2899.90, 10, TRUE), (7, 42, 1299.90, 8, TRUE),
(7, 43, 1899.90, 6, TRUE), (7, 44, 2199.90, 5, TRUE), (7, 45, 3499.90, 4, TRUE);

-- Casas Bahia (8) - foco: Eletrodomésticos, Informática, Móveis
INSERT INTO `fornecedores_produtos` (`fornecedor_id`, `produto_id`, `preco`, `estoque`, `ativo`) VALUES
(8, 11, 49.90, 45, TRUE), (8, 12, 20.90, 95, TRUE), (8, 13, 35.90, 75, TRUE),
(8, 14, 27.90, 60, TRUE), (8, 15, 31.90, 40, TRUE), (8, 16, 199.90, 20, TRUE),
(8, 17, 289.90, 15, TRUE), (8, 18, 349.90, 10, TRUE), (8, 19, 239.90, 12, TRUE),
(8, 20, 92.90, 25, TRUE), (8, 41, 2699.90, 12, TRUE), (8, 42, 1199.90, 10, TRUE),
(8, 43, 1799.90, 8, TRUE), (8, 44, 2099.90, 6, TRUE), (8, 45, 3299.90, 5, TRUE);

-- Carrefour (9) - foco: Mercado, Vestuário, Automotivos, Decoração, Eletrodomésticos, Informática
INSERT INTO `fornecedores_produtos` (`fornecedor_id`, `produto_id`, `preco`, `estoque`, `ativo`) VALUES
(9, 1, 22.90, 250, TRUE), (9, 2, 8.90, 350, TRUE), (9, 3, 7.90, 300, TRUE),
(9, 4, 4.50, 450, TRUE), (9, 5, 3.20, 550, TRUE), (9, 6, 5.50, 400, TRUE),
(9, 7, 6.20, 350, TRUE), (9, 8, 16.90, 220, TRUE), (9, 9, 7.90, 280, TRUE),
(9, 10, 11.90, 200, TRUE), (9, 11, 47.90, 50, TRUE), (9, 12, 19.90, 100, TRUE),
(9, 13, 33.90, 80, TRUE), (9, 14, 24.90, 70, TRUE), (9, 15, 27.90, 50, TRUE),
(9, 16, 179.90, 22, TRUE), (9, 17, 269.90, 18, TRUE), (9, 18, 319.90, 12, TRUE),
(9, 19, 219.90, 15, TRUE), (9, 20, 85.90, 28, TRUE), (9, 21, 37.90, 120, TRUE),
(9, 22, 84.90, 90, TRUE), (9, 23, 74.90, 70, TRUE), (9, 24, 124.90, 55, TRUE),
(9, 25, 18.90, 220, TRUE), (9, 26, 32.90, 95, TRUE), (9, 27, 27.90, 140, TRUE),
(9, 28, 22.90, 180, TRUE), (9, 29, 29.90, 120, TRUE), (9, 30, 139.90, 45, TRUE),
(9, 31, 40.90, 35, TRUE), (9, 32, 84.90, 25, TRUE), (9, 33, 179.90, 18, TRUE),
(9, 34, 42.90, 45, TRUE), (9, 35, 11.90, 60, TRUE), (9, 36, 26.90, 30, TRUE),
(9, 37, 33.90, 22, TRUE), (9, 38, 52.90, 18, TRUE), (9, 39, 40.90, 25, TRUE),
(9, 40, 62.90, 15, TRUE), (9, 41, 2799.90, 15, TRUE), (9, 42, 1399.90, 12, TRUE),
(9, 43, 1999.90, 10, TRUE), (9, 44, 2299.90, 8, TRUE), (9, 45, 3599.90, 6, TRUE);

-- Extra (10) - foco: Mercado, Vestuário, Eletrodomésticos
INSERT INTO `fornecedores_produtos` (`fornecedor_id`, `produto_id`, `preco`, `estoque`, `ativo`) VALUES
(10, 1, 23.90, 220, TRUE), (10, 2, 9.50, 320, TRUE), (10, 3, 8.50, 280, TRUE),
(10, 4, 4.80, 420, TRUE), (10, 5, 3.40, 480, TRUE), (10, 6, 5.80, 380, TRUE),
(10, 7, 6.40, 320, TRUE), (10, 8, 17.90, 200, TRUE), (10, 9, 8.50, 260, TRUE),
(10, 10, 12.50, 190, TRUE), (10, 21, 42.90, 100, TRUE), (10, 22, 94.90, 80, TRUE),
(10, 23, 84.90, 60, TRUE), (10, 24, 139.90, 50, TRUE), (10, 25, 21.90, 200, TRUE),
(10, 26, 36.90, 85, TRUE), (10, 27, 32.90, 110, TRUE), (10, 28, 26.90, 140, TRUE),
(10, 29, 34.90, 100, TRUE), (10, 30, 159.90, 40, TRUE), (10, 41, 2899.90, 10, TRUE),
(10, 42, 1299.90, 8, TRUE), (10, 43, 1899.90, 6, TRUE), (10, 44, 2199.90, 5, TRUE),
(10, 45, 3499.90, 4, TRUE);

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================
-- VERIFICAÇÃO RÁPIDA
-- ============================================================
SELECT 'Categorias' AS tabela, COUNT(*) AS qtd FROM categorias
UNION ALL SELECT 'Fornecedores', COUNT(*) FROM fornecedores
UNION ALL SELECT 'Produtos', COUNT(*) FROM produtos WHERE ativo = TRUE
UNION ALL SELECT 'Preços (fornecedores_produtos)', COUNT(*) FROM fornecedores_produtos WHERE ativo = TRUE;