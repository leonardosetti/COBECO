import { PrismaClient, Retailer } from '@prisma/client';

export class RetailerRepository {
  constructor(private prisma: PrismaClient) {}

  async findAll(): Promise<Retailer[]> {
    return this.prisma.retailer.findMany();
  }

  async findById(id: string): Promise<Retailer | null> {
    return this.prisma.retailer.findUnique({
      where: { id },
    });
  }

  async findBySlug(slug: string): Promise<Retailer | null> {
    return this.prisma.retailer.findUnique({
      where: { slug },
    });
  }
}
