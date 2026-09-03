import { PrismaClient, Testimonial } from '@prisma/client';
import { TestimonialRepositoryContract } from './repository.contracts';

export class TestimonialRepository implements TestimonialRepositoryContract {
  constructor(private prisma: PrismaClient) {}

  async findApproved(): Promise<Testimonial[]> {
    return this.prisma.testimonial.findMany({
      where: { approved: true },
      orderBy: { createdAt: 'desc' },
    });
  }

  async findById(id: string): Promise<Testimonial | null> {
    return this.prisma.testimonial.findUnique({
      where: { id },
    });
  }

  async create(data: { userId: string; authorName: string; content: string }): Promise<Testimonial> {
    return this.prisma.testimonial.create({ data });
  }
}
