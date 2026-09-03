import { PrismaClient, User } from '@prisma/client';
import { UserCreateData, UserRepositoryContract } from './repository.contracts';

export class UserRepository implements UserRepositoryContract {
  constructor(private prisma: PrismaClient) {}

  async create(data: UserCreateData): Promise<User> {
    return this.prisma.user.create({ data });
  }

  async findByEmail(email: string): Promise<User | null> {
    return this.prisma.user.findUnique({
      where: { email },
    });
  }

  async findByUsername(username: string): Promise<User | null> {
    return this.prisma.user.findUnique({
      where: { username: username.trim().toLowerCase() },
    });
  }

  async findByEmailOrUsername(identifier: string): Promise<User | null> {
    const normalized = identifier.trim().toLowerCase();
    return this.prisma.user.findFirst({
      where: { OR: [{ email: normalized }, { username: normalized }] },
    });
  }

  async findById(id: string): Promise<User | null> {
    return this.prisma.user.findUnique({
      where: { id },
    });
  }

  async updatePassword(id: string, passwordHash: string): Promise<User> {
    return this.prisma.user.update({
      where: { id },
      data: { passwordHash, updatedAt: new Date() },
    });
  }

  async softDelete(id: string): Promise<User> {
    return this.prisma.user.update({
      where: { id },
      data: { deletedAt: new Date() },
    });
  }

  async updateConsent(id: string): Promise<User> {
    return this.prisma.user.update({
      where: { id },
      data: { consentedAt: new Date() },
    });
  }
}
