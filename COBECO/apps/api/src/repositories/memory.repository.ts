import { randomUUID } from 'crypto';
import { verify as verifyHash } from 'argon2';
import {
  ListItemRecord,
  ListRepositoryContract,
  PasswordResetTokenRecord,
  PasswordResetTokenRepositoryContract,
  ProductListRecord,
  SharedListRecord,
  RetailerRecord,
  RetailerRepositoryContract,
  TestimonialRecord,
  TestimonialRepositoryContract,
  UserCreateData,
  UserRecord,
  UserRepositoryContract,
  QuotationItemRecord,
  QuotationRecord,
  QuotationRepositoryContract,
  PaginatedResult,
  CatalogRepositoryContract,
  CategoryRecord,
  SupplierRecord,
  CatalogProductRecord,
  CatalogOfferRecord,
} from './repository.contracts';
import { NormalizedPriceResult } from '../integrations/price-provider';

function cloneItem(item: ListItemRecord): ListItemRecord {
  return { ...item };
}

function cloneList(list: ProductListRecord): ProductListRecord {
  return { ...list, items: list.items.map(cloneItem) };
}

function cloneQuotationResult(result: NormalizedPriceResult): NormalizedPriceResult {
  return {
    ...result,
    fetchedAt: new Date(result.fetchedAt),
    incompleteFields: [...result.incompleteFields],
  };
}

function cloneQuotation(record: QuotationRecord): QuotationRecord {
  return {
    ...record,
    requestedAt: new Date(record.requestedAt),
    items: record.items.map((item) => ({
      ...item,
      results: item.results.map(cloneQuotationResult),
      providers: item.providers.map((provider) => ({ ...provider })),
      highlights: {
        lowestPriceIds: [...item.highlights.lowestPriceIds],
        fastestDeliveryIds: [...item.highlights.fastestDeliveryIds],
        bestValueIds: [...item.highlights.bestValueIds],
      },
    })),
    groups: record.groups?.map((group) => ({
      ...group,
      supplierIds: [...group.supplierIds],
      supplierNames: [...group.supplierNames],
      availableItems: [...group.availableItems],
      missingItems: [...group.missingItems],
      supplierBudgets: group.supplierBudgets.map((budget) => ({ ...budget })),
    })),
    meta: record.meta ? { ...record.meta } : undefined,
  };
}

export class MemoryUserRepository implements UserRepositoryContract {
  private readonly users = new Map<string, UserRecord>();

  async create(data: UserCreateData): Promise<UserRecord> {
    const now = new Date();
    const user: UserRecord = {
      id: randomUUID(),
      ...data,
      consentedAt: now,
      createdAt: now,
      updatedAt: now,
      deletedAt: null,
    };
    this.users.set(user.id, user);
    return { ...user };
  }

  async findByEmail(email: string): Promise<UserRecord | null> {
    const normalizedEmail = email.trim().toLowerCase();
    const user = [...this.users.values()].find((candidate) => candidate.email === normalizedEmail);
    return user ? { ...user } : null;
  }

  async findByUsername(username: string): Promise<UserRecord | null> {
    const normalized = username.trim().toLowerCase();
    const user = [...this.users.values()].find((candidate) => candidate.username === normalized);
    return user ? { ...user } : null;
  }

  async findByEmailOrUsername(identifier: string): Promise<UserRecord | null> {
    const normalized = identifier.trim().toLowerCase();
    const user = [...this.users.values()].find(
      (candidate) => candidate.email === normalized || candidate.username === normalized
    );
    return user ? { ...user } : null;
  }

  async findById(id: string): Promise<UserRecord | null> {
    const user = this.users.get(id);
    return user ? { ...user } : null;
  }

  async updatePassword(id: string, passwordHash: string): Promise<UserRecord> {
    const user = this.requireUser(id);
    user.passwordHash = passwordHash;
    user.updatedAt = new Date();
    return { ...user };
  }

  async softDelete(id: string): Promise<UserRecord> {
    const user = this.requireUser(id);
    user.deletedAt = new Date();
    user.updatedAt = new Date();
    return { ...user };
  }

  async updateConsent(id: string): Promise<UserRecord> {
    const user = this.requireUser(id);
    user.consentedAt = new Date();
    user.updatedAt = new Date();
    return { ...user };
  }

  private requireUser(id: string): UserRecord {
    const user = this.users.get(id);
    if (!user) throw new Error(`User ${id} not found`);
    return user;
  }
}

export class MemoryPasswordResetTokenRepository implements PasswordResetTokenRepositoryContract {
  private readonly tokens = new Map<string, PasswordResetTokenRecord>();

  async create(data: {
    userId: string;
    tokenHash: string;
    expiresAt: Date;
  }): Promise<PasswordResetTokenRecord> {
    const token: PasswordResetTokenRecord = {
      id: randomUUID(),
      ...data,
      usedAt: null,
      createdAt: new Date(),
    };
    this.tokens.set(token.id, token);
    return { ...token };
  }

  async findByToken(token: string): Promise<PasswordResetTokenRecord | null> {
    for (const record of this.tokens.values()) {
      if (
        !record.usedAt &&
        record.expiresAt >= new Date() &&
        (await verifyHash(record.tokenHash, token))
      ) {
        return { ...record };
      }
    }
    return null;
  }

  async markAsUsed(id: string): Promise<PasswordResetTokenRecord> {
    const record = this.tokens.get(id);
    if (!record) throw new Error(`Token ${id} not found`);
    record.usedAt = new Date();
    return { ...record };
  }

  async deleteExpired(): Promise<{ count: number }> {
    const expired = [...this.tokens.values()].filter((token) => token.expiresAt < new Date());
    expired.forEach((token) => this.tokens.delete(token.id));
    return { count: expired.length };
  }
}

export class MemoryTestimonialRepository implements TestimonialRepositoryContract {
  private readonly testimonials: TestimonialRecord[] = [
    {
      id: 'testimonial-1',
      authorName: 'Mariana Souza',
      content: 'Montei minha lista em poucos minutos e encontrei uma oferta melhor.',
      approved: true,
      createdAt: new Date('2026-01-10'),
    },
    {
      id: 'testimonial-2',
      authorName: 'Rafael Lima',
      content: 'A comparação por preço e prazo deixou minha pesquisa muito mais simples.',
      approved: true,
      createdAt: new Date('2026-01-08'),
    },
  ];

  async findApproved(): Promise<TestimonialRecord[]> {
    return this.testimonials
      .filter((testimonial) => testimonial.approved)
      .map((testimonial) => ({ ...testimonial }));
  }

  async create(data: {
    userId: string;
    authorName: string;
    content: string;
  }): Promise<TestimonialRecord> {
    const testimonial: TestimonialRecord = {
      id: randomUUID(),
      ...data,
      approved: false,
      createdAt: new Date(),
    };
    this.testimonials.push(testimonial);
    return { ...testimonial };
  }
}

export class MemoryRetailerRepository implements RetailerRepositoryContract {
  private readonly retailers: RetailerRecord[] = [
    {
      id: 'retailer-amazon',
      name: 'Amazon',
      slug: 'amazon',
      websiteUrl: 'https://www.amazon.com.br',
    },
    {
      id: 'retailer-mercado-livre',
      name: 'Mercado Livre',
      slug: 'mercado-livre',
      websiteUrl: 'https://www.mercadolivre.com.br',
    },
    { id: 'retailer-shopee', name: 'Shopee', slug: 'shopee', websiteUrl: 'https://shopee.com.br' },
  ];

  async findAll(): Promise<RetailerRecord[]> {
    return this.retailers.map((retailer) => ({ ...retailer }));
  }
}

export class MemoryListRepository implements ListRepositoryContract {
  private readonly lists = new Map<string, ProductListRecord & { deletedAt: Date | null }>();
  private readonly shares = new Map<
    string,
    { token: string; userId: string; listId: string; createdAt: Date }
  >();

  async findManyByUserId(userId: string): Promise<ProductListRecord[]> {
    return [...this.lists.values()]
      .filter((list) => list.userId === userId && !list.deletedAt)
      .sort((a, b) => b.updatedAt.getTime() - a.updatedAt.getTime())
      .map(cloneList);
  }

  async findById(userId: string, listId: string): Promise<ProductListRecord | null> {
    const list = this.lists.get(listId);
    return list && list.userId === userId && !list.deletedAt ? cloneList(list) : null;
  }

  async create(
    userId: string,
    name: string,
    categoryId: string | null = null
  ): Promise<ProductListRecord> {
    const now = new Date();
    const list = {
      id: randomUUID(),
      userId,
      name,
      categoryId,
      createdAt: now,
      updatedAt: now,
      deletedAt: null,
      items: [],
    };
    this.lists.set(list.id, list);
    return cloneList(list);
  }

  async update(userId: string, listId: string, name: string): Promise<ProductListRecord> {
    const list = this.requireList(userId, listId);
    list.name = name;
    list.updatedAt = new Date();
    return cloneList(list);
  }

  async delete(userId: string, listId: string): Promise<void> {
    // Exclusão lógica (RF09), espelhando o repositório Prisma.
    const list = this.requireList(userId, listId);
    list.deletedAt = new Date();
    for (const [token, share] of this.shares) {
      if (share.listId === listId) this.shares.delete(token);
    }
  }

  async duplicate(userId: string, listId: string, name: string): Promise<ProductListRecord> {
    const source = this.requireList(userId, listId);
    const now = new Date();
    const duplicate = {
      id: randomUUID(),
      userId,
      name,
      categoryId: source.categoryId,
      createdAt: now,
      updatedAt: now,
      deletedAt: null,
      items: source.items.map((item) => ({ ...item, id: randomUUID(), listId: '' })),
    };
    duplicate.items.forEach((item) => (item.listId = duplicate.id));
    this.lists.set(duplicate.id, duplicate);
    return cloneList(duplicate);
  }

  async createItem(
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
    const list = this.requireList(userId, listId);
    list.items.push(
      ...items.map((item) => ({
        id: randomUUID(),
        listId,
        description: item.description,
        quantity: item.quantity,
        productId: item.productId || null,
        createdAt: new Date(),
      }))
    );
    list.updatedAt = new Date();
    return cloneList(list);
  }

  async updateItem(
    userId: string,
    listId: string,
    itemId: string,
    description: string,
    quantity: number,
    productId: string | null = null
  ) {
    const list = this.requireList(userId, listId);
    const item = list.items.find((candidate) => candidate.id === itemId);
    if (!item) throw new Error('ITEM_NOT_FOUND');
    item.description = description;
    item.quantity = quantity;
    item.productId = productId;
    list.updatedAt = new Date();
    return cloneList(list);
  }

  async deleteItem(userId: string, listId: string, itemId: string) {
    const list = this.requireList(userId, listId);
    const itemIndex = list.items.findIndex((candidate) => candidate.id === itemId);
    if (itemIndex === -1) throw new Error('ITEM_NOT_FOUND');
    list.items.splice(itemIndex, 1);
    list.updatedAt = new Date();
    return cloneList(list);
  }

  async createShare(userId: string, listId: string): Promise<{ token: string; createdAt: Date }> {
    this.requireList(userId, listId);
    const existing = [...this.shares.values()].find(
      (share) => share.userId === userId && share.listId === listId
    );
    if (existing) return { token: existing.token, createdAt: new Date(existing.createdAt) };
    const share = { token: randomUUID(), userId, listId, createdAt: new Date() };
    this.shares.set(share.token, share);
    return { token: share.token, createdAt: new Date(share.createdAt) };
  }

  async revokeShare(userId: string, listId: string): Promise<void> {
    this.requireList(userId, listId);
    for (const [token, share] of this.shares) {
      if (share.userId === userId && share.listId === listId) this.shares.delete(token);
    }
  }

  async findSharedList(token: string): Promise<SharedListRecord | null> {
    const share = this.shares.get(token);
    if (!share) return null;
    const list = this.lists.get(share.listId);
    if (!list || list.userId !== share.userId || list.deletedAt) return null;
    return {
      id: list.id,
      name: list.name,
      createdAt: new Date(list.createdAt),
      updatedAt: new Date(list.updatedAt),
      items: list.items.map(cloneItem),
    };
  }

  private requireList(userId: string, listId: string) {
    const list = this.lists.get(listId);
    if (!list || list.userId !== userId || list.deletedAt) throw new Error('LIST_NOT_FOUND');
    return list;
  }
}

export class MemoryQuotationRepository implements QuotationRepositoryContract {
  private readonly quotations = new Map<string, QuotationRecord>();

  async create(data: {
    userId: string;
    listId: string | null;
    listName: string | null;
    mode: 'item' | 'list';
    requestedAt: Date;
    items?: QuotationItemRecord[];
    groups?: QuotationRecord['groups'];
    bestGroupId?: string | null;
    meta?: QuotationRecord['meta'];
  }): Promise<QuotationRecord> {
    const quotation: QuotationRecord = {
      id: randomUUID(),
      ...data,
      requestedAt: new Date(data.requestedAt),
      status: 'pending',
      items: data.items || [],
      groups: data.groups,
      bestGroupId: data.bestGroupId,
      meta: data.meta,
    };
    this.quotations.set(quotation.id, quotation);
    return cloneQuotation(quotation);
  }

  async complete(
    userId: string,
    quotationId: string,
    items: QuotationItemRecord[]
  ): Promise<QuotationRecord> {
    const quotation = this.requireOwned(userId, quotationId);
    quotation.status = 'completed';
    quotation.items = items;
    return cloneQuotation(quotation);
  }

  async completeParity(
    userId: string,
    quotationId: string,
    groups: NonNullable<QuotationRecord['groups']>,
    bestGroupId: string | null,
    meta: NonNullable<QuotationRecord['meta']>
  ): Promise<QuotationRecord> {
    const quotation = this.requireOwned(userId, quotationId);
    quotation.status = 'completed';
    quotation.groups = groups;
    quotation.bestGroupId = bestGroupId;
    quotation.meta = meta;
    return cloneQuotation(quotation);
  }

  async fail(userId: string, quotationId: string): Promise<QuotationRecord> {
    const quotation = this.requireOwned(userId, quotationId);
    quotation.status = 'failed';
    return cloneQuotation(quotation);
  }

  async findManyByUserId(
    userId: string,
    page: number,
    pageSize: number
  ): Promise<PaginatedResult<QuotationRecord>> {
    const all = [...this.quotations.values()]
      .filter((quotation) => quotation.userId === userId)
      .sort((left, right) => right.requestedAt.getTime() - left.requestedAt.getTime());
    const total = all.length;
    const totalPages = Math.max(1, Math.ceil(total / pageSize));
    return {
      items: all.slice((page - 1) * pageSize, page * pageSize).map(cloneQuotation),
      total,
      page,
      pageSize,
      totalPages,
    };
  }

  async findById(userId: string, quotationId: string): Promise<QuotationRecord | null> {
    const quotation = this.quotations.get(quotationId);
    return quotation && quotation.userId === userId ? cloneQuotation(quotation) : null;
  }

  async delete(userId: string, quotationId: string): Promise<void> {
    this.requireOwned(userId, quotationId);
    this.quotations.delete(quotationId);
  }

  private requireOwned(userId: string, quotationId: string): QuotationRecord {
    const quotation = this.quotations.get(quotationId);
    if (!quotation || quotation.userId !== userId) throw new Error('QUOTATION_NOT_FOUND');
    return quotation;
  }
}

export class MemoryCatalogRepository implements CatalogRepositoryContract {
  private readonly category: CategoryRecord = { id: 'supermercado', name: 'Supermercado' };
  private readonly products: CatalogProductRecord[] = Array.from({ length: 10 }, (_, index) => ({
    id: `product-${index + 1}`,
    name: index === 9 ? 'Produto sem oferta' : `Produto ${index + 1}`,
    categoryId: this.category.id,
    unit: 'unidade',
    active: true,
  }));
  private readonly suppliers: SupplierRecord[] = 'ABCDEFGH'.split('').map((letter) => ({
    id: `supplier-${letter.toLowerCase()}`,
    name: `Fornecedor ${letter}`,
    categoryId: this.category.id,
    active: true,
  }));
  private readonly offers: CatalogOfferRecord[];

  constructor() {
    const coverage: Record<string, number[]> = {
      a: [1, 2, 3, 4, 5, 6, 7, 8, 9],
      b: [1, 2, 3, 4, 5, 6, 7, 8, 9],
      c: [1, 2, 3, 4, 5, 6, 8, 9],
      d: [1, 2, 4, 5, 8, 9],
      e: [1, 2, 3, 4, 5, 6, 8, 9],
      f: [1, 2, 3, 4, 5, 6, 8, 9],
      g: [1, 3, 4, 5, 8, 9],
      h: [1, 2, 3, 4, 5, 6, 8, 9],
    };
    this.offers = Object.entries(coverage).flatMap(([letter, productNumbers], supplierIndex) =>
      productNumbers.map((number) => ({
        supplierId: `supplier-${letter}`,
        productId: `product-${number}`,
        price: 5 + number + supplierIndex,
        active: true,
      }))
    );
    this.offers.push({
      supplierId: 'supplier-h',
      productId: 'product-10',
      price: 99,
      active: false,
    });
  }

  async findCategories() {
    return [{ ...this.category }];
  }
  async findSuppliersByCategory(categoryId: string) {
    return this.suppliers
      .filter((supplier) => supplier.categoryId === categoryId && supplier.active)
      .map((supplier) => ({ ...supplier }));
  }
  async findProductsByCategory(categoryId: string) {
    return this.products
      .filter((product) => product.categoryId === categoryId && product.active)
      .map((product) => ({ ...product }));
  }
  async findOffers(categoryId: string, supplierIds: string[]) {
    const productIds = new Set(
      this.products
        .filter((product) => product.categoryId === categoryId)
        .map((product) => product.id)
    );
    return this.offers
      .filter((offer) => supplierIds.includes(offer.supplierId) && productIds.has(offer.productId))
      .map((offer) => ({ ...offer }));
  }
}
