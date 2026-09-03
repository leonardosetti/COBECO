import { AppError } from '../types';
import { PriceIntegrationService } from '../integrations/price.service';
import {
  NormalizedPriceResult,
  PriceSearchResponse,
  ProviderSearchStatus,
} from '../integrations/price-provider';
import {
  ListRepositoryContract,
  PaginatedResult,
  ProductListRecord,
  QuotationItemRecord,
  QuotationRecord,
  QuotationRepositoryContract,
} from '../repositories/repository.contracts';
import { CatalogRepositoryContract } from '../repositories/repository.contracts';
import { calculateAvailability, RequestedItem } from '../domain/availability';
import { groupByCoverageProfile } from '../domain/grouping';
import { calculateGroupBudgets, GroupBudget, selectBestGroup } from '../domain/budget';
import { MAX_SUPPLIERS, MIN_SUPPLIERS } from '../validators/quotation.validator';

export interface QuotationHighlights {
  lowestPriceIds: string[];
  fastestDeliveryIds: string[];
  bestValueIds: string[];
}

export interface QuotationItem {
  itemId: string | null;
  description: string;
  quantity: number;
  results: NormalizedPriceResult[];
  providers: ProviderSearchStatus[];
  highlights: QuotationHighlights;
}

export interface QuotationResponse {
  quotationId: string | null;
  mode: 'item' | 'list';
  listId: string | null;
  listName: string | null;
  requestedAt: string;
  items: QuotationItem[];
  groups?: GroupBudget[];
  bestGroupId?: string | null;
  meta?: {
    totalItems: number;
    selectedSuppliers: number;
    items?: Array<{ id: string; description: string; quantity: number }>;
  };
}

export interface QuotationHistorySummary {
  id: string;
  mode: 'item' | 'list';
  listId: string | null;
  listName: string | null;
  requestedAt: string;
  status: 'pending' | 'completed' | 'failed';
  itemCount: number;
  descriptions: string[];
}

export type PaginatedQuotationHistory = PaginatedResult<QuotationHistorySummary>;

export interface QuotationComparisonItem {
  description: string;
  first: { quotationId: string; requestedAt: string; results: NormalizedPriceResult[] };
  second: { quotationId: string; requestedAt: string; results: NormalizedPriceResult[] };
}

export interface QuotationComparisonResponse {
  first: QuotationHistorySummary;
  second: QuotationHistorySummary;
  items: QuotationComparisonItem[];
}

/** RF12: disponibilidade de cada fornecedor perante os itens de uma lista. */
export interface SupplierAvailabilitySummary {
  id: string;
  name: string;
  availableItems: number;
  totalItems: number;
  /** Percentual de 0 a 100, com duas casas. */
  availability: number;
}

export class QuotationService {
  constructor(
    private readonly priceService: PriceIntegrationService,
    private readonly listRepository: ListRepositoryContract,
    private readonly quotationRepository?: QuotationRepositoryContract,
    private readonly catalogRepository?: CatalogRepositoryContract
  ) {}

  async quoteItem(userId: string, description: string): Promise<QuotationResponse> {
    const query = description.trim();
    if (!query) throw new AppError('VALIDATION_ERROR', 'Informe um produto para cotar', 400);
    const quotation = await this.startQuotation(userId, 'item', null, null, [
      emptyQuotationItem(null, query, 1),
    ]);
    try {
      const search = await this.priceService.search(query);
      const response = this.toResponse(
        'item',
        null,
        null,
        [{ itemId: null, description: query, quantity: 1, search }],
        quotation?.id || null
      );
      await this.completeQuotation(userId, quotation, response);
      return response;
    } catch (error) {
      await this.failQuotation(userId, quotation);
      throw error;
    }
  }

  /**
   * `supplierIds` só governa o caminho de catálogo (RF11); a cotação por
   * provedores externos não tem fornecedores para selecionar.
   */
  async quoteList(
    userId: string,
    listId: string,
    supplierIds: string[] = []
  ): Promise<QuotationResponse> {
    const list = await this.listRepository.findById(userId, listId);
    if (!list) throw new AppError('LIST_NOT_FOUND', 'Lista não encontrada', 404);
    if (!list.items.length)
      throw new AppError('EMPTY_LIST', 'Adicione ao menos um produto antes de cotar', 400);

    if (this.catalogRepository) {
      return this.quoteListFromCatalog(userId, list, supplierIds);
    }

    const quotation = await this.startQuotation(
      userId,
      'list',
      list.id,
      list.name,
      list.items.map((item) => emptyQuotationItem(item.id, item.description, item.quantity))
    );
    try {
      const searches = await Promise.all(
        list.items.map(async (item) => ({
          itemId: item.id,
          description: item.description,
          quantity: item.quantity,
          search: await this.priceService.search(item.description, { allowEmpty: true }),
        }))
      );
      const response = this.toResponse('list', list.id, list.name, searches, quotation?.id || null);
      await this.completeQuotation(userId, quotation, response);
      return response;
    } catch (error) {
      await this.failQuotation(userId, quotation);
      throw error;
    }
  }

  /**
   * RF12: quantos itens da lista cada fornecedor da categoria consegue atender.
   * Alimenta a tela de seleção antes de o orçamento ser calculado.
   */
  async listSupplierAvailability(
    userId: string,
    listId: string
  ): Promise<SupplierAvailabilitySummary[]> {
    const list = await this.listRepository.findById(userId, listId);
    if (!list) throw new AppError('LIST_NOT_FOUND', 'Lista não encontrada', 404);
    if (!this.catalogRepository)
      throw new AppError('CATALOG_UNAVAILABLE', 'Catálogo indisponível', 503);

    const { categoryId, suppliers, requestedItems } = await this.resolveCatalogContext(list);
    const offers = await this.catalogRepository.findOffers(
      categoryId,
      suppliers.map((supplier) => supplier.id)
    );
    const totalItems = requestedItems.length;

    return calculateAvailability(requestedItems, suppliers, offers)
      .map(({ supplier, availableItems }) => ({
        id: supplier.id,
        name: supplier.name,
        availableItems: availableItems.length,
        totalItems,
        availability:
          totalItems === 0
            ? 0
            : Math.round((availableItems.length / totalItems) * 10_000) / 100,
      }))
      // RF11: ordenação alfabética é o padrão da tela de seleção.
      .sort((left, right) => left.name.localeCompare(right.name, 'pt-BR'));
  }

  /**
   * Categoria, fornecedores ativos e itens da lista já resolvidos contra o
   * catálogo — compartilhado pela seleção (RF12) e pelo cálculo (RF13).
   */
  private async resolveCatalogContext(list: ProductListRecord): Promise<{
    categoryId: string;
    suppliers: Awaited<ReturnType<CatalogRepositoryContract['findSuppliersByCategory']>>;
    requestedItems: RequestedItem[];
  }> {
    const catalogRepository = this.catalogRepository;
    if (!catalogRepository) throw new AppError('CATALOG_UNAVAILABLE', 'Catálogo indisponível', 503);
    const categories = await catalogRepository.findCategories();
    const categoryId = list.categoryId || categories[0]?.id;
    if (!categoryId) throw new AppError('CATEGORY_NOT_FOUND', 'Nenhuma categoria cadastrada', 404);

    const [suppliers, products] = await Promise.all([
      catalogRepository.findSuppliersByCategory(categoryId),
      catalogRepository.findProductsByCategory(categoryId),
    ]);
    const productsByName = new Map(
      products.map((product) => [normalizeDescription(product.name), product.id])
    );

    return {
      categoryId,
      suppliers,
      requestedItems: list.items.map((item) => ({
        id: item.id,
        productId:
          item.productId || productsByName.get(normalizeDescription(item.description)) || null,
        description: item.description,
        quantity: item.quantity,
      })),
    };
  }

  private async quoteListFromCatalog(
    userId: string,
    list: ProductListRecord,
    supplierIds: string[]
  ): Promise<QuotationResponse> {
    const catalogRepository = this.catalogRepository;
    if (!catalogRepository) throw new AppError('CATALOG_UNAVAILABLE', 'Catálogo indisponível', 503);

    // RF11 é validado aqui, e não só no schema da rota, para que a regra valha
    // para qualquer chamador do serviço (§4.1 do refinamento v2.1).
    const uniqueIds = [...new Set(supplierIds ?? [])];
    if (uniqueIds.length < MIN_SUPPLIERS) {
      throw new AppError(
        'SUPPLIERS_REQUIRED',
        `Selecione ao menos ${MIN_SUPPLIERS} fornecedores para comparar`,
        400
      );
    }
    if (uniqueIds.length > MAX_SUPPLIERS) {
      throw new AppError(
        'TOO_MANY_SUPPLIERS',
        `Selecione no máximo ${MAX_SUPPLIERS} fornecedores por comparação`,
        400
      );
    }

    const { categoryId, suppliers: allSuppliers, requestedItems } =
      await this.resolveCatalogContext(list);
    const selected = allSuppliers.filter((supplier) => uniqueIds.includes(supplier.id));
    if (uniqueIds.some((id) => !selected.some((supplier) => supplier.id === id))) {
      throw new AppError(
        'INVALID_SUPPLIER',
        'A seleção contém fornecedor inválido para a categoria',
        400
      );
    }

    const offers = await catalogRepository.findOffers(
      categoryId,
      selected.map((supplier) => supplier.id)
    );
    const groups = calculateGroupBudgets(
      groupByCoverageProfile(
        calculateAvailability(requestedItems, selected, offers),
        requestedItems.length
      )
    );
    const bestGroupId = selectBestGroup(groups);
    const meta = {
      totalItems: requestedItems.length,
      selectedSuppliers: selected.length,
      items: requestedItems.map(({ id, description, quantity }) => ({ id, description, quantity })),
    };
    const itemRecords = list.items.map((item) =>
      emptyQuotationItem(item.id, item.description, item.quantity)
    );
    const quotation = await this.startQuotation(userId, 'list', list.id, list.name, itemRecords);
    if (quotation && this.quotationRepository) {
      await this.quotationRepository.completeParity(
        userId,
        quotation.id,
        groups,
        bestGroupId,
        meta
      );
    }
    return {
      quotationId: quotation?.id || null,
      mode: 'list',
      listId: list.id,
      listName: list.name,
      requestedAt: new Date().toISOString(),
      items: itemRecords,
      groups,
      bestGroupId,
      meta,
    };
  }

  async listHistory(userId: string, page = 1, pageSize = 20): Promise<PaginatedQuotationHistory> {
    if (!this.quotationRepository) return { items: [], total: 0, page, pageSize, totalPages: 1 };
    const result = await this.quotationRepository.findManyByUserId(userId, page, pageSize);
    return { ...result, items: result.items.map(toHistorySummary) };
  }

  async getHistory(userId: string, quotationId: string): Promise<QuotationResponse> {
    const quotation = await this.requireQuotation(userId, quotationId);
    return this.fromRecord(quotation);
  }

  async deleteHistory(userId: string, quotationId: string): Promise<{ message: string }> {
    if (!this.quotationRepository)
      throw new AppError('QUOTATION_NOT_FOUND', 'Cotação não encontrada', 404);
    try {
      await this.quotationRepository.delete(userId, quotationId);
    } catch (error) {
      if (error instanceof Error && error.message === 'QUOTATION_NOT_FOUND') {
        throw new AppError('QUOTATION_NOT_FOUND', 'Cotação não encontrada', 404);
      }
      throw error;
    }
    return { message: 'Cotação excluída com sucesso' };
  }

  async compareHistory(
    userId: string,
    firstId: string,
    secondId: string
  ): Promise<QuotationComparisonResponse> {
    const first = await this.requireQuotation(userId, firstId);
    const second = await this.requireQuotation(userId, secondId);
    const firstByDescription = new Map(
      first.items.map((item) => [normalizeDescription(item.description), item])
    );
    const items = second.items.flatMap((secondItem) => {
      const firstItem = firstByDescription.get(normalizeDescription(secondItem.description));
      if (!firstItem) return [];
      return [
        {
          description: secondItem.description,
          first: {
            quotationId: first.id,
            requestedAt: first.requestedAt.toISOString(),
            results: firstItem.results,
          },
          second: {
            quotationId: second.id,
            requestedAt: second.requestedAt.toISOString(),
            results: secondItem.results,
          },
        },
      ];
    });
    if (!items.length)
      throw new AppError('NO_COMMON_PRODUCT', 'As cotações não possuem produtos em comum', 400);
    return { first: toHistorySummary(first), second: toHistorySummary(second), items };
  }

  private toResponse(
    mode: 'item' | 'list',
    listId: string | null,
    listName: string | null,
    items: Array<{
      itemId: string | null;
      description: string;
      quantity: number;
      search: PriceSearchResponse;
    }>,
    quotationId: string | null
  ): QuotationResponse {
    return {
      quotationId,
      mode,
      listId,
      listName,
      requestedAt: new Date().toISOString(),
      items: items.map(({ itemId, description, quantity, search }) => ({
        itemId,
        description,
        quantity,
        results: search.results,
        providers: search.providers,
        highlights: buildHighlights(search.results),
      })),
    };
  }

  private async startQuotation(
    userId: string,
    mode: 'item' | 'list',
    listId: string | null,
    listName: string | null,
    items: QuotationItemRecord[]
  ): Promise<QuotationRecord | null> {
    if (!this.quotationRepository) return null;
    return this.quotationRepository.create({
      userId,
      listId,
      listName,
      mode,
      requestedAt: new Date(),
      items,
    });
  }

  private async completeQuotation(
    userId: string,
    quotation: QuotationRecord | null,
    response: QuotationResponse
  ): Promise<void> {
    if (quotation && this.quotationRepository)
      await this.quotationRepository.complete(userId, quotation.id, response.items);
  }

  private async failQuotation(userId: string, quotation: QuotationRecord | null): Promise<void> {
    if (quotation && this.quotationRepository)
      await this.quotationRepository.fail(userId, quotation.id);
  }

  private async requireQuotation(userId: string, quotationId: string): Promise<QuotationRecord> {
    if (!this.quotationRepository)
      throw new AppError('QUOTATION_NOT_FOUND', 'Cotação não encontrada', 404);
    const quotation = await this.quotationRepository.findById(userId, quotationId);
    if (!quotation) throw new AppError('QUOTATION_NOT_FOUND', 'Cotação não encontrada', 404);
    return quotation;
  }

  private fromRecord(record: QuotationRecord): QuotationResponse {
    return {
      quotationId: record.id,
      mode: record.mode,
      listId: record.listId,
      listName: record.listName,
      requestedAt: record.requestedAt.toISOString(),
      items: record.items,
      groups: record.groups,
      bestGroupId: record.bestGroupId,
      meta: record.meta,
    };
  }
}

function normalizeDescription(description: string): string {
  return description.trim().toLocaleLowerCase('pt-BR').replace(/\s+/g, ' ');
}

function toHistorySummary(record: QuotationRecord): QuotationHistorySummary {
  return {
    id: record.id,
    mode: record.mode,
    listId: record.listId,
    listName: record.listName,
    requestedAt: record.requestedAt.toISOString(),
    status: record.status,
    itemCount: record.items.length,
    descriptions: record.items.map((item) => item.description),
  };
}

function emptyQuotationItem(
  itemId: string | null,
  description: string,
  quantity: number
): QuotationItemRecord {
  return {
    itemId,
    description,
    quantity,
    results: [],
    providers: [],
    highlights: { lowestPriceIds: [], fastestDeliveryIds: [], bestValueIds: [] },
  };
}

function buildHighlights(results: NormalizedPriceResult[]): QuotationHighlights {
  return {
    lowestPriceIds: pickLowestByCurrency(results, (result) => result.price),
    fastestDeliveryIds: pickLowest(results, (result) => result.deliveryDays),
    bestValueIds: pickBestValueByCurrency(results),
  };
}

function pickLowestByCurrency(
  results: NormalizedPriceResult[],
  value: (result: NormalizedPriceResult) => number | null
): string[] {
  const byCurrency = new Map<string, NormalizedPriceResult[]>();
  for (const result of results) {
    if (value(result) === null) continue;
    const group = byCurrency.get(result.currency) || [];
    group.push(result);
    byCurrency.set(result.currency, group);
  }
  return [...byCurrency.values()].flatMap((group) => pickLowest(group, value));
}

function pickLowest(
  results: NormalizedPriceResult[],
  value: (result: NormalizedPriceResult) => number | null
): string[] {
  const candidates = results.filter((result) => value(result) !== null);
  if (!candidates.length) return [];
  const minimum = Math.min(...candidates.map((result) => value(result) as number));
  return candidates.filter((result) => value(result) === minimum).map((result) => result.id);
}

function pickBestValueByCurrency(results: NormalizedPriceResult[]): string[] {
  const byCurrency = new Map<string, NormalizedPriceResult[]>();
  for (const result of results) {
    if (result.price === null || result.deliveryDays === null) continue;
    const group = byCurrency.get(result.currency) || [];
    group.push(result);
    byCurrency.set(result.currency, group);
  }

  return [...byCurrency.values()].flatMap((group) => {
    const priceValues = group.map((result) => result.price as number);
    const deliveryValues = group.map((result) => result.deliveryDays as number);
    const minPrice = Math.min(...priceValues);
    const maxPrice = Math.max(...priceValues);
    const minDelivery = Math.min(...deliveryValues);
    const maxDelivery = Math.max(...deliveryValues);
    const score = (result: NormalizedPriceResult) =>
      normalize(result.price as number, minPrice, maxPrice) +
      normalize(result.deliveryDays as number, minDelivery, maxDelivery);
    const best = Math.min(...group.map(score));
    return group.filter((result) => score(result) === best).map((result) => result.id);
  });
}

function normalize(value: number, minimum: number, maximum: number): number {
  return maximum === minimum ? 0 : (value - minimum) / (maximum - minimum);
}
