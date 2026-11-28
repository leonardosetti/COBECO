-- COBECO — Seed gerado a partir do pré-seed (scripts/pre_seed.csv)
-- Equalização: fornecedores_produtos apenas quando atende_categoria = S
-- Flag de estoque: ativo = disponível; estoque = 0 quando indisponível

SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;
SET FOREIGN_KEY_CHECKS = 0;

-- Limpeza idempotente dos dados
DELETE FROM `sessoes`;
DELETE FROM `fornecedores_produtos`;
DELETE FROM `fornecedores_categorias`;
DELETE FROM `itens_lista`;
DELETE FROM `listas`;
DELETE FROM `usuarios`;
DELETE FROM `produtos`;
DELETE FROM `fornecedores`;
DELETE FROM `categorias`;

ALTER TABLE `sessoes` AUTO_INCREMENT = 1;
ALTER TABLE `usuarios` AUTO_INCREMENT = 1;
ALTER TABLE `listas` AUTO_INCREMENT = 1;
ALTER TABLE `itens_lista` AUTO_INCREMENT = 1;
ALTER TABLE `categorias` AUTO_INCREMENT = 1;
ALTER TABLE `fornecedores` AUTO_INCREMENT = 1;
ALTER TABLE `produtos` AUTO_INCREMENT = 1;

-- Categorias
INSERT INTO `categorias` (`id`, `nome`, `descricao`) VALUES
  (1, 'Mercado', 'Supermercados, mercearias e atacados'),
  (2, 'Vestuário', 'Roupas, calçados e acessórios'),
  (3, 'Automotivos', 'Peças, acessórios e serviços automotivos'),
  (4, 'Informática', 'Computadores, periféricos e eletrônicos'),
  (5, 'Decoração', 'Itens de decoração e artigos para casa'),
  (6, 'Móveis', 'Móveis residenciais e corporativos'),
  (7, 'Materiais de Construção e Ferragens', 'Materiais de construção, ferramentas e ferragens'),
  (8, 'Ferramentas', 'Ferramentas manuais, elétricas e de medição'),
  (9, 'Livros', 'Livros, revistas e publicações'),
  (10, 'Jardinagem', 'Plantas, ferramentas e artigos de jardim'),
  (11, 'Eletrodomésticos', 'Eletrodomésticos de linha branca e marrom');

-- Fornecedores
INSERT INTO `fornecedores` (`id`, `nome`, `cnpj`, `ativo`) VALUES
  (1, 'Carrefour', '99.000.111/0001-22', TRUE),
  (2, 'Extra', '00.111.222/0001-33', TRUE),
  (3, 'Pão de Açúcar', '66.777.888/0001-99', TRUE),
  (4, 'Magazine Luiza', '77.888.999/0001-00', TRUE),
  (5, 'Casas Bahia', '88.999.000/0001-11', TRUE),
  (6, 'Leroy Merlin', '11.222.333/0001-44', TRUE),
  (7, 'Etna', '22.333.444/0001-55', TRUE),
  (8, 'C&A', '33.444.555/0001-66', TRUE),
  (9, 'Renner', '44.555.666/0001-77', TRUE),
  (10, 'Hering', '55.666.777/0001-88', TRUE);

-- Fornecedores por categoria (N:N, da equalização do CSV)
INSERT INTO `fornecedores_categorias` (`fornecedor_id`, `categoria_id`) VALUES
  (1, 1),
  (1, 11),
  (2, 1),
  (3, 1),
  (4, 4),
  (4, 6),
  (4, 11),
  (5, 4),
  (5, 6),
  (5, 11),
  (6, 5),
  (6, 7),
  (6, 8),
  (7, 5),
  (7, 6),
  (8, 2),
  (9, 2),
  (10, 2);

-- Produtos (categoria_id atribuído conforme pré-seed)
INSERT INTO `produtos` (`id`, `nome`, `unidade`, `ativo`, `categoria_id`) VALUES
  (1, 'Arroz Tipo 1 5kg', 'un', TRUE, 1),
  (2, 'Feijão Preto 1kg', 'un', TRUE, 1),
  (3, 'Óleo de Soja 900ml', 'un', TRUE, 1),
  (4, 'Café Torrado e Moído 500g', 'un', TRUE, 1),
  (5, 'Açúcar Refinado 1kg', 'un', TRUE, 1),
  (6, 'Leite Integral UHT 1L', 'un', TRUE, 1),
  (7, 'Macarrão Espaguete 500g', 'un', TRUE, 1),
  (8, 'Molho de Tomate 340g', 'un', TRUE, 1),
  (9, 'Farinha de Trigo 1kg', 'un', TRUE, 1),
  (10, 'Ovos Brancos (dúzia)', 'dz', TRUE, 1),
  (11, 'Camiseta Algodão M', 'un', TRUE, 2),
  (12, 'Calça Jeans 40', 'un', TRUE, 2),
  (13, 'Notebook i5 8GB', 'un', TRUE, 4),
  (14, 'Liquidificador 2 Velocidades', 'un', TRUE, 11),
  (15, 'Martelo de Unha 25mm', 'un', TRUE, 8),
  (16, 'Parafuso Philips 5mm (cx)', 'cx', TRUE, 7),
  (17, 'Vaso de Barro 20cm', 'un', TRUE, 5),
  (18, 'Cadeira de Escritório', 'un', TRUE, 6),
  (19, 'Smartphone Galaxy S23', 'un', TRUE, 4),
  (20, 'Geladeira Frost Free 400L', 'un', TRUE, 11);

-- Preços e estoque (equalizados por categoria; flag disponível/indisponível)
INSERT INTO `fornecedores_produtos` (`fornecedor_id`, `produto_id`, `preco`, `estoque`, `ativo`) VALUES
  (1, 1, 25.50, 9999, TRUE),
  (2, 1, 24.80, 9999, TRUE),
  (3, 1, 28.90, 12, TRUE),
  (1, 2, 8.30, 9999, TRUE),
  (2, 2, 7.70, 9999, TRUE),
  (3, 2, 9.10, 0, FALSE),
  (1, 3, 7.05, 9999, TRUE),
  (2, 3, 6.30, 9999, TRUE),
  (3, 3, 7.75, 45, TRUE),
  (1, 4, 17.55, 9999, TRUE),
  (2, 4, 16.90, 8, TRUE),
  (3, 4, 20.20, 0, FALSE),
  (1, 5, 4.30, 9999, TRUE),
  (2, 5, 4.00, 9999, TRUE),
  (3, 5, 5.15, 100, TRUE),
  (1, 6, 4.90, 9999, TRUE),
  (2, 6, 4.78, 9999, TRUE),
  (3, 6, 5.95, 3, TRUE),
  (1, 7, 4.65, 9999, TRUE),
  (2, 7, 4.58, 9999, TRUE),
  (3, 7, 5.45, 50, TRUE),
  (1, 8, 3.90, 9999, TRUE),
  (2, 8, 3.70, 9999, TRUE),
  (3, 8, 4.35, 0, FALSE),
  (1, 9, 5.60, 9999, TRUE),
  (2, 9, 5.10, 9999, TRUE),
  (3, 9, 6.10, 20, TRUE),
  (1, 10, 10.05, 9999, TRUE),
  (2, 10, 8.98, 9999, TRUE),
  (3, 10, 11.25, 2, FALSE),
  (8, 11, 40.30, 9999, TRUE),
  (9, 11, 39.65, 15, TRUE),
  (10, 11, 42.70, 0, FALSE),
  (8, 12, 110.60, 8, TRUE),
  (9, 12, 122.30, 9999, TRUE),
  (10, 12, 117.90, 3, TRUE),
  (4, 13, 2834.50, 4, TRUE),
  (5, 13, 3133.90, 0, FALSE),
  (4, 19, 3450.00, 2, TRUE),
  (1, 14, 124.80, 9999, TRUE),
  (4, 14, 120.95, 7, TRUE),
  (5, 14, 138.18, 0, FALSE),
  (1, 20, 4400.00, 2, TRUE),
  (4, 20, 4190.00, 0, FALSE),
  (5, 20, 4825.20, 1, TRUE),
  (6, 15, 31.00, 9999, TRUE),
  (6, 16, 11.85, 9999, TRUE),
  (6, 17, 45.80, 9999, TRUE),
  (7, 17, 49.45, 3, TRUE),
  (4, 18, 440.50, 4, TRUE),
  (5, 18, 480.18, 0, FALSE),
  (7, 18, 480.18, 2, TRUE);

SET FOREIGN_KEY_CHECKS = 1;

-- Verificação do volume persistido
SELECT 'categorias' AS tabela, COUNT(*) AS quantidade FROM `categorias`
UNION ALL SELECT 'fornecedores', COUNT(*) FROM `fornecedores`
UNION ALL SELECT 'produtos', COUNT(*) FROM `produtos` WHERE `ativo` = TRUE
UNION ALL SELECT 'precos', COUNT(*) FROM `fornecedores_produtos` WHERE `ativo` = TRUE
UNION ALL SELECT 'relacoes', COUNT(*) FROM `fornecedores_categorias`;
