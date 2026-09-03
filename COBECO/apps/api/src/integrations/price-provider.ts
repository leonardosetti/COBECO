export type IncompleteField = 'price' | 'deliveryDays';

export interface PriceSearchInput {
  query: string;
  signal?: AbortSignal;
}

export interface NormalizedPriceResult {
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
  fetchedAt: Date;
  incompleteFields: IncompleteField[];
}

export interface PriceProvider {
  readonly slug: string;
  readonly displayName: string;
  search(input: PriceSearchInput): Promise<NormalizedPriceResult[]>;
}

export interface ProviderSearchStatus {
  providerSlug: string;
  providerName: string;
  state: 'success' | 'empty' | 'failed';
  resultCount: number;
  incompleteCount: number;
  errorCode?: string;
  message?: string;
}

export interface PriceSearchResponse {
  query: string;
  searchedAt: string;
  results: NormalizedPriceResult[];
  providers: ProviderSearchStatus[];
}
