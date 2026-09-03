export interface UserRecord {
  id: string;
  name: string;
  username: string;
  email: string;
  passwordHash: string;
  consentedAt: Date | null;
  createdAt: Date;
  updatedAt: Date;
  deletedAt: Date | null;
}

export interface UserCreateData {
  name: string;
  username: string;
  email: string;
  passwordHash: string;
}

export interface UserRepositoryContract {
  create(data: UserCreateData): Promise<UserRecord>;
  findByEmail(email: string): Promise<UserRecord | null>;
  findByUsername(username: string): Promise<UserRecord | null>;
  /** RF02: resolve o login tanto por e-mail quanto por username. */
  findByEmailOrUsername(identifier: string): Promise<UserRecord | null>;
  findById(id: string): Promise<UserRecord | null>;
  updatePassword(id: string, passwordHash: string): Promise<UserRecord>;
  softDelete(id: string): Promise<UserRecord>;
  updateConsent(id: string): Promise<UserRecord>;
}

export interface PasswordResetTokenRecord {
  id: string;
  userId: string;
  tokenHash: string;
  expiresAt: Date;
  usedAt: Date | null;
  createdAt: Date;
}

export interface PasswordResetTokenRepositoryContract {
  create(data: {
    userId: string;
    tokenHash: string;
    expiresAt: Date;
  }): Promise<PasswordResetTokenRecord>;
  findByToken(token: string): Promise<PasswordResetTokenRecord | null>;
  markAsUsed(id: string): Promise<PasswordResetTokenRecord>;
  deleteExpired(): Promise<{ count: number }>;
}

export interface TestimonialRecord {
  id: string;
  authorName: string;
  content: string;
  approved: boolean;
  createdAt: Date;
}

export interface RetailerRecord {
  id: string;
  name: string;
  slug: string;
  websiteUrl: string;
}

export interface TestimonialRepositoryContract {
  findApproved(): Promise<TestimonialRecord[]>;
  create(data: { userId: string; authorName: string; content: string }): Promise<TestimonialRecord>;
}

export interface RetailerRepositoryContract {
  findAll(): Promise<RetailerRecord[]>;
}

export interface ListItemRecord {
  id: string;
  listId: string;
  description: string;
  quantity: number;
  productId?: string | null;
  createdAt: Date;
}

export interface ProductListRecord {
  id: string;
  userId: string;
  name: string;
  categoryId?: string | null;
  createdAt: Date;
  updatedAt: Date;
  items: ListItemRecord[];
}

export interface ListRepositoryContract {
  findManyByUserId(userId: string): Promise<ProductListRecord[]>;
  findById(userId: string, listId: string): Promise<ProductListRecord | null>;
  create(userId: string, name: string, categoryId?: string | null): Promise<ProductListRecord>;
  update(userId: string, listId: string, name: string): Promise<ProductListRecord>;
  delete(userId: string, listId: string): Promise<void>;
  duplicate(userId: string, listId: string, name: string): Promise<ProductListRecord>;
  createItem(
    userId: string,
    listId: string,
    description: string,
    quantity: number,
    productId?: string | null
  ): Promise<ProductListRecord>;
  createItems(
    userId: string,
    listId: string,
    items: Array<{ description: string; quantity: number; productId?: string | null }>
  ): Promise<ProductListRecord>;
  updateItem(
    userId: string,
    listId: string,
    itemId: string,
    description: string,
    quantity: number,
    productId?: string | null
  ): Promise<ProductListRecord>;
  deleteItem(userId: string, listId: string, itemId: string): Promise<ProductListRecord>;
  createShare(userId: string, listId: string): Promise<{ token: string; createdAt: Date }>;
  revokeShare(userId: string, listId: string): Promise<void>;
  findSharedList(token: string): Promise<SharedListRecord | null>;
}

export interface SharedListRecord {
  id: string;
  name: string;
  createdAt: Date;
  updatedAt: Date;
  items: ListItemRecord[];
}

export type QuotationStatus = 'pending' | 'completed' | 'failed';

export interface QuotationItemRecord {
  itemId: string | null;
  description: string;
  quantity: number;
  results: NormalizedPriceResult[];
  providers: ProviderSearchStatus[];
  highlights: QuotationHighlights;
}

export interface QuotationRecord {
  id: string;
  userId: string;
  listId: string | null;
  listName: string | null;
  mode: 'item' | 'list';
  requestedAt: Date;
  status: QuotationStatus;
  items: QuotationItemRecord[];
  groups?: import('../domain/budget').GroupBudget[];
  bestGroupId?: string | null;
  meta?: ParityMeta;
}

export interface ParityMeta {
  totalItems: number;
  selectedSuppliers: number;
  items?: Array<{ id: string; description: string; quantity: number }>;
}

export interface PaginatedResult<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

export interface QuotationRepositoryContract {
  create(data: {
    userId: string;
    listId: string | null;
    listName: string | null;
    mode: 'item' | 'list';
    requestedAt: Date;
    items?: QuotationItemRecord[];
    groups?: import('../domain/budget').GroupBudget[];
    bestGroupId?: string | null;
    meta?: ParityMeta;
  }): Promise<QuotationRecord>;
  complete(
    userId: string,
    quotationId: string,
    items: QuotationItemRecord[]
  ): Promise<QuotationRecord>;
  completeParity(
    userId: string,
    quotationId: string,
    groups: import('../domain/budget').GroupBudget[],
    bestGroupId: string | null,
    meta: ParityMeta
  ): Promise<QuotationRecord>;
  fail(userId: string, quotationId: string): Promise<QuotationRecord>;
  findManyByUserId(
    userId: string,
    page: number,
    pageSize: number
  ): Promise<PaginatedResult<QuotationRecord>>;
  findById(userId: string, quotationId: string): Promise<QuotationRecord | null>;
  delete(userId: string, quotationId: string): Promise<void>;
}

export interface CategoryRecord {
  id: string;
  name: string;
}

export interface SupplierRecord {
  id: string;
  name: string;
  categoryId: string;
  active: boolean;
}

export interface CatalogProductRecord {
  id: string;
  name: string;
  categoryId: string;
  unit: string;
  active: boolean;
}

export interface CatalogOfferRecord {
  supplierId: string;
  productId: string;
  price: number;
  active: boolean;
}

export interface CatalogRepositoryContract {
  findCategories(): Promise<CategoryRecord[]>;
  findSuppliersByCategory(categoryId: string): Promise<SupplierRecord[]>;
  findProductsByCategory(categoryId: string): Promise<CatalogProductRecord[]>;
  findOffers(categoryId: string, supplierIds: string[]): Promise<CatalogOfferRecord[]>;
}
import type { NormalizedPriceResult, ProviderSearchStatus } from '../integrations/price-provider';
import type { QuotationHighlights } from '../services/quotation.service';
