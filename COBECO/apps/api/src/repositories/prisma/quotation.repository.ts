import { Prisma, PrismaClient } from '@prisma/client';
import {
  PaginatedResult,
  ParityMeta,
  QuotationItemRecord,
  QuotationRecord,
  QuotationRepositoryContract,
} from '../repository.contracts';
import { GroupBudget } from '../../domain/budget';
import { IncompleteField } from '../../integrations/price-provider';

export class PrismaQuotationRepository implements QuotationRepositoryContract {
  constructor(private readonly prisma: PrismaClient) {}

  async create(data: {
    userId: string;
    listId: string | null;
    listName: string | null;
    mode: 'item' | 'list';
    requestedAt: Date;
    items?: QuotationItemRecord[];
    groups?: GroupBudget[];
    bestGroupId?: string | null;
    meta?: ParityMeta;
  }): Promise<QuotationRecord> {
    const created = await this.prisma.quotation.create({
      data: {
        userId: data.userId,
        listId: data.listId,
        listName: data.listName,
        mode: data.mode,
        requestedAt: data.requestedAt,
        status: 'pending',
        parityGroups: toJson(data.groups),
        parityMeta: toJson(data.meta),
        bestGroupId: data.bestGroupId,
      },
    });
    return { ...data, id: created.id, status: 'pending', items: data.items || [] };
  }

  async complete(
    userId: string,
    quotationId: string,
    items: QuotationItemRecord[]
  ): Promise<QuotationRecord> {
    await this.requireOwned(userId, quotationId);
    await this.prisma.$transaction(async (transaction) => {
      await transaction.quotationResult.deleteMany({ where: { quotationId } });
      for (const item of items) {
        for (const result of item.results) {
          await transaction.quotationResult.create({
            data: {
              quotation: { connect: { id: quotationId } },
              ...(item.itemId ? { listItem: { connect: { id: item.itemId } } } : {}),
              productName: result.productName,
              price: result.price,
              currency: result.currency,
              deliveryDays: result.deliveryDays,
              redirectUrl: result.redirectUrl,
              providerSlug: result.providerSlug,
              fetchedAt: result.fetchedAt,
              retailer: {
                connectOrCreate: {
                  where: { slug: result.retailerSlug },
                  create: {
                    name: result.retailerName,
                    slug: result.retailerSlug,
                    websiteUrl: result.redirectUrl,
                  },
                },
              },
            },
          });
        }
      }
      await transaction.quotation.update({
        where: { id: quotationId },
        data: { status: 'completed' },
      });
    });
    return {
      ...(await this.requireOwned(userId, quotationId)),
      status: 'completed' as const,
      items,
    };
  }

  async completeParity(
    userId: string,
    quotationId: string,
    groups: GroupBudget[],
    bestGroupId: string | null,
    meta: ParityMeta
  ) {
    await this.requireOwned(userId, quotationId);
    const quotation = await this.prisma.quotation.update({
      where: { id: quotationId },
      data: {
        status: 'completed',
        parityGroups: toJson(groups),
        parityMeta: toJson(meta),
        bestGroupId,
      },
      include: quotationInclude,
    });
    return mapQuotation(quotation);
  }

  async fail(userId: string, quotationId: string) {
    await this.requireOwned(userId, quotationId);
    return mapQuotation(
      await this.prisma.quotation.update({
        where: { id: quotationId },
        data: { status: 'failed' },
        include: quotationInclude,
      })
    );
  }

  async findManyByUserId(
    userId: string,
    page: number,
    pageSize: number
  ): Promise<PaginatedResult<QuotationRecord>> {
    const [items, total] = await this.prisma.$transaction([
      this.prisma.quotation.findMany({
        where: { userId },
        include: quotationInclude,
        orderBy: { requestedAt: 'desc' },
        skip: (page - 1) * pageSize,
        take: pageSize,
      }),
      this.prisma.quotation.count({ where: { userId } }),
    ]);
    return {
      items: items.map(mapQuotation),
      total,
      page,
      pageSize,
      totalPages: Math.max(1, Math.ceil(total / pageSize)),
    };
  }

  async findById(userId: string, quotationId: string) {
    const value = await this.prisma.quotation.findFirst({
      where: { id: quotationId, userId },
      include: quotationInclude,
    });
    return value ? mapQuotation(value) : null;
  }

  async delete(userId: string, quotationId: string) {
    await this.requireOwned(userId, quotationId);
    await this.prisma.quotation.delete({ where: { id: quotationId } });
  }

  private async requireOwned(userId: string, quotationId: string) {
    const quotation = await this.prisma.quotation.findFirst({
      where: { id: quotationId, userId },
      include: quotationInclude,
    });
    if (!quotation) throw new Error('QUOTATION_NOT_FOUND');
    return mapQuotation(quotation);
  }
}

const quotationInclude = {
  quotationResults: { include: { retailer: true, listItem: true } },
  list: { include: { listItems: { orderBy: { createdAt: 'asc' as const } } } },
} as const;

type QuotationWithRelations = Prisma.QuotationGetPayload<{ include: typeof quotationInclude }>;

function mapQuotation(value: QuotationWithRelations): QuotationRecord {
  const itemMap = new Map<string, QuotationItemRecord>();
  for (const result of value.quotationResults) {
    const key = result.listItemId || result.productName;
    const current: QuotationItemRecord = itemMap.get(key) || {
      itemId: result.listItemId,
      description: result.listItem?.description || result.productName,
      quantity: result.listItem?.quantity || 1,
      results: [],
      providers: [],
      highlights: { lowestPriceIds: [], fastestDeliveryIds: [], bestValueIds: [] },
    };
    const incompleteFields: IncompleteField[] = [];
    if (result.price === null) incompleteFields.push('price');
    if (result.deliveryDays === null) incompleteFields.push('deliveryDays');
    current.results.push({
      id: result.id,
      providerSlug: result.providerSlug,
      retailerName: result.retailer.name,
      retailerSlug: result.retailer.slug,
      productName: result.productName,
      price: result.price,
      currency: result.currency,
      deliveryDays: result.deliveryDays,
      redirectUrl: result.redirectUrl,
      fetchedAt: result.fetchedAt,
      incompleteFields,
    });
    itemMap.set(key, current);
  }
  const meta = value.parityMeta as unknown as ParityMeta | null;
  const persistedItems: Array<{ id: string; description: string; quantity: number }> =
    value.list?.listItems || meta?.items || [];
  return {
    id: value.id,
    userId: value.userId,
    listId: value.listId,
    listName: value.listName,
    mode: value.mode as 'item' | 'list',
    requestedAt: value.requestedAt,
    status: value.status as QuotationRecord['status'],
    items: itemMap.size
      ? [...itemMap.values()]
      : persistedItems.map((item) => ({
          itemId: item.id,
          description: item.description,
          quantity: item.quantity,
          results: [],
          providers: [],
          highlights: { lowestPriceIds: [], fastestDeliveryIds: [], bestValueIds: [] },
        })),
    groups: (value.parityGroups || undefined) as GroupBudget[] | undefined,
    bestGroupId: value.bestGroupId,
    meta: meta || undefined,
  };
}

function toJson(value: unknown): Prisma.InputJsonValue | undefined {
  return value === undefined ? undefined : JSON.parse(JSON.stringify(value));
}
