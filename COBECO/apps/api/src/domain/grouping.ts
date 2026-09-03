import { SupplierAvailability } from './availability';

export interface CoverageGroup {
  groupId: string;
  suppliers: SupplierAvailability[];
  availableItemIds: string[];
  missingItemIds: string[];
  coverage: number;
}

/** Agrupa fornecedores que possuem exatamente o mesmo perfil de cobertura. */
export function groupByCoverageProfile(
  availabilities: SupplierAvailability[],
  totalItems: number
): CoverageGroup[] {
  const grouped = new Map<string, SupplierAvailability[]>();
  for (const availability of availabilities) {
    const signature = availability.availableItems
      .map((item) => item.id)
      .sort()
      .join('|');
    grouped.set(signature, [...(grouped.get(signature) || []), availability]);
  }

  return [...grouped.entries()]
    .map(([signature, suppliers]) => {
      const availableItemIds = signature ? signature.split('|') : [];
      return {
        groupId: '',
        suppliers,
        availableItemIds,
        missingItemIds: suppliers[0]?.missingItems.map((item) => item.id).sort() || [],
        coverage:
          totalItems === 0 ? 0 : Math.round((availableItemIds.length / totalItems) * 10_000) / 100,
      };
    })
    .sort(
      (left, right) =>
        right.availableItemIds.length - left.availableItemIds.length ||
        right.suppliers.length - left.suppliers.length ||
        left.suppliers
          .map((entry) => entry.supplier.name)
          .sort()
          .join()
          .localeCompare(
            right.suppliers
              .map((entry) => entry.supplier.name)
              .sort()
              .join(),
            'pt-BR'
          )
    )
    .map((group, index) => ({ ...group, groupId: `group-${index + 1}` }));
}
