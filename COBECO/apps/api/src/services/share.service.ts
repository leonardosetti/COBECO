import { AppError } from '../types';
import { ListRepositoryContract, SharedListRecord } from '../repositories/repository.contracts';

export class ShareService {
  constructor(private readonly listRepository: ListRepositoryContract) {}

  async create(userId: string, listId: string): Promise<{ token: string; urlPath: string }> {
    try {
      const share = await this.listRepository.createShare(userId, listId);
      return { token: share.token, urlPath: `/shared-list/${share.token}` };
    } catch (error) {
      this.mapNotFound(error);
      throw error;
    }
  }

  async revoke(userId: string, listId: string): Promise<{ message: string }> {
    try {
      await this.listRepository.revokeShare(userId, listId);
      return { message: 'Compartilhamento revogado com sucesso' };
    } catch (error) {
      this.mapNotFound(error);
      throw error;
    }
  }

  async getSharedList(token: string): Promise<SharedListRecord> {
    const list = await this.listRepository.findSharedList(token);
    if (!list) throw new AppError('SHARED_LIST_NOT_FOUND', 'Link de compartilhamento inválido ou expirado', 404);
    return list;
  }

  private mapNotFound(error: unknown): void {
    if (error instanceof Error && error.message === 'LIST_NOT_FOUND') {
      throw new AppError('LIST_NOT_FOUND', 'Lista não encontrada', 404);
    }
  }
}
