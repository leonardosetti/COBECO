-- COBECO — Seed do protótipo alta fidelidade (doc-prototype-0003 v3.2)
-- Fonte: frontend (DOC-03) — 11 categorias, 10 fornecedores, 20 produtos
-- Geração determinística a partir de backend/scripts/script-seed-0003-prototype-seed-v1.0.py

SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;
SET FOREIGN_KEY_CHECKS = 0;

-- Limpeza idempotente dos dados mockados
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

-- Categorias (11 macro — protótipo DOC-03)
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

-- Fornecedores (10 — IDs do protótipo DOC-03)
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

-- Fornecedores por categoria (N:N)
INSERT INTO `fornecedores_categorias` (`fornecedor_id`, `categoria_id`) VALUES
  (1, 1),
  (1, 2),
  (1, 3),
  (1, 5),
  (1, 11),
  (1, 4),
  (2, 1),
  (2, 2),
  (2, 9),
  (2, 11),
  (3, 1),
  (4, 11),
  (4, 4),
  (4, 6),
  (5, 11),
  (5, 4),
  (5, 6),
  (6, 7),
  (6, 8),
  (6, 10),
  (6, 5),
  (7, 5),
  (7, 6),
  (8, 2),
  (9, 2),
  (10, 2);

-- Produtos (20 — protótipo DOC-03)
INSERT INTO `produtos` (`id`, `nome`, `unidade`, `ativo`) VALUES
  (1, 'Arroz Tipo 1 5kg', 'un', TRUE),
  (2, 'Feijão Preto 1kg', 'un', TRUE),
  (3, 'Óleo de Soja 900ml', 'un', TRUE),
  (4, 'Café Torrado e Moído 500g', 'un', TRUE),
  (5, 'Açúcar Refinado 1kg', 'un', TRUE),
  (6, 'Leite Integral UHT 1L', 'un', TRUE),
  (7, 'Macarrão Espaguete 500g', 'un', TRUE),
  (8, 'Molho de Tomate 340g', 'un', TRUE),
  (9, 'Farinha de Trigo 1kg', 'un', TRUE),
  (10, 'Ovos Brancos (dúzia)', 'dz', TRUE),
  (11, 'Detergente Neutro 500ml', 'un', TRUE),
  (12, 'Papel Toalha 2 rolos', 'un', TRUE),
  (13, 'Liquidificador 2 Velocidades', 'un', TRUE),
  (14, 'Notebook i5 8GB', 'un', TRUE),
  (15, 'Martelo de Unha 25mm', 'un', TRUE),
  (16, 'Parafuso Philips 5mm (cx)', 'cx', TRUE),
  (17, 'Camiseta Algodão M', 'un', TRUE),
  (18, 'Calça Jeans 40', 'un', TRUE),
  (19, 'Vaso de Barro 20cm', 'un', TRUE),
  (20, 'Cadeira de Escritório', 'un', TRUE);

-- Preços e estoque (regra do protótipo: base * FATOR[f] * (1 + sin*0.03))
INSERT INTO `fornecedores_produtos` (`fornecedor_id`, `produto_id`, `preco`, `estoque`, `ativo`) VALUES
  (1, 1, 25.51, 9999, TRUE),
  (1, 2, 8.29, 9999, TRUE),
  (1, 3, 7.03, 9999, TRUE),
  (1, 4, 17.56, 9999, TRUE),
  (1, 5, 4.30, 9999, TRUE),
  (1, 6, 4.90, 9999, TRUE),
  (1, 7, 4.65, 9999, TRUE),
  (1, 8, 3.88, 9999, TRUE),
  (1, 9, 5.59, 9999, TRUE),
  (1, 10, 10.06, 9999, TRUE),
  (1, 11, 2.88, 9999, TRUE),
  (1, 12, 6.29, 9999, TRUE),
  (1, 13, 124.82, 9999, TRUE),
  (1, 14, 2834.51, 9999, TRUE),
  (1, 17, 40.29, 9999, TRUE),
  (1, 18, 117.92, 9999, TRUE),
  (2, 1, 24.78, 9999, TRUE),
  (2, 2, 7.70, 9999, TRUE),
  (2, 3, 6.31, 9999, TRUE),
  (2, 5, 4.02, 9999, TRUE),
  (2, 6, 4.79, 9999, TRUE),
  (2, 7, 4.59, 9999, TRUE),
  (2, 8, 3.71, 9999, TRUE),
  (2, 9, 5.11, 9999, TRUE),
  (2, 10, 8.98, 9999, TRUE),
  (2, 11, 2.62, 9999, TRUE),
  (2, 12, 5.99, 9999, TRUE),
  (2, 13, 123.01, 9999, TRUE),
  (2, 17, 36.03, 9999, TRUE),
  (3, 1, 28.93, 9999, TRUE),
  (3, 2, 9.07, 9999, TRUE),
  (3, 3, 7.75, 9999, TRUE),
  (3, 4, 20.21, 9999, TRUE),
  (3, 5, 5.16, 9999, TRUE),
  (3, 6, 5.94, 9999, TRUE),
  (3, 7, 5.45, 9999, TRUE),
  (3, 8, 4.33, 9999, TRUE),
  (3, 9, 6.10, 9999, TRUE),
  (3, 10, 11.23, 9999, TRUE),
  (3, 11, 3.38, 9999, TRUE),
  (3, 12, 7.63, 9999, TRUE),
  (4, 13, 120.96, 9999, TRUE),
  (4, 14, 2733.93, 9999, TRUE),
  (4, 20, 419.69, 9999, TRUE),
  (5, 13, 138.18, 9999, TRUE),
  (5, 14, 3133.90, 9999, TRUE),
  (5, 20, 482.52, 9999, TRUE),
  (6, 15, 31.01, 9999, TRUE),
  (6, 16, 11.83, 9999, TRUE),
  (6, 19, 45.80, 9999, TRUE),
  (6, 20, 440.51, 9999, TRUE),
  (7, 19, 49.45, 9999, TRUE),
  (7, 20, 480.18, 9999, TRUE),
  (8, 17, 37.02, 9999, TRUE),
  (8, 18, 110.61, 9999, TRUE),
  (9, 17, 39.64, 9999, TRUE),
  (9, 18, 122.28, 9999, TRUE),
  (10, 17, 42.71, 9999, TRUE);

SET FOREIGN_KEY_CHECKS = 1;

-- Verificação do volume persistido
SELECT 'categorias' AS tabela, COUNT(*) AS quantidade FROM `categorias`
UNION ALL SELECT 'fornecedores', COUNT(*) FROM `fornecedores`
UNION ALL SELECT 'produtos', COUNT(*) FROM `produtos` WHERE `ativo` = TRUE
UNION ALL SELECT 'precos', COUNT(*) FROM `fornecedores_produtos` WHERE `ativo` = TRUE
UNION ALL SELECT 'relacoes', COUNT(*) FROM `fornecedores_categorias`;
