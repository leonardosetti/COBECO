// O seed roda com cwd em apps/api; sem isto o DATABASE_URL do .env local
// nao chega ao Prisma e o comando documentado falha.
import 'dotenv/config';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

/**
 * RNF09: 50 produtos e 10 fornecedores.
 *
 * Os produtos 1 a 10 e as coberturas de A a H são os da seção 7.3 do documento
 * de concepção e não devem mudar: comparar apenas A-H sobre os produtos 1 a 9
 * tem de continuar gerando os grupos A,B / C,E,F,H / D / G. Fornecedores I e J
 * e os produtos 11 a 50 ampliam o catálogo sem tocar nesse cenário.
 */
const products = [
  'Arroz 5 kg',
  'Feijão 1 kg',
  'Óleo de soja 900 ml',
  'Açúcar 1 kg',
  'Café 500 g',
  'Leite integral 1 L',
  'Farinha de trigo 1 kg',
  'Macarrão 500 g',
  'Sal 1 kg',
  'Produto sem oferta',
  'Molho de tomate 340 g',
  'Extrato de tomate 340 g',
  'Milho em conserva 200 g',
  'Ervilha em conserva 200 g',
  'Atum em lata 170 g',
  'Sardinha em lata 125 g',
  'Biscoito cream cracker 400 g',
  'Biscoito recheado 140 g',
  'Achocolatado em pó 400 g',
  'Chá preto 10 sachês',
  'Manteiga 200 g',
  'Margarina 500 g',
  'Queijo mussarela 500 g',
  'Presunto fatiado 200 g',
  'Iogurte natural 170 g',
  'Requeijão cremoso 200 g',
  'Ovos brancos dúzia',
  'Pão de forma 500 g',
  'Pão francês 1 kg',
  'Bolo pronto 300 g',
  'Frango congelado 1 kg',
  'Carne moída 1 kg',
  'Linguiça toscana 1 kg',
  'Bacon defumado 250 g',
  'Peixe congelado 800 g',
  'Batata 1 kg',
  'Cebola 1 kg',
  'Tomate 1 kg',
  'Alho 200 g',
  'Banana 1 kg',
  'Maçã 1 kg',
  'Laranja 1 kg',
  'Detergente 500 ml',
  'Sabão em pó 1 kg',
  'Amaciante 2 L',
  'Água sanitária 1 L',
  'Papel higiênico 4 rolos',
  'Sabonete 90 g',
  'Creme dental 90 g',
  'Shampoo 350 ml',
].map((name, index) => [`product-${index + 1}`, name] as const);

/** Coberturas fixas do cenário de paridade, sobre os produtos 1 a 9. */
const coverage: Record<string, number[]> = {
  A: [1, 2, 3, 4, 5, 6, 7, 8, 9],
  B: [1, 2, 3, 4, 5, 6, 7, 8, 9],
  C: [1, 2, 3, 4, 5, 6, 8, 9],
  D: [1, 2, 4, 5, 8, 9],
  E: [1, 2, 3, 4, 5, 6, 8, 9],
  F: [1, 2, 3, 4, 5, 6, 8, 9],
  G: [1, 3, 4, 5, 8, 9],
  H: [1, 2, 3, 4, 5, 6, 8, 9],
  I: [1, 2, 3, 5, 6, 7, 8, 9],
  J: [2, 3, 4, 5, 6, 8, 9],
};

/**
 * Produtos 11 a 50: a lacuna determinística dá ao filtro de disponibilidade
 * (RF12) percentuais diferentes para exibir, em vez de 100% em todo mundo.
 */
function extendedCoverage(supplierIndex: number): number[] {
  return Array.from({ length: 40 }, (_, offset) => offset + 11).filter(
    (productNumber) => (productNumber + supplierIndex) % 7 !== 0
  );
}

async function main() {
  const category = await prisma.category.upsert({
    where: { name: 'Supermercado' },
    update: {},
    create: { id: 'supermercado', name: 'Supermercado' },
  });

  for (const [id, name] of products) {
    await prisma.product.upsert({
      where: { id },
      update: { name, categoryId: category.id, active: true },
      create: { id, name, categoryId: category.id },
    });
  }

  for (const [supplierIndex, [letter, productNumbers]] of Object.entries(coverage).entries()) {
    const supplierId = `supplier-${letter.toLowerCase()}`;
    await prisma.supplier.upsert({
      where: { id: supplierId },
      update: { name: `Fornecedor ${letter}`, active: true },
      create: { id: supplierId, name: `Fornecedor ${letter}`, categoryId: category.id },
    });
    for (const productNumber of [...productNumbers, ...extendedCoverage(supplierIndex)]) {
      await prisma.supplierProduct.upsert({
        where: { supplierId_productId: { supplierId, productId: `product-${productNumber}` } },
        update: { price: 5 + productNumber + supplierIndex, active: true },
        create: {
          supplierId,
          productId: `product-${productNumber}`,
          price: 5 + productNumber + supplierIndex,
          active: true,
        },
      });
    }
  }

  await prisma.supplierProduct.upsert({
    where: { supplierId_productId: { supplierId: 'supplier-h', productId: 'product-10' } },
    update: { price: 99, active: false },
    create: { supplierId: 'supplier-h', productId: 'product-10', price: 99, active: false },
  });

  const retailers = [
    ['amazon', 'Amazon', 'https://www.amazon.com.br'],
    ['mercado-livre', 'Mercado Livre', 'https://www.mercadolivre.com.br'],
    ['shopee', 'Shopee', 'https://www.shopee.com.br'],
    ['magazine-luiza', 'Magazine Luiza', 'https://www.magazineluiza.com.br'],
  ];
  for (const [slug, name, websiteUrl] of retailers) {
    await prisma.retailer.upsert({
      where: { slug },
      update: {},
      create: { slug, name, websiteUrl },
    });
  }

  const testimonials = [
    [
      'testimonial-1',
      'João Silva',
      'O COBECO tornou a comparação da minha compra muito mais simples.',
    ],
    [
      'testimonial-2',
      'Maria Santos',
      'Os grupos de cobertura deixam claro onde encontro todos os produtos.',
    ],
    ['testimonial-3', 'Carlos Oliveira', 'Consigo ver rapidamente o orçamento mais econômico.'],
  ];
  for (const [id, authorName, content] of testimonials) {
    await prisma.testimonial.upsert({
      where: { id },
      update: {},
      create: { id, authorName, content, approved: true },
    });
  }
}

main()
  .then(() =>
    console.log('Seed concluído: catálogo A-J (10 fornecedores, 50 produtos) e dados públicos carregados.')
  )
  .catch((error) => {
    console.error(error);
    process.exitCode = 1;
  })
  .finally(() => prisma.$disconnect());
