import { PrismaClient } from '@prisma/client';
import { CatalogRepositoryContract } from '../repository.contracts';

export class PrismaCatalogRepository implements CatalogRepositoryContract {
  constructor(private readonly prisma: PrismaClient) {}

  findCategories() {
    return this.prisma.category.findMany({ orderBy: { name: 'asc' } });
  }

  findSuppliersByCategory(categoryId: string) {
    return this.prisma.supplier.findMany({
      where: { categoryId, active: true },
      orderBy: { name: 'asc' },
    });
  }

  findProductsByCategory(categoryId: string) {
    return this.prisma.product.findMany({
      where: { categoryId, active: true },
      orderBy: { name: 'asc' },
    });
  }

  async findOffers(categoryId: string, supplierIds: string[]) {
    const offers = await this.prisma.supplierProduct.findMany({
      where: {
        supplierId: { in: supplierIds },
        supplier: { categoryId, active: true },
        product: { active: true },
      },
    });
    return offers.map((offer) => ({ ...offer, price: Number(offer.price) }));
  }
}
