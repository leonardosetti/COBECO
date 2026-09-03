import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from 'axios';

type RetriableConfig = InternalAxiosRequestConfig & { _retried?: boolean };

export interface ListItem {
  id: string;
  listId: string;
  description: string;
  quantity: number;
  productId?: string | null;
  createdAt: string;
}

export interface ProductList {
  id: string;
  userId: string;
  name: string;
  categoryId?: string | null;
  createdAt: string;
  updatedAt: string;
  items: ListItem[];
}

export interface SharedList {
  id: string;
  name: string;
  createdAt: string;
  updatedAt: string;
  items: ListItem[];
}

export interface QuotationResult {
  id: string;
  providerSlug: string;
  retailerName: string;
  retailerSlug: string;
  productName: string;
  description?: string;
  price: number | null;
  currency: string;
  deliveryDays: number | null;
  redirectUrl: string;
  fetchedAt: string;
  incompleteFields: Array<'price' | 'deliveryDays'>;
}

export interface ProviderQuotationStatus {
  providerSlug: string;
  providerName: string;
  state: 'success' | 'empty' | 'failed';
  resultCount: number;
  incompleteCount: number;
  errorCode?: string;
  message?: string;
}

export interface QuotationItem {
  itemId: string | null;
  description: string;
  quantity: number;
  results: QuotationResult[];
  providers: ProviderQuotationStatus[];
  highlights: {
    lowestPriceIds: string[];
    fastestDeliveryIds: string[];
    bestValueIds: string[];
  };
}

export interface QuotationResponse {
  quotationId: string | null;
  mode: 'item' | 'list';
  listId: string | null;
  listName: string | null;
  requestedAt: string;
  items: QuotationItem[];
  groups?: QuotationGroup[];
  bestGroupId?: string | null;
  meta?: {
    totalItems: number;
    selectedSuppliers: number;
    items?: Array<{ id: string; description: string; quantity: number }>;
  };
}

export interface Category {
  id: string;
  name: string;
}
export interface Supplier {
  id: string;
  name: string;
  categoryId: string;
  active: boolean;
}
export interface CatalogProduct {
  id: string;
  name: string;
  categoryId: string;
  unit: string;
  active: boolean;
}
/** RF12: quanto da lista cada fornecedor consegue atender. */
export interface SupplierAvailability {
  id: string;
  name: string;
  availableItems: number;
  totalItems: number;
  availability: number;
}
export interface QuotationGroup {
  groupId: string;
  supplierIds: string[];
  supplierNames: string[];
  availableItems: string[];
  missingItems: string[];
  coverage: number;
  total: number;
  supplierBudgets: Array<{ supplierId: string; supplierName: string; total: number }>;
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

export interface PaginatedQuotationHistory {
  items: QuotationHistorySummary[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

export interface QuotationComparisonItem {
  description: string;
  first: { quotationId: string; requestedAt: string; results: QuotationResult[] };
  second: { quotationId: string; requestedAt: string; results: QuotationResult[] };
}

export interface QuotationComparisonResponse {
  first: QuotationHistorySummary;
  second: QuotationHistorySummary;
  items: QuotationComparisonItem[];
}

export interface ApiError {
  code: string;
  message: string;
}

class ApiService {
  private client: AxiosInstance;
  /** Renovação em voo, compartilhada para não disparar N refreshes simultâneos. */
  private refreshInFlight: Promise<string> | null = null;

  constructor() {
    this.client = axios.create({
      baseURL: '/api',
      headers: {
        'Content-Type': 'application/json',
      },
      withCredentials: true,
    });

    // Add request interceptor to include auth token
    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('accessToken');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Em 401, tenta uma renovação silenciosa pelo cookie httpOnly antes de
    // derrubar a sessão. Sem isto o usuário era expulso a cada 15 minutos.
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const original = error.config as RetriableConfig | undefined;
        const isAuthRoute = original?.url?.includes('/auth/');

        if (error.response?.status !== 401 || !original || original._retried || isAuthRoute) {
          if (error.response?.status === 401 && !isAuthRoute) this.forceLogout();
          return Promise.reject(error);
        }

        original._retried = true;

        try {
          const token = await this.refreshSession();
          original.headers.Authorization = `Bearer ${token}`;
          return await this.client(original);
        } catch (refreshError) {
          this.forceLogout();
          return Promise.reject(error);
        }
      }
    );
  }

  /** Troca o cookie de refresh por um novo access token e o persiste. */
  private refreshSession(): Promise<string> {
    if (!this.refreshInFlight) {
      this.refreshInFlight = axios
        .post('/api/auth/refresh', null, { withCredentials: true })
        .then((response) => {
          const token: string = response.data.accessToken;
          localStorage.setItem('accessToken', token);
          if (response.data.user) {
            localStorage.setItem('user', JSON.stringify(response.data.user));
          }
          return token;
        })
        .finally(() => {
          this.refreshInFlight = null;
        });
    }

    return this.refreshInFlight;
  }

  private forceLogout() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('user');
    if (window.location.pathname !== '/login') {
      window.location.href = '/login';
    }
  }

  async getTestimonials() {
    const response = await this.client.get('/public/testimonials');
    return response.data;
  }

  async getRetailers() {
    const response = await this.client.get('/public/retailers');
    return response.data;
  }

  async getLists(): Promise<ProductList[]> {
    const response = await this.client.get('/platform/lists');
    return response.data;
  }

  async shareList(listId: string): Promise<{ token: string; urlPath: string }> {
    const response = await this.client.post(`/platform/lists/${listId}/share`);
    return response.data;
  }

  async revokeListShare(listId: string): Promise<void> {
    await this.client.delete(`/platform/lists/${listId}/share`);
  }

  async getSharedList(token: string): Promise<SharedList> {
    const response = await this.client.get(`/public/shared-lists/${token}`);
    return response.data;
  }

  async submitTestimonial(authorName: string, content: string): Promise<void> {
    await this.client.post('/platform/testimonials', { authorName, content });
  }

  async quoteItem(description: string): Promise<QuotationResponse> {
    const response = await this.client.post('/platform/quotations/item', { description });
    return response.data;
  }

  async quoteList(listId: string, supplierIds: string[]): Promise<QuotationResponse> {
    const response = await this.client.post(`/platform/lists/${listId}/quote`, { supplierIds });
    return response.data;
  }

  async getListSupplierAvailability(listId: string): Promise<SupplierAvailability[]> {
    return (await this.client.get(`/platform/lists/${listId}/suppliers`)).data;
  }

  async getQuotationHistory(page = 1, pageSize = 10): Promise<PaginatedQuotationHistory> {
    const response = await this.client.get('/platform/quotations/history', {
      params: { page, pageSize },
    });
    return response.data;
  }

  async getQuotation(quotationId: string): Promise<QuotationResponse> {
    const response = await this.client.get(`/platform/quotations/${quotationId}`);
    return response.data;
  }

  async deleteQuotation(quotationId: string): Promise<void> {
    await this.client.delete(`/platform/quotations/${quotationId}`);
  }

  async compareQuotations(firstId: string, secondId: string): Promise<QuotationComparisonResponse> {
    const response = await this.client.get('/platform/quotations/compare', {
      params: { firstId, secondId },
    });
    return response.data;
  }

  async createList(name: string, categoryId?: string): Promise<ProductList> {
    const response = await this.client.post('/platform/lists', { name, categoryId });
    return response.data;
  }

  async updateList(listId: string, name: string): Promise<ProductList> {
    const response = await this.client.patch(`/platform/lists/${listId}`, { name });
    return response.data;
  }

  async deleteList(listId: string): Promise<void> {
    await this.client.delete(`/platform/lists/${listId}`);
  }

  async duplicateList(listId: string, name?: string): Promise<ProductList> {
    const response = await this.client.post(
      `/platform/lists/${listId}/duplicate`,
      name ? { name } : {}
    );
    return response.data;
  }

  async addListItem(
    listId: string,
    description: string,
    quantity: number,
    productId?: string | null
  ): Promise<ProductList> {
    const response = await this.client.post(`/platform/lists/${listId}/items`, {
      description,
      quantity,
      productId,
    });
    return response.data;
  }

  async addBulkListItems(listId: string, lines: string): Promise<ProductList> {
    const response = await this.client.post(`/platform/lists/${listId}/items/bulk`, { lines });
    return response.data;
  }

  async updateListItem(
    listId: string,
    itemId: string,
    description: string,
    quantity: number
  ): Promise<ProductList> {
    const response = await this.client.patch(`/platform/lists/${listId}/items/${itemId}`, {
      description,
      quantity,
    });
    return response.data;
  }

  async deleteListItem(listId: string, itemId: string): Promise<ProductList> {
    const response = await this.client.delete(`/platform/lists/${listId}/items/${itemId}`);
    return response.data;
  }

  async deleteAccount(): Promise<void> {
    await this.client.delete('/platform/account');
  }

  async getCategories(): Promise<Category[]> {
    return (await this.client.get('/platform/categories')).data;
  }

  async getSuppliers(categoryId: string): Promise<Supplier[]> {
    return (await this.client.get(`/platform/categories/${categoryId}/suppliers`)).data;
  }

  async getCatalogProducts(categoryId: string): Promise<CatalogProduct[]> {
    return (await this.client.get(`/platform/categories/${categoryId}/products`)).data;
  }

  getErrorMessage(error: unknown): string {
    if (axios.isAxiosError(error)) {
      if (error.response?.data) {
        const data = error.response.data as { error?: ApiError };
        return data.error?.message || 'Erro na requisição';
      }
      return 'Não foi possível conectar ao servidor. Verifique sua conexão e tente novamente.';
    }

    // O AuthContext usa fetch e lança Error com a mensagem já vinda da API;
    // sem este ramo toda falha de login virava "Erro inesperado".
    if (error instanceof Error && error.message) {
      return error.message;
    }

    return 'Erro inesperado';
  }
}

export const apiService = new ApiService();
