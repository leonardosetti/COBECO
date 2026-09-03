import { Prisma, PrismaClient } from '@prisma/client';
import {
  ListRepositoryContract,
  ProductListRecord,
  SharedListRecord,
} from '../repository.contracts';

const includeItems = { listItems: { orderBy: { createdAt: 'asc' as const } } };

/** RF09: listas excluídas continuam na tabela, mas somem de toda leitura. */
const notDeleted = { deletedAt: null };

export class PrismaListRepository implements ListRepositoryContract {
  constructor(private readonly prisma: PrismaClient) {}

  async findManyByUserId(userId: string) {
    return (
      await this.prisma.productList.findMany({
        where: { userId, ...notDeleted },
        include: includeItems,
        orderBy: { updatedAt: 'desc' },
      })
    ).map(mapList);
  }

  async findById(userId: string, listId: string) {
    const list = await this.prisma.productList.findFirst({
      where: { id: listId, userId, ...notDeleted },
      include: includeItems,
    });
    return list ? mapList(list) : null;
  }

  async create(userId: string, name: string, categoryId: string | null = null) {
    return mapList(
      await this.prisma.productList.create({
        data: { userId, name, categoryId },
        include: includeItems,
      })
    );
  }

  async update(userId: string, listId: string, name: string) {
    await this.requireOwned(userId, listId);
    return mapList(
      await this.prisma.productList.update({
        where: { id: listId },
        data: { name },
        include: includeItems,
      })
    );
  }

  async delete(userId: string, listId: string) {
    await this.requireOwned(userId, listId);
    // Exclusão lógica (RF09): preserva o histórico de cotações que referencia a
    // lista e permite auditoria posterior.
    await this.prisma.productList.update({
      where: { id: listId },
      data: { deletedAt: new Date() },
    });
    await this.prisma.listShare.deleteMany({ where: { listId } });
  }

  async duplicate(userId: string, listId: string, name: string) {
    const source = await this.requireOwned(userId, listId);
    return mapList(
      await this.prisma.productList.create({
        data: {
          userId,
          name,
          categoryId: source.categoryId,
          listItems: {
            create: source.listItems.map((item) => ({
              description: item.description,
              quantity: item.quantity,
              productId: item.productId,
            })),
          },
        },
        include: includeItems,
      })
    );
  }

  createItem(
    userId: string,
    listId: string,
    description: string,
    quantity: number,
    productId: string | null = null
  ) {
    return this.createItems(userId, listId, [{ description, quantity, productId }]);
  }

  async createItems(
    userId: string,
    listId: string,
    items: Array<{ description: string; quantity: number; productId?: string | null }>
  ) {
    await this.requireOwned(userId, listId);
    await this.prisma.productList.update({
      where: { id: listId },
      data: {
        listItems: {
          create: items.map((item) => ({
            description: item.description,
            quantity: item.quantity,
            productId: item.productId || null,
          })),
        },
      },
    });
    return (await this.findById(userId, listId)) as ProductListRecord;
  }

  async updateItem(
    userId: string,
    listId: string,
    itemId: string,
    description: string,
    quantity: number,
    productId: string | null = null
  ) {
    await this.requireOwned(userId, listId);
    const item = await this.prisma.listItem.findFirst({ where: { id: itemId, listId } });
    if (!item) throw new Error('ITEM_NOT_FOUND');
    await this.prisma.listItem.update({
      where: { id: itemId },
      data: { description, quantity, productId },
    });
    return (await this.findById(userId, listId)) as ProductListRecord;
  }

  async deleteItem(userId: string, listId: string, itemId: string) {
    await this.requireOwned(userId, listId);
    const deleted = await this.prisma.listItem.deleteMany({ where: { id: itemId, listId } });
    if (!deleted.count) throw new Error('ITEM_NOT_FOUND');
    return (await this.findById(userId, listId)) as ProductListRecord;
  }

  async createShare(userId: string, listId: string) {
    await this.requireOwned(userId, listId);
    const existing = await this.prisma.listShare.findFirst({ where: { listId } });
    if (existing) return { token: existing.token, createdAt: existing.createdAt };
    const share = await this.prisma.listShare.create({
      data: { listId, token: crypto.randomUUID() },
    });
    return { token: share.token, createdAt: share.createdAt };
  }

  async revokeShare(userId: string, listId: string) {
    await this.requireOwned(userId, listId);
    await this.prisma.listShare.deleteMany({ where: { listId } });
  }

  async findSharedList(token: string): Promise<SharedListRecord | null> {
    const share = await this.prisma.listShare.findUnique({
      where: { token },
      include: { list: { include: includeItems } },
    });
    if (!share || share.list.deletedAt) return null;
    const list = mapList(share.list);
    return {
      id: list.id,
      name: list.name,
      createdAt: list.createdAt,
      updatedAt: list.updatedAt,
      items: list.items,
    };
  }

  private async requireOwned(userId: string, listId: string) {
    const list = await this.prisma.productList.findFirst({
      where: { id: listId, userId, ...notDeleted },
      include: includeItems,
    });
    if (!list) throw new Error('LIST_NOT_FOUND');
    return list;
  }
}

type ListWithItems = Prisma.ProductListGetPayload<{ include: typeof includeItems }>;

function mapList(list: ListWithItems): ProductListRecord {
  const { listItems, ...record } = list;
  return { ...record, items: listItems };
}
