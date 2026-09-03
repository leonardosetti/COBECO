import { NormalizedPriceResult, PriceProvider, PriceSearchInput } from '../price-provider';

export interface MockProductInput {
  id: string;
  productName: string;
  price?: number | null;
  currency?: string;
  deliveryDays?: number | null;
  description?: string;
  redirectUrl?: string;
}

export class MockPriceProvider implements PriceProvider {
  readonly slug = 'mock';
  readonly displayName = 'Provider de desenvolvimento';
  calls = 0;

  constructor(
    private readonly products: MockProductInput[] = [
      { id: 'mock-arroz', productName: 'Arroz 5kg', price: 29.9, deliveryDays: 3 },
      { id: 'mock-cafe', productName: 'Café torrado 500g', price: 18.5, deliveryDays: 2 },
    ]
  ) {}

  async search(input: PriceSearchInput): Promise<NormalizedPriceResult[]> {
    this.calls += 1;
    const query = input.query.toLocaleLowerCase('pt-BR');
    return this.products
      .filter((product) => product.productName.toLocaleLowerCase('pt-BR').includes(query))
      .map((product) => ({
        id: `${this.slug}:${product.id}`,
        providerSlug: this.slug,
        retailerName: 'COBECO (mock)',
        retailerSlug: this.slug,
        productName: product.productName,
        description: product.description,
        price: product.price ?? null,
        currency: product.currency ?? 'BRL',
        deliveryDays: product.deliveryDays ?? null,
        redirectUrl: product.redirectUrl ?? 'https://example.com/mock-product',
        fetchedAt: new Date(),
        incompleteFields: [
          ...(product.price == null ? (['price'] as const) : []),
          ...(product.deliveryDays == null ? (['deliveryDays'] as const) : []),
        ],
      }));
  }
}
