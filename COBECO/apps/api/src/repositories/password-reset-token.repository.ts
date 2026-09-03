import { PrismaClient, PasswordResetToken } from '@prisma/client';
import { verify as verifyHash } from 'argon2';
import {
  PasswordResetTokenRecord,
  PasswordResetTokenRepositoryContract,
} from './repository.contracts';

export class PasswordResetTokenRepository implements PasswordResetTokenRepositoryContract {
  constructor(private prisma: PrismaClient) {}

  async create(data: { userId: string; tokenHash: string; expiresAt: Date }): Promise<PasswordResetToken> {
    return this.prisma.passwordResetToken.create({
      data: {
        user: { connect: { id: data.userId } },
        tokenHash: data.tokenHash,
        expiresAt: data.expiresAt,
      },
    });
  }

  async findByTokenHash(tokenHash: string): Promise<PasswordResetToken | null> {
    return this.prisma.passwordResetToken.findUnique({
      where: { tokenHash },
      include: { user: true },
    });
  }

  async findByToken(token: string): Promise<PasswordResetTokenRecord | null> {
    const tokens = await this.prisma.passwordResetToken.findMany({
      where: { usedAt: null, expiresAt: { gte: new Date() } },
    });
    for (const tokenRecord of tokens) {
      if (await verifyHash(tokenRecord.tokenHash, token)) return tokenRecord;
    }
    return null;
  }

  async markAsUsed(id: string): Promise<PasswordResetToken> {
    return this.prisma.passwordResetToken.update({
      where: { id },
      data: { usedAt: new Date() },
    });
  }

  async deleteExpired(): Promise<{ count: number }> {
    return this.prisma.passwordResetToken.deleteMany({
      where: {
        expiresAt: {
          lt: new Date(),
        },
      },
    });
  }
}
