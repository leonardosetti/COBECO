import { AppError } from '../types';
import { ListRepositoryContract } from '../repositories/repository.contracts';

export class ListService {
  constructor(private readonly listRepository: ListRepositoryContract) {}

  list(userId: string) {
    return this.listRepository.findManyByUserId(userId);
  }

  create(userId: string, name: string, categoryId?: string | null) {
    return this.listRepository.create(userId, name.trim(), categoryId);
  }

  update(userId: string, listId: string, name: string) {
    return this.runRepositoryAction(() => this.listRepository.update(userId, listId, name.trim()));
  }

  async remove(userId: string, listId: string) {
    await this.runRepositoryAction(() => this.listRepository.delete(userId, listId));
    return { message: 'Lista excluída com sucesso' };
  }

  duplicate(userId: string, listId: string, name: string) {
    return this.runRepositoryAction(() =>
      this.listRepository.duplicate(userId, listId, name.trim())
    );
  }

  addItem(
    userId: string,
    listId: string,
    description: string,
    quantity: number,
    productId?: string | null
  ) {
    return this.runRepositoryAction(() =>
      this.listRepository.createItem(userId, listId, description.trim(), quantity, productId)
    );
  }

  addItems(
    userId: string,
    listId: string,
    items: Array<{ description: string; quantity: number; productId?: string | null }>
  ) {
    return this.runRepositoryAction(() =>
      this.listRepository.createItems(
        userId,
        listId,
        items.map((item) => ({ ...item, description: item.description.trim() }))
      )
    );
  }

  updateItem(
    userId: string,
    listId: string,
    itemId: string,
    description: string,
    quantity: number,
    productId?: string | null
  ) {
    return this.runRepositoryAction(() =>
      this.listRepository.updateItem(
        userId,
        listId,
        itemId,
        description.trim(),
        quantity,
        productId
      )
    );
  }

  removeItem(userId: string, listId: string, itemId: string) {
    return this.runRepositoryAction(() => this.listRepository.deleteItem(userId, listId, itemId));
  }

  private async runRepositoryAction<T>(action: () => Promise<T>): Promise<T> {
    try {
      return await action();
    } catch (error) {
      if (error instanceof Error && error.message === 'LIST_NOT_FOUND') {
        throw new AppError('LIST_NOT_FOUND', 'Lista não encontrada', 404);
      }
      if (error instanceof Error && error.message === 'ITEM_NOT_FOUND') {
        throw new AppError('ITEM_NOT_FOUND', 'Item não encontrado', 404);
      }
      throw error;
    }
  }
}
