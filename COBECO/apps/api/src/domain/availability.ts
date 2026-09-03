export interface RequestedItem {
  id: string;
  productId: string | null;
  description: string;
  quantity: number;
}

export interface CatalogSupplier {
  id: string;
  name: string;
}

export interface CatalogOffer {
  supplierId: string;
  productId: string;
  price: number;
  active: boolean;
}

export interface AvailableItem extends RequestedItem {
  unitPrice: number;
  subtotal: number;
}

export interface SupplierAvailability {
  supplier: CatalogSupplier;
  availableItems: AvailableItem[];
  missingItems: RequestedItem[];
}

/** Cruza uma lista normalizada com ofertas ativas, sem dependências de infraestrutura. */
export function calculateAvailability(
  items: RequestedItem[],
  suppliers: CatalogSupplier[],
  offers: CatalogOffer[]
): SupplierAvailability[] {
  const offerBySupplierAndProduct = new Map(
    offers
      .filter((offer) => offer.active)
      .map((offer) => [`${offer.supplierId}:${offer.productId}`, offer] as const)
  );

  return suppliers.map((supplier) => {
    const availableItems: AvailableItem[] = [];
    const missingItems: RequestedItem[] = [];

    for (const item of items) {
      const offer = item.productId
        ? offerBySupplierAndProduct.get(`${supplier.id}:${item.productId}`)
        : undefined;
      if (!offer) {
        missingItems.push({ ...item });
        continue;
      }
      availableItems.push({
        ...item,
        unitPrice: offer.price,
        subtotal: offer.price * item.quantity,
      });
    }

    return { supplier: { ...supplier }, availableItems, missingItems };
  });
}
